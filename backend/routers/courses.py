from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models.course import Course, Chapter, CourseEnrollment, ChapterProgress, CourseNote, CourseComment
from models.user import User
from schemas.course import (
    CourseCreate, CourseUpdate, CourseResponse, 
    ChapterCreate, ChapterUpdate, ChapterResponse,
    CourseNoteCreate, CourseNoteUpdate, CourseNoteResponse,
    CourseCommentCreate, CourseCommentResponse,
    ChapterProgressUpdate,
    PaginatedCourseResponse
)
from core.deps import get_current_user, get_current_user_optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/courses", tags=["courses"])

@router.get("", response_model=PaginatedCourseResponse)
def get_courses(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    sort_by: Optional[str] = "newest",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    try:
        logger.info(f"Getting courses with params: category={category}, difficulty={difficulty}, sort_by={sort_by}, page={page}, limit={limit}")
        
        query = db.query(Course)
        
        if category:
            query = query.filter(Course.category == category)
        if difficulty:
            query = query.filter(Course.difficulty == difficulty)
            
        if sort_by == "popular":
            query = query.outerjoin(CourseEnrollment).group_by(Course.id).order_by(func.count(CourseEnrollment.id).desc())
        elif sort_by == "rating":
            query = query.outerjoin(CourseComment).group_by(Course.id).order_by(func.avg(CourseComment.rating).desc())
        else:  # newest
            query = query.order_by(Course.created_at.desc())
        
        total = query.count()
        courses = query.offset((page - 1) * limit).limit(limit).all()
        
        logger.info(f"Found {len(courses)} courses, total: {total}")
        
        # 获取用户的学习进度
        if current_user:
            for course in courses:
                enrollment = db.query(CourseEnrollment).filter(
                    CourseEnrollment.course_id == course.id,
                    CourseEnrollment.user_id == current_user.id
                ).first()
                if enrollment:
                    course.progress = enrollment.progress
        
        return {
            "items": courses,
            "total": total,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"Error getting courses: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取课程列表失败: {str(e)}"
        )

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    try:
        logger.info(f"Getting course with id: {course_id}")
        
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        # 获取用户的学习进度
        if current_user:
            enrollment = db.query(CourseEnrollment).filter(
                CourseEnrollment.course_id == course_id,
                CourseEnrollment.user_id == current_user.id
            ).first()
            
            if enrollment:
                course.progress = enrollment.progress
                
                # 获取章节进度
                chapter_progress = db.query(ChapterProgress).filter(
                    ChapterProgress.user_id == current_user.id,
                    ChapterProgress.chapter_id.in_([c.id for c in course.chapters])
                ).all()
                
                progress_map = {p.chapter_id: p for p in chapter_progress}
                for chapter in course.chapters:
                    if chapter.id in progress_map:
                        chapter.progress = progress_map[chapter.id].progress
                        chapter.completed = progress_map[chapter.id].completed
        
        return course
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting course {course_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取课程详情失败: {str(e)}"
        )

@router.post("/{course_id}/enroll")
def enroll_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id,
        CourseEnrollment.user_id == current_user.id
    ).first()
    
    if enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled")
    
    enrollment = CourseEnrollment(
        user_id=current_user.id,
        course_id=course_id
    )
    db.add(enrollment)
    db.commit()
    
    return {"message": "Enrolled successfully"}

@router.post("/{course_id}/chapters/{chapter_id}/progress")
def update_chapter_progress(
    course_id: int,
    chapter_id: int,
    progress_data: ChapterProgressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    chapter = db.query(Chapter).filter(
        Chapter.id == chapter_id,
        Chapter.course_id == course_id
    ).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    progress = db.query(ChapterProgress).filter(
        ChapterProgress.chapter_id == chapter_id,
        ChapterProgress.user_id == current_user.id
    ).first()
    
    if not progress:
        progress = ChapterProgress(
            user_id=current_user.id,
            chapter_id=chapter_id
        )
        db.add(progress)
    
    progress.progress = progress_data.progress
    if progress.progress >= 95:  # 95%以上视为完成
        progress.completed = True
    
    # 更新课程总进度
    enrollment = db.query(CourseEnrollment).filter(
        CourseEnrollment.course_id == course_id,
        CourseEnrollment.user_id == current_user.id
    ).first()
    
    if enrollment:
        total_progress = db.query(func.avg(ChapterProgress.progress)).filter(
            ChapterProgress.user_id == current_user.id,
            ChapterProgress.chapter_id.in_([c.id for c in chapter.course.chapters])
        ).scalar() or 0
        
        enrollment.progress = total_progress
        if total_progress >= 95:
            enrollment.completed = True
    
    db.commit()
    return {"message": "Progress updated"}

@router.post("/{course_id}/notes", response_model=CourseNoteResponse)
def create_note(
    course_id: int,
    note: CourseNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if note.chapter_id:
        chapter = db.query(Chapter).filter(
            Chapter.id == note.chapter_id,
            Chapter.course_id == course_id
        ).first()
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
    
    db_note = CourseNote(
        user_id=current_user.id,
        course_id=course_id,
        chapter_id=note.chapter_id,
        content=note.content
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.put("/notes/{note_id}", response_model=CourseNoteResponse)
def update_note(
    note_id: int,
    note: CourseNoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_note = db.query(CourseNote).filter(
        CourseNote.id == note_id,
        CourseNote.user_id == current_user.id
    ).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_note = db.query(CourseNote).filter(
        CourseNote.id == note_id,
        CourseNote.user_id == current_user.id
    ).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted"}

@router.get("/{course_id}/notes", response_model=List[CourseNoteResponse])
def get_course_notes(
    course_id: int,
    chapter_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(CourseNote).filter(
        CourseNote.course_id == course_id,
        CourseNote.user_id == current_user.id
    )
    
    if chapter_id:
        query = query.filter(CourseNote.chapter_id == chapter_id)
    
    notes = query.order_by(CourseNote.created_at.desc()).all()
    return notes

@router.post("/{course_id}/comments", response_model=CourseCommentResponse)
def create_comment(
    course_id: int,
    comment: CourseCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_comment = CourseComment(
        user_id=current_user.id,
        course_id=course_id,
        content=comment.content,
        rating=comment.rating
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/{course_id}/comments", response_model=List[CourseCommentResponse])
def get_course_comments(
    course_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    comments = db.query(CourseComment).filter(
        CourseComment.course_id == course_id
    ).order_by(
        CourseComment.created_at.desc()
    ).offset(
        (page - 1) * limit
    ).limit(limit).all()
    
    return comments