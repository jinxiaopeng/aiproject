from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..auth import get_current_user
from ..models import (
    LearningProgress,
    Course,
    Lesson,
    User,
    UserLevel
)
from ..schemas import (
    LearningProgressResponse,
    CourseProgressResponse,
    UserProgressResponse,
    UserLevelResponse
)

router = APIRouter(prefix="/api/progress", tags=["progress"])

@router.get("/courses/{course_id}", response_model=CourseProgressResponse)
async def get_course_progress(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取课程学习进度"""
    progress = (
        db.query(LearningProgress)
        .filter(
            LearningProgress.course_id == course_id,
            LearningProgress.user_id == current_user.id
        )
        .first()
    )
    
    if not progress:
        # 创建新的进度记录
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="课程不存在")
            
        total_lessons = (
            db.query(func.count(Lesson.id))
            .filter(Lesson.course_id == course_id)
            .scalar()
        )
        
        progress = LearningProgress(
            user_id=current_user.id,
            course_id=course_id,
            total_lessons=total_lessons,
            completed_lessons=0,
            progress=0
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return progress

@router.post("/courses/{course_id}/lessons/{lesson_id}")
async def update_lesson_progress(
    course_id: int,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新课时学习进度"""
    # 检查课程和课时是否存在
    lesson = (
        db.query(Lesson)
        .filter(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id
        )
        .first()
    )
    
    if not lesson:
        raise HTTPException(status_code=404, detail="课时不存在")
    
    # 更新课程进度
    progress = (
        db.query(LearningProgress)
        .filter(
            LearningProgress.course_id == course_id,
            LearningProgress.user_id == current_user.id
        )
        .first()
    )
    
    if not progress:
        raise HTTPException(status_code=404, detail="进度记录不存在")
    
    # 标记课时为已完成
    if lesson_id not in progress.completed_lesson_ids:
        progress.completed_lesson_ids.append(lesson_id)
        progress.completed_lessons = len(progress.completed_lesson_ids)
        progress.progress = (progress.completed_lessons / progress.total_lessons) * 100
        
        # 如果课程完成，更新用户等级
        if progress.progress == 100:
            await update_user_level(current_user.id, db)
    
    db.commit()
    db.refresh(progress)
    return progress

@router.get("/overview", response_model=UserProgressResponse)
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户总体学习进度"""
    # 获取所有课程进度
    progress_records = (
        db.query(LearningProgress)
        .filter(LearningProgress.user_id == current_user.id)
        .all()
    )
    
    # 计算总体进度
    total_courses = len(progress_records)
    completed_courses = len([p for p in progress_records if p.progress == 100])
    total_lessons = sum(p.total_lessons for p in progress_records)
    completed_lessons = sum(p.completed_lessons for p in progress_records)
    
    # 获取学习时长
    total_learning_time = sum(p.learning_time for p in progress_records)
    
    return {
        "total_courses": total_courses,
        "completed_courses": completed_courses,
        "total_lessons": total_lessons,
        "completed_lessons": completed_lessons,
        "total_learning_time": total_learning_time,
        "overall_progress": (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    }

@router.get("/level", response_model=UserLevelResponse)
async def get_user_level(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户等级信息"""
    level = (
        db.query(UserLevel)
        .filter(UserLevel.user_id == current_user.id)
        .first()
    )
    
    if not level:
        # 创建初始等级记录
        level = UserLevel(
            user_id=current_user.id,
            level=1,
            current_points=0,
            next_level_points=1000
        )
        db.add(level)
        db.commit()
        db.refresh(level)
    
    return level

async def update_user_level(user_id: int, db: Session):
    """更新用户等级"""
    level = (
        db.query(UserLevel)
        .filter(UserLevel.user_id == user_id)
        .first()
    )
    
    if not level:
        return
    
    # 完成课程奖励积分
    reward_points = 500
    level.current_points += reward_points
    
    # 检查是否升级
    while level.current_points >= level.next_level_points:
        level.level += 1
        level.current_points -= level.next_level_points
        level.next_level_points = calculate_next_level_points(level.level)
    
    db.commit()

def calculate_next_level_points(current_level: int) -> int:
    """计算下一级所需积分"""
    return int(1000 * (current_level ** 1.5)) 