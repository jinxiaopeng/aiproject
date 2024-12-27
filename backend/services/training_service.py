"""
训练相关服务
"""

from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.challenge import Challenge
from ..models.training_progress import TrainingProgress
from ..models.hint_unlock import HintUnlock
from ..models.user import User
from ..schemas.challenge import TrainingStep, HintResponse

class TrainingService:
    @staticmethod
    def get_training_progress(
        db: Session,
        user_id: int,
        challenge_id: int
    ) -> Optional[TrainingProgress]:
        """获取训练进度"""
        return db.query(TrainingProgress).filter(
            and_(
                TrainingProgress.user_id == user_id,
                TrainingProgress.challenge_id == challenge_id
            )
        ).first()
    
    @staticmethod
    def start_training(
        db: Session,
        user_id: int,
        challenge_id: int
    ) -> TrainingProgress:
        """开始训练"""
        # 检查是否已存在进度
        progress = TrainingService.get_training_progress(db, user_id, challenge_id)
        if progress:
            # 如果已完成，不允许重新开始
            if progress.completed_at:
                raise ValueError("Training already completed")
            return progress
            
        # 创建新的进度记录
        progress = TrainingProgress(
            user_id=user_id,
            challenge_id=challenge_id,
            current_step=0,
            completed_tasks=[],
            unlocked_hints=[],
            start_time=datetime.utcnow()
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
        return progress
    
    @staticmethod
    def update_progress(
        db: Session,
        user_id: int,
        challenge_id: int,
        step: int,
        completed_tasks: List[bool]
    ) -> TrainingProgress:
        """更新训练进度"""
        progress = TrainingService.get_training_progress(db, user_id, challenge_id)
        if not progress:
            raise ValueError("Training not started")
            
        # 获取靶场信息
        challenge = db.query(Challenge).get(challenge_id)
        if not challenge or not challenge.steps:
            raise ValueError("Invalid challenge")
            
        # 验证步骤
        if step >= len(challenge.steps):
            raise ValueError("Invalid step")
            
        # 更新进度
        progress.current_step = step
        progress.completed_tasks = completed_tasks
        progress.last_active_time = datetime.utcnow()
        
        # 检查是否完成所有步骤
        if step == len(challenge.steps) - 1 and all(completed_tasks):
            progress.completed_at = datetime.utcnow()
            
            # 更新靶场统计
            challenge.completions = (challenge.completions or 0) + 1
            total_attempts = db.query(TrainingProgress).filter(
                TrainingProgress.challenge_id == challenge_id
            ).count()
            challenge.pass_rate = (challenge.completions / total_attempts) * 100
        
        db.commit()
        db.refresh(progress)
        return progress
    
    @staticmethod
    def unlock_hint(
        db: Session,
        user_id: int,
        challenge_id: int,
        hint_index: int
    ) -> HintResponse:
        """解锁提示"""
        # 检查提示是否已解锁
        existing = db.query(HintUnlock).filter(
            and_(
                HintUnlock.user_id == user_id,
                HintUnlock.challenge_id == challenge_id,
                HintUnlock.hint_index == hint_index
            )
        ).first()
        if existing:
            raise ValueError("Hint already unlocked")
            
        # 获取靶场信息
        challenge = db.query(Challenge).get(challenge_id)
        if not challenge or not challenge.hints:
            raise ValueError("Invalid challenge")
            
        # 验证提示索引
        if hint_index >= len(challenge.hints):
            raise ValueError("Invalid hint index")
            
        # 计算消耗积分
        cost = 10 * (hint_index + 1)  # 每个提示消耗递增的积分
        
        # 检查用户积分
        user = db.query(User).get(user_id)
        if not user or user.points < cost:
            raise ValueError("Insufficient points")
            
        # 扣除积分
        user.points -= cost
        
        # 记录解锁
        unlock = HintUnlock(
            user_id=user_id,
            challenge_id=challenge_id,
            hint_index=hint_index,
            cost=cost
        )
        db.add(unlock)
        
        # 更新进度中的已解锁提示
        progress = TrainingService.get_training_progress(db, user_id, challenge_id)
        if progress:
            unlocked = progress.unlocked_hints or []
            unlocked.append(hint_index)
            progress.unlocked_hints = unlocked
        
        db.commit()
        
        return HintResponse(
            hint=challenge.hints[hint_index],
            cost=cost
        )
    
    @staticmethod
    def get_unlocked_hints(
        db: Session,
        user_id: int,
        challenge_id: int
    ) -> List[int]:
        """获取已解锁的提示"""
        unlocks = db.query(HintUnlock).filter(
            and_(
                HintUnlock.user_id == user_id,
                HintUnlock.challenge_id == challenge_id
            )
        ).all()
        return [u.hint_index for u in unlocks] 