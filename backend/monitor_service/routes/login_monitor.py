from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..database import get_db
from ..services.login_monitor import LoginMonitorService
from ..schemas.monitor import LoginMonitorCreate, LoginMonitor
from ..models.monitor import LoginEventType

router = APIRouter(prefix="/login", tags=["login_monitor"])

@router.post("/events", response_model=LoginMonitor)
async def create_login_event(
    event: LoginMonitorCreate,
    db: Session = Depends(get_db)
):
    """创建登录事件记录"""
    service = LoginMonitorService(db)
    return service.create_login_event(event)

@router.get("/events", response_model=List[LoginMonitor])
async def get_login_events(
    user_id: Optional[int] = None,
    event_type: Optional[LoginEventType] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """获取登录事件记录列表"""
    service = LoginMonitorService(db)
    return service.get_login_events(
        user_id=user_id,
        event_type=event_type,
        start_time=start_time,
        end_time=end_time,
        skip=skip,
        limit=limit
    )

@router.get("/failed-attempts/{user_id}")
async def get_failed_login_attempts(
    user_id: int,
    minutes: int = Query(30, ge=1, le=1440),
    db: Session = Depends(get_db)
):
    """获取用户的失败登录尝试次数"""
    service = LoginMonitorService(db)
    attempts = service.get_failed_login_attempts(user_id, minutes)
    return {
        "user_id": user_id,
        "failed_attempts": attempts,
        "time_window_minutes": minutes
    }

@router.get("/statistics")
async def get_login_statistics(
    user_id: Optional[int] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """获取登录统计信息"""
    service = LoginMonitorService(db)
    return service.get_login_statistics(
        user_id=user_id,
        start_time=start_time,
        end_time=end_time
    ) 