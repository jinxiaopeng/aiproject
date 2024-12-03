from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from ..auth import get_current_user
from ..database import get_db
from sqlalchemy.orm import Session
from ..models import Lesson
from ..schemas import User, LessonNavigation

router = APIRouter(prefix="/api/lessons", tags=["lessons"])

@router.get("/{lesson_id}/navigation", response_model=LessonNavigation)
async def get_lesson_navigation(
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取课时的导航信息（上一课/下一课）"""
    # 获取当前课时信息
    current_lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not current_lesson:
        raise HTTPException(status_code=404, detail="课时不存在")

    # 获取同一课程的所有课时
    course_lessons = db.query(Lesson).filter(
        Lesson.course_id == current_lesson.course_id
    ).order_by(Lesson.chapter_id, Lesson.order_num).all()

    # 找到当前课时的索引
    current_index = next(
        (i for i, lesson in enumerate(course_lessons) if lesson.id == lesson_id),
        -1
    )

    # 获取上一课和下一课
    prev_lesson = None if current_index <= 0 else course_lessons[current_index - 1]
    next_lesson = None if current_index >= len(course_lessons) - 1 else course_lessons[current_index + 1]

    return {
        "current": current_lesson,
        "previous": prev_lesson,
        "next": next_lesson,
        "total": len(course_lessons),
        "current_index": current_index + 1
    } 