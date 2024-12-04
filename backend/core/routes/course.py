from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from ..models.course import Course, CourseCreate, CourseUpdate, CourseProgress
from ..models.user import User
from ..utils.auth import get_current_user
from ..database import get_db

router = APIRouter(prefix="/api/courses", tags=["courses"])

@router.get("/", response_model=List[Course])
async def get_courses(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    db = Depends(get_db)
):
    """获取课程列表"""
    query = {}
    if category:
        query["category"] = category
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    courses = await db.courses.find(query).skip(skip).limit(limit).to_list(limit)
    return courses

@router.get("/{course_id}", response_model=Course)
async def get_course(
    course_id: str,
    db = Depends(get_db)
):
    """获取课程详情"""
    course = await db.courses.find_one({"_id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return course

@router.post("/{course_id}/enroll")
async def enroll_course(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """报名课程"""
    # 检查课程是否存在
    course = await db.courses.find_one({"_id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    # 检查是否已经报名
    enrollment = await db.enrollments.find_one({
        "user_id": current_user["id"],
        "course_id": course_id
    })
    if enrollment:
        raise HTTPException(status_code=400, detail="已经报名该课程")
    
    # 创建报名记录
    enrollment = {
        "user_id": current_user["id"],
        "course_id": course_id,
        "enrolled_at": datetime.utcnow(),
        "progress": 0,
        "status": "enrolled"
    }
    await db.enrollments.insert_one(enrollment)
    
    return {"message": "报名成功"}

@router.get("/{course_id}/progress", response_model=CourseProgress)
async def get_course_progress(
    course_id: str,
    current_user: User = Depends(get_current_user),
    db = Depends(get_db)
):
    """获取课程学习进度"""
    # 检查课程是否存在
    course = await db.courses.find_one({"_id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    # 获取报名记录
    enrollment = await db.enrollments.find_one({
        "user_id": current_user["id"],
        "course_id": course_id
    })
    if not enrollment:
        raise HTTPException(status_code=404, detail="未报名该课程")
    
    # 获取学习记录
    progress = await db.course_progress.find_one({
        "user_id": current_user["id"],
        "course_id": course_id
    })
    if not progress:
        progress = {
            "progress": 0,
            "completed_chapters": [],
            "last_study_time": None
        }
    
    return progress 