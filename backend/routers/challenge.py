from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import traceback

from core.database import get_db
from core.security import verify_flag
from core.docker import docker_manager
from models.challenge import Challenge, ChallengeInstance, ChallengeSubmission
from models.challenge import ChallengeCategory, ChallengeDifficulty
from schemas.challenge import (
    ChallengeCreate,
    ChallengeResponse,
    ChallengeSubmitFlag,
    ChallengeInstanceResponse
)
from config import CHALLENGE_EXPIRE_MINUTES

router = APIRouter()

@router.get("/categories")
async def get_categories():
    """获取题目分类"""
    return [category.value for category in ChallengeCategory]

@router.get("/", response_model=List[ChallengeResponse])
async def get_challenges(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取题目列表"""
    print("开始获取题目列表")
    query = db.query(Challenge).filter(Challenge.is_active == True)
    
    if category:
        print(f"按分类筛选: {category}")
        query = query.filter(Challenge.category == category)
    if difficulty:
        print(f"按难度筛选: {difficulty}")
        query = query.filter(Challenge.difficulty == difficulty)
    
    challenges = query.all()
    print(f"找到 {len(challenges)} 个题目")
    return challenges

@router.get("/{challenge_id}", response_model=ChallengeResponse)
async def get_challenge(challenge_id: int, db: Session = Depends(get_db)):
    """获取题目详情"""
    print(f"开始获取题目详情: {challenge_id}")
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id,
        Challenge.is_active == True
    ).first()
    
    if not challenge:
        print(f"题目不存在: {challenge_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    
    print(f"找到题目: {challenge.title}")
    return challenge

@router.post("/{challenge_id}/submit")
async def submit_flag(
    challenge_id: int,
    submission: ChallengeSubmitFlag,
    db: Session = Depends(get_db)
):
    """提交flag"""
    print(f"开始提交flag: {challenge_id}")
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id,
        Challenge.is_active == True
    ).first()
    
    if not challenge:
        print(f"题目不存在: {challenge_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    
    # 验证flag
    print("开始验证flag")
    is_correct = verify_flag(submission.flag, challenge.flag)
    print(f"flag验证结果: {is_correct}")
    
    # 记录提交
    submission = ChallengeSubmission(
        challenge_id=challenge_id,
        user_id=1,  # TODO: 从token中获取用户ID
        submitted_flag=submission.flag,
        is_correct=is_correct,
        points_awarded=challenge.points if is_correct else 0
    )
    db.add(submission)
    db.commit()
    print("提交记录已保存")
    
    return {
        "is_correct": is_correct,
        "points_awarded": submission.points_awarded
    }

@router.post("/{challenge_id}/instance", response_model=ChallengeInstanceResponse)
async def create_instance(challenge_id: int, db: Session = Depends(get_db)):
    """启动题目实例"""
    print(f"开始启动题目实例: {challenge_id}")
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id,
        Challenge.is_active == True
    ).first()
    
    if not challenge:
        print(f"题目不存在: {challenge_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    
    # 检查是否已有正在运行的实例
    print("检查是否有正在运行的实例")
    existing_instance = db.query(ChallengeInstance).filter(
        ChallengeInstance.challenge_id == challenge_id,
        ChallengeInstance.user_id == 1,  # TODO: 从token中获取用户ID
        ChallengeInstance.is_active == True
    ).first()
    
    if existing_instance:
        print(f"找到正在运行的实例: {existing_instance.id}")
        return existing_instance
    
    try:
        print(f"开始创建Docker容器: {challenge.docker_image}")
        print(f"端口映射: {challenge.port_mapping}")
        
        # 启动Docker容器
        container_id, instance_url = await docker_manager.create_container(
            challenge.docker_image,
            port_mapping=challenge.port_mapping
        )
        print(f"容器创建成功: {container_id}")
        print(f"实例URL: {instance_url}")
        
        # 创建实例记录
        instance = ChallengeInstance(
            challenge_id=challenge_id,
            user_id=1,  # TODO: 从token中获取用户ID
            container_id=container_id,
            instance_url=instance_url,
            expires_at=datetime.utcnow() + timedelta(minutes=CHALLENGE_EXPIRE_MINUTES)
        )
        db.add(instance)
        db.commit()
        db.refresh(instance)
        print(f"实例记录已创建: {instance.id}")
        
        return instance
        
    except Exception as e:
        print(f"启动实例失败: {str(e)}")
        print(f"错误详情: {traceback.format_exc()}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"启动实例失败: {str(e)}"
        )

@router.delete("/{challenge_id}/instance")
async def stop_instance(challenge_id: int, db: Session = Depends(get_db)):
    """停止题目实例"""
    instance = db.query(ChallengeInstance).filter(
        ChallengeInstance.challenge_id == challenge_id,
        ChallengeInstance.user_id == 1,  # TODO: 从token中获取用户ID
        ChallengeInstance.is_active == True
    ).first()
    
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="实例不存在"
        )
    
    try:
        # 停止Docker容器
        await docker_manager.stop_container(instance.container_id)
        
        # 更新实例状态
        instance.is_active = False
        db.commit()
        
        return {"message": "实例已停止"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"停止实例失败: {str(e)}"
        )

@router.get("/{challenge_id}/submissions")
async def get_challenge_submissions(
    challenge_id: int,
    db: Session = Depends(get_db)
):
    """获取题目的提交记录"""
    # 检查题目是否存在
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="题目不存在"
        )
    
    # 获取提交记录
    submissions = db.query(ChallengeSubmission)\
        .filter(ChallengeSubmission.challenge_id == challenge_id)\
        .order_by(ChallengeSubmission.submitted_at.desc())\
        .all()
    
    return submissions 