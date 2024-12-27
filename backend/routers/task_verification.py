"""
任务验证路由
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List

from ..dependencies import get_db, get_current_user
from ..models.user import User
from ..services.task_verification import TaskVerificationService

router = APIRouter(
    prefix="/api/tasks",
    tags=["task_verification"]
)

@router.post("/{challenge_id}/flag")
async def submit_flag(
    challenge_id: int,
    flag: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """提交flag"""
    try:
        return TaskVerificationService.verify_flag(
            db=db,
            user_id=current_user.id,
            challenge_id=challenge_id,
            flag=flag
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{challenge_id}/verify")
async def verify_task(
    challenge_id: int,
    step: int,
    task_index: int,
    result: Dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """验证任务"""
    try:
        success = TaskVerificationService.verify_task(
            db=db,
            user_id=current_user.id,
            challenge_id=challenge_id,
            step=step,
            task_index=task_index,
            result=result
        )
        return {"success": success}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{challenge_id}/hints")
async def get_task_hints(
    challenge_id: int,
    step: int,
    task_index: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[str]:
    """获取任务提示"""
    try:
        return TaskVerificationService.get_task_hints(
            db=db,
            challenge_id=challenge_id,
            step=step,
            task_index=task_index
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 