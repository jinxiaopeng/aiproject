from fastapi import APIRouter, Depends, HTTPException, Body, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from models import Challenge, ChallengeSubmission, ChallengeInstance, User, ChallengeCategory, ChallengeDifficulty
from schemas.challenge import (
    ChallengeCreate, 
    ChallengeResponse, 
    ChallengeSubmitFlag,
    ChallengeInstanceCreate,
    ChallengeInstanceResponse
)
from core.auth import get_current_user
from core.docker import docker_manager
from core.database import get_db
from core.security import verify_flag

router = APIRouter()

@router.get("/categories")
async def get_categories():
    """获取题目分类"""
    return [{"key": cat.name, "value": cat.value} for cat in ChallengeCategory]

@router.get("/challenges")
async def get_challenges(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取题目列表"""
    query = db.query(Challenge).filter(Challenge.is_active == True)
    
    if category:
        query = query.filter(Challenge.category == category)
    if difficulty:
        query = query.filter(Challenge.difficulty == difficulty)
        
    challenges = query.all()
    
    # 获取用户已解决的题目
    solved = set(
        db.query(ChallengeSubmission.challenge_id)
        .filter(
            ChallengeSubmission.user_id == current_user.id,
            ChallengeSubmission.is_correct == True
        )
        .all()
    )
    
    return [
        {
            **challenge.__dict__,
            "is_solved": challenge.id in solved,
            "solved_count": len([s for s in challenge.submissions if s.is_correct])
        }
        for challenge in challenges
    ]

@router.post("/challenges")
async def create_challenge(
    challenge: ChallengeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新题目"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="只有管理员可以创建题目")
        
    db_challenge = Challenge(**challenge.dict(), created_by=current_user.id)
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge

@router.post("/challenges/{challenge_id}/submit")
async def submit_flag(
    challenge_id: int,
    submission: ChallengeSubmitFlag,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """提交Flag"""
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="题目不存在")
        
    # 检查是否已经解决
    existing_solve = db.query(ChallengeSubmission).filter(
        ChallengeSubmission.challenge_id == challenge_id,
        ChallengeSubmission.user_id == current_user.id,
        ChallengeSubmission.is_correct == True
    ).first()
    
    if existing_solve:
        raise HTTPException(status_code=400, detail="你已经解决过这道题目")
    
    # 验证flag
    is_correct = verify_flag(submission.flag, challenge.flag)
    
    # 记录提交
    submission = ChallengeSubmission(
        challenge_id=challenge_id,
        user_id=current_user.id,
        submitted_flag=submission.flag,
        is_correct=is_correct,
        points_awarded=challenge.points if is_correct else 0
    )
    
    db.add(submission)
    db.commit()
    
    return {"success": is_correct, "message": "恭喜你解出题目！" if is_correct else "Flag不正确"}

@router.post("/challenges/{challenge_id}/instance")
async def create_challenge_instance(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建题目实例（启动Docker容器）"""
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="题目不存在")
        
    if not challenge.docker_image:
        raise HTTPException(status_code=400, detail="此题目没有Docker环境")
    
    # 检查用户是否已有正在运行的实例
    existing_instance = db.query(ChallengeInstance).filter(
        ChallengeInstance.challenge_id == challenge_id,
        ChallengeInstance.user_id == current_user.id,
        ChallengeInstance.is_active == True
    ).first()
    
    if existing_instance:
        return existing_instance
    
    # 创建新实例
    container_id, instance_url = await docker_manager.create_container(
        challenge.docker_image,
        challenge.docker_compose,
        challenge.port_mapping
    )
    
    instance = ChallengeInstance(
        challenge_id=challenge_id,
        user_id=current_user.id,
        container_id=container_id,
        instance_url=instance_url,
        expires_at=datetime.utcnow() + timedelta(hours=2)  # 2小时后过期
    )
    
    db.add(instance)
    db.commit()
    db.refresh(instance)
    
    return instance

@router.delete("/challenges/{challenge_id}/instance")
async def delete_challenge_instance(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除题目实例（停止Docker容器）"""
    instance = db.query(ChallengeInstance).filter(
        ChallengeInstance.challenge_id == challenge_id,
        ChallengeInstance.user_id == current_user.id,
        ChallengeInstance.is_active == True
    ).first()
    
    if not instance:
        raise HTTPException(status_code=404, detail="未找到运行中的实例")
    
    await docker_manager.stop_container(instance.container_id)
    
    instance.is_active = False
    db.commit()
    
    return {"message": "实例已停止"} 