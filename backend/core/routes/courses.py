from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_current_user
from ..schemas import (
    CourseCreate,
    CourseUpdate,
    CourseResponse,
    CourseDetailResponse,
    ChapterResponse,
    LessonResponse,
    User
)
from ..services.course import CourseService

router = APIRouter(prefix="/api/courses", tags=["courses"])

def get_course_service(db: Session = Depends(get_db)) -> CourseService:
    return CourseService(db)

@router.get("", response_model=List[CourseResponse])
async def get_courses(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    course_service: CourseService = Depends(get_course_service)
):
    """获取课程列表"""
    return course_service.get_courses(category, difficulty, search)

@router.get("/{course_id}", response_model=CourseDetailResponse)
async def get_course_detail(
    course_id: int,
    current_user: User = Depends(get_current_user),
    course_service: CourseService = Depends(get_course_service)
):
    """获取课程详情"""
    course = course_service.get_course_detail(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return course

@router.post("", response_model=CourseResponse)
async def create_course(
    course_data: CourseCreate,
    current_user: User = Depends(get_current_user),
    course_service: CourseService = Depends(get_course_service)
):
    """创建新课程"""
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="没有创建课程的权限")
    return course_service.create_course(course_data, current_user.id)

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    current_user: User = Depends(get_current_user),
    course_service: CourseService = Depends(get_course_service)
):
    """更新课程信息"""
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="没有更新课程的权限")
    course = course_service.get_course_detail(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    if course.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="没有权限修改此课程")
    return course_service.update_course(course_id, course_data)

@router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    current_user: User = Depends(get_current_user),
    course_service: CourseService = Depends(get_course_service)
):
    """删除课程"""
    if current_user.role not in ["admin", "teacher"]:
        raise HTTPException(status_code=403, detail="没有删除课程的权限")
    course = course_service.get_course_detail(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    if course.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="没有权限删除此课程")
    course_service.delete_course(course_id)
    return {"message": "课程已删除"}

@router.get("/{course_id}/chapters", response_model=List[ChapterResponse])
async def get_course_chapters(
    course_id: int,
    current_user: User = Depends(get_current_user),
    course_service: CourseService = Depends(get_course_service)
):
    """获取课程章节列表"""
    return course_service.get_course_chapters(course_id)

@router.get("/{course_id}/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson_detail(
    course_id: int,
    lesson_id: int,
    current_user: User = Depends(get_current_user),
    course_service: CourseService = Depends(get_course_service)
):
    """获取课时详情"""
    lesson = course_service.get_lesson_detail(course_id, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="课时不存在")
    return lesson

@router.post("/{course_id}/progress")
async def update_learning_progress(
    course_id: int,
    lesson_id: int = Body(...),
    progress: float = Body(...),
    current_user: User = Depends(get_current_user),
    course_service: CourseService = Depends(get_course_service)
):
    """更新学习进度"""
    return course_service.update_learning_progress(
        user_id=current_user.id,
        course_id=course_id,
        lesson_id=lesson_id,
        progress=progress
    )

@router.get("/recommended", response_model=List[CourseResponse])
async def get_recommended_courses(
    current_user: User = Depends(get_current_user),
    course_service: CourseService = Depends(get_course_service)
):
    """获取推荐课程"""
    return course_service.get_recommended_courses(current_user.id) 