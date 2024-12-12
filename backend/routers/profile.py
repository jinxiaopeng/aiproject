from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import aiofiles
from datetime import datetime, timedelta

from ..database import get_db
from ..models import User, UserActivity, UserStats, UserSkill
from ..schemas.profile import (
    UserProfileResponse,
    UpdateProfileRequest,
    ActivityResponse,
    StatsResponse,
    SkillResponse,
    ChangePasswordRequest,
    ChangeEmailRequest
)
from ..utils.auth import get_current_user
from ..utils.storage import upload_file
from ..utils.email import send_verification_code
from ..utils.security import get_password_hash

router = APIRouter(prefix="/api/profile", tags=["profile"])

@router.get("/info", response_model=UserProfileResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """获取用户个人信息"""
    return current_user

@router.put("/info", response_model=UserProfileResponse)
async def update_profile(
    request: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户个人信息"""
    for key, value in request.dict(exclude_unset=True).items():
        setattr(current_user, key, value)
    
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传用户头像"""
    # 验证文件类型
    if not file.content_type in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="只支持JPG和PNG格式的图片")
    
    # 验证文件大小
    content = await file.read()
    if len(content) > 2 * 1024 * 1024:  # 2MB
        raise HTTPException(status_code=400, detail="文件大小不能超过2MB")
    
    # 上传文件
    file_url = await upload_file(content, file.filename, "avatars")
    
    # 更新用户头像
    current_user.avatar = file_url
    db.commit()
    
    return {"url": file_url}

@router.get("/activities", response_model=List[ActivityResponse])
async def get_activities(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户最近活动"""
    activities = db.query(UserActivity)\
        .filter(UserActivity.user_id == current_user.id)\
        .order_by(UserActivity.created_at.desc())\
        .limit(10)\
        .all()
    return activities

@router.get("/stats", response_model=StatsResponse)
async def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户统计数据"""
    stats = db.query(UserStats)\
        .filter(UserStats.user_id == current_user.id)\
        .first()
    
    if not stats:
        stats = UserStats(user_id=current_user.id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    
    return stats

@router.get("/skills", response_model=List[SkillResponse])
async def get_skills(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户技能数据"""
    skills = db.query(UserSkill)\
        .filter(UserSkill.user_id == current_user.id)\
        .all()
    return skills

@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改密码"""
    if not current_user.verify_password(request.old_password):
        raise HTTPException(status_code=400, detail="原密码错误")
    
    current_user.hashed_password = get_password_hash(request.new_password)
    db.commit()
    return {"message": "密码修改成功"}

@router.post("/change-email/code")
async def send_email_code(
    email: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发送邮箱验证码"""
    # 检查邮箱是否已被使用
    if db.query(User).filter(User.email == email, User.id != current_user.id).first():
        raise HTTPException(status_code=400, detail="该邮箱已被使用")
    
    # 发送验证码
    code = await send_verification_code(email)
    return {"message": "验证码已发送"}

@router.post("/change-email")
async def change_email(
    request: ChangeEmailRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改邮箱"""
    # 验证验证码
    # TODO: 实现验证码验证逻辑
    
    current_user.email = request.email
    db.commit()
    return {"message": "邮箱修改成功"} 