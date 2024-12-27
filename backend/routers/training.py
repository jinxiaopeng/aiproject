"""
靶场训练API路由
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user
from ..services.training_service import TrainingService
from ..schemas.challenge import HintResponse
from ..models.user import User

router = APIRouter(
    prefix="/api/training",
    tags=["training"]
)

@router.post("/{challenge_id}/start")
def start_training(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """开始训练"""
    try:
        progress = TrainingService.start_training(
            db=db,
            user_id=current_user.id,
            challenge_id=challenge_id
        )
        return progress
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{challenge_id}/progress")
def get_progress(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取训练进度"""
    progress = TrainingService.get_training_progress(
        db=db,
        user_id=current_user.id,
        challenge_id=challenge_id
    )
    if not progress:
        raise HTTPException(status_code=404, detail="Training progress not found")
    return progress

@router.put("/{challenge_id}/progress")
def update_progress(
    challenge_id: int,
    step: int,
    completed_tasks: List[bool],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新训练进度"""
    try:
        progress = TrainingService.update_progress(
            db=db,
            user_id=current_user.id,
            challenge_id=challenge_id,
            step=step,
            completed_tasks=completed_tasks
        )
        return progress
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{challenge_id}/hints/{hint_index}")
def unlock_hint(
    challenge_id: int,
    hint_index: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> HintResponse:
    """解锁提示"""
    try:
        return TrainingService.unlock_hint(
            db=db,
            user_id=current_user.id,
            challenge_id=challenge_id,
            hint_index=hint_index
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{challenge_id}/hints")
def get_unlocked_hints(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[int]:
    """获取已解锁的提示"""
    return TrainingService.get_unlocked_hints(
        db=db,
        user_id=current_user.id,
        challenge_id=challenge_id
    ) 