from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from ..auth import get_current_user
from ..database import get_db
from ..models import CourseProgress, LessonProgress, LearningRecord, Course, Lesson
from ..schemas import (
    User, 
    CourseProgressCreate,
    CourseProgressUpdate,
    CourseProgressResponse,
    LessonProgressCreate,
    LessonProgressUpdate,
    LessonProgressResponse,
    LearningRecordCreate
)

router = APIRouter(prefix="/api/progress", tags=["progress"])

@router.get("/courses/{course_id}", response_model=CourseProgressResponse)
async def get_course_progress(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的课程学习进度"""
    progress = db.query(CourseProgress).filter(
        CourseProgress.user_id == current_user.id,
        CourseProgress.course_id == course_id
    ).first()
    
    if not progress:
        # 如果没有进度记录，创建一个新的
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="课程不存在")
            
        total_lessons = db.query(Lesson).filter(Lesson.course_id == course_id).count()
        progress = CourseProgress(
            user_id=current_user.id,
            course_id=course_id,
            total_lessons=total_lessons,
            total_duration=0  # 这里需要计算课程总时长
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return progress

@router.get("/lessons/{lesson_id}", response_model=LessonProgressResponse)
async def get_lesson_progress(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户的课时学习进度"""
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        # 如果没有进度记录，创建一个新的
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=404, detail="课时不存在")
            
        progress = LessonProgress(
            user_id=current_user.id,
            lesson_id=lesson_id,
            course_id=lesson.course_id
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return progress

@router.post("/lessons/{lesson_id}/record", response_model=LessonProgressResponse)
async def record_learning_progress(
    lesson_id: int,
    record: LearningRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """记录学习行为并更新进度"""
    # 获取课时进度
    progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.lesson_id == lesson_id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="未找到学习进度记录")
    
    # 创建学习记录
    learning_record = LearningRecord(
        user_id=current_user.id,
        course_id=progress.course_id,
        lesson_id=lesson_id,
        action=record.action,
        position=record.position,
        duration=record.duration
    )
    db.add(learning_record)
    
    # 更新课时进度
    if record.action == "start":
        if not progress.started_at:
            progress.started_at = datetime.now()
            progress.status = "in_progress"
    elif record.action == "complete":
        progress.completed_at = datetime.now()
        progress.status = "completed"
        progress.progress = 100
        
        # 更新课程进度
        course_progress = db.query(CourseProgress).filter(
            CourseProgress.user_id == current_user.id,
            CourseProgress.course_id == progress.course_id
        ).first()
        
        if course_progress:
            course_progress.completed_lessons += 1
            course_progress.progress = (course_progress.completed_lessons / course_progress.total_lessons) * 100
            if course_progress.progress >= 100:
                course_progress.status = "completed"
                course_progress.completed_at = datetime.now()
    
    progress.last_position = record.position
    progress.learning_time += record.duration
    
    db.commit()
    db.refresh(progress)
    return progress

@router.get("/courses/{course_id}/statistics")
async def get_course_statistics(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取课程学习统计信息"""
    progress = db.query(CourseProgress).filter(
        CourseProgress.user_id == current_user.id,
        CourseProgress.course_id == course_id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="未找到课程进度记录")
    
    # 获取所有课时进度
    lesson_progress = db.query(LessonProgress).filter(
        LessonProgress.user_id == current_user.id,
        LessonProgress.course_id == course_id
    ).all()
    
    # 计算统计信息
    total_learning_time = sum(p.learning_time for p in lesson_progress)
    completed_lessons = len([p for p in lesson_progress if p.status == "completed"])
    in_progress_lessons = len([p for p in lesson_progress if p.status == "in_progress"])
    
    return {
        "total_learning_time": total_learning_time,
        "completed_lessons": completed_lessons,
        "in_progress_lessons": in_progress_lessons,
        "total_lessons": progress.total_lessons,
        "overall_progress": progress.progress,
        "status": progress.status
    } 