from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..auth import get_current_user
from ..rewards import RewardService
from ..schemas import (
    User,
    AchievementTypeResponse,
    UserAchievementResponse,
    PointHistoryResponse,
    LevelRuleResponse,
    UserLevelResponse
)

router = APIRouter(prefix="/api/rewards", tags=["rewards"])

def get_reward_service(db: Session = Depends(get_db)) -> RewardService:
    return RewardService(db)

@router.get("/achievements/types", response_model=List[AchievementTypeResponse])
async def get_achievement_types(
    current_user: User = Depends(get_current_user),
    reward_service: RewardService = Depends(get_reward_service)
):
    """获取所有成就类型"""
    return reward_service.get_achievement_types()

@router.get("/achievements", response_model=List[UserAchievementResponse])
async def get_user_achievements(
    current_user: User = Depends(get_current_user),
    reward_service: RewardService = Depends(get_reward_service)
):
    """获取用户的所有成就"""
    return reward_service.get_user_achievements(current_user.id)

@router.post("/achievements/check", response_model=List[UserAchievementResponse])
async def check_achievements(
    current_user: User = Depends(get_current_user),
    reward_service: RewardService = Depends(get_reward_service)
):
    """检查并更新用户成就"""
    return reward_service.check_achievements(current_user.id)

@router.get("/points/history", response_model=List[PointHistoryResponse])
async def get_point_history(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    reward_service: RewardService = Depends(get_reward_service)
):
    """获取用户积分历史"""
    return reward_service.get_point_history(current_user.id, limit)

@router.get("/levels/rules", response_model=List[LevelRuleResponse])
async def get_level_rules(
    current_user: User = Depends(get_current_user),
    reward_service: RewardService = Depends(get_reward_service)
):
    """获取所有等级规则"""
    return reward_service.get_level_rules()

@router.get("/levels/current", response_model=UserLevelResponse)
async def get_user_level(
    current_user: User = Depends(get_current_user),
    reward_service: RewardService = Depends(get_reward_service)
):
    """获取用户当前等级信息"""
    level = reward_service.get_user_level(current_user.id)
    if not level:
        raise HTTPException(status_code=404, detail="未找到用户等级信息") 