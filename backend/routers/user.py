from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from backend.core.deps import get_current_user, get_db
from backend.models.user import User
from backend.models.lab import LabProgress

router = APIRouter(prefix="/user", tags=["user"])
logger = logging.getLogger(__name__)

@router.get("/profile")
async def get_user_profile(current_user = Depends(get_current_user)):
    """获取当前用户信息"""
    logger.info(f"用户 {current_user.username} 请求个人信息")
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "status": current_user.status,
        "last_login": current_user.last_login
    }

@router.get("/stats")
async def get_user_stats(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户统计信息"""
    logger.info(f"用户 {current_user.username} 请求统计信息")
    
    # 获取完成的靶场数量
    completed_labs = db.query(LabProgress).filter(
        LabProgress.user_id == current_user.id,
        LabProgress.status == "completed"
    ).count()
    
    # 获取总得分
    total_score = db.query(LabProgress).filter(
        LabProgress.user_id == current_user.id,
        LabProgress.status == "completed"
    ).with_entities(
        db.func.sum(LabProgress.score)
    ).scalar() or 0
    
    # 获取最近完成的靶场
    recent_labs = db.query(LabProgress).filter(
        LabProgress.user_id == current_user.id,
        LabProgress.status == "completed"
    ).order_by(
        LabProgress.completed_at.desc()
    ).limit(5).all()
    
    recent_completions = [{
        "lab_id": progress.lab_id,
        "completed_at": progress.completed_at,
        "score": progress.score
    } for progress in recent_labs]
    
    logger.debug(f"用户统计: 完成靶场={completed_labs}, 总分={total_score}")
    
    return {
        "completed_labs": completed_labs,
        "total_score": total_score,
        "recent_completions": recent_completions
    } 