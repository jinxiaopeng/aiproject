from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from datetime import datetime
from sqlalchemy import func

from database import get_db
from models.course import Course, Chapter, CourseEnrollment, ChapterProgress
from models.user import User
from schemas.course import CourseCreate, CourseUpdate, ChapterCreate, ChapterUpdate, CourseResponse
from core.deps import get_current_user, get_current_user_optional

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("")
async def get_courses(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    sort_by: Optional[str] = None,
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """获取课程列表"""
    query = db.query(Course)
    
    # 应用过滤条件
    if category:
        query = query.filter(Course.category == category)
    if difficulty:
        query = query.filter(Course.difficulty == difficulty)
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            Course.title.ilike(search_pattern) | 
            Course.description.ilike(search_pattern)
        )
        
    # 应用排序
    if sort_by == "newest":
        query = query.order_by(Course.created_at.desc())
    elif sort_by == "popular":
        query = query.order_by(Course.student_count.desc())
    elif sort_by == "rating":
        query = query.order_by(Course.rating.desc())
    else:
        query = query.order_by(Course.created_at.desc())
    
    # 分页
    courses = query.offset((page - 1) * limit).limit(limit).all()
    
    # 如果用户已登录，查询课程进度
    if current_user:
        for course in courses:
            # 查询用户是否已报名
            enrollment = db.query(CourseEnrollment).filter(
                CourseEnrollment.course_id == course.id,
                CourseEnrollment.user_id == current_user.id
            ).first()
            
            if enrollment:
                # 计算课程总进度
                chapter_progress = db.query(
                    func.avg(ChapterProgress.progress)
                ).filter(
                    ChapterProgress.chapter_id.in_([c.id for c in course.chapters]),
                    ChapterProgress.user_id == current_user.id
                ).scalar()
                
                course.progress = round(chapter_progress or 0)
    
    return courses

@router.post("/{course_id}/enroll")
async def enroll_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """报名课程"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
        
    # 检查是否已报名
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id,
        CourseEnrollment.user_id == current_user.id
    ).first()
    
    if enrollment:
        raise HTTPException(status_code=400, detail="已经报名过该课程")
        
    # 创建报名记录
    enrollment = CourseEnrollment(
        course_id=course_id,
        user_id=current_user.id
    )
    db.add(enrollment)
    
    # 更新课程学习人数
    course.student_count += 1
    
    db.commit()
    return {"message": "报名成功"}

@router.post("/chapters/{chapter_id}/progress")
async def update_chapter_progress(
    chapter_id: int,
    progress: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新章节学习进度"""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")
        
    # 检查是否已报名课程
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == chapter.course_id,
        CourseEnrollment.user_id == current_user.id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=403, detail="请先报名课程")
        
    # 更新或创建进度记录
    chapter_progress = db.query(ChapterProgress).filter(
        ChapterProgress.chapter_id == chapter_id,
        ChapterProgress.user_id == current_user.id
    ).first()
    
    if chapter_progress:
        chapter_progress.progress = progress["progress"]
        chapter_progress.last_position = progress["last_position"]
        chapter_progress.completed = progress["completed"]
    else:
        chapter_progress = ChapterProgress(
            chapter_id=chapter_id,
            user_id=current_user.id,
            progress=progress["progress"],
            last_position=progress["last_position"],
            completed=progress["completed"]
        )
        db.add(chapter_progress)
    
    # 更新最后访问时间
    enrollment.last_accessed_at = datetime.utcnow()
    db.commit()
    
    return {"message": "进度更新成功"}

@router.post("/chapters/{chapter_id}/upload-video")
async def upload_chapter_video(
    chapter_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """上传章节视频"""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    # 检查是否是课程创建者
    course = db.query(Course).filter(Course.id == chapter.course_id).first()
    if course.instructor_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限上传视频")

    # 创建课程视频目录
    video_dir = os.path.join("static", "videos", f"course_{course.id}")
    os.makedirs(video_dir, exist_ok=True)

    # 保存视频文件
    file_extension = os.path.splitext(file.filename)[1]
    video_filename = f"chapter_{chapter_id}{file_extension}"
    video_path = os.path.join(video_dir, video_filename)
    
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 更新数据中的视频URL
    video_url = f"/static/videos/course_{course.id}/{video_filename}"
    chapter.video_url = video_url
    db.commit()

    return {"message": "视频上传成功", "video_url": video_url}

@router.get("/chapters/{chapter_id}/video")
async def get_chapter_video(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取章节视频信息"""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="章节不存在")

    # 检查用户是否已报名课程
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == chapter.course_id,
        CourseEnrollment.user_id == current_user.id
    ).first()

    if not enrollment:
        raise HTTPException(status_code=403, detail="请先报名课程")

    if not chapter.video_url:
        raise HTTPException(status_code=404, detail="视频不存在")

    # 更新最后访问时间
    enrollment.last_accessed_at = datetime.utcnow()
    db.commit()

    return {
        "video_url": chapter.video_url,
        "duration": chapter.duration,
        "title": chapter.title
    } 

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    """获取课程详情"""
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return course 