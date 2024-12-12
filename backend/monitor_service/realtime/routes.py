from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..core.auth import get_current_user
from . import services
from .schemas import RealtimeMonitorCreate, RealtimeMonitorResponse, RealtimeMonitorStats

router = APIRouter()

@router.post("/data", response_model=RealtimeMonitorResponse)
async def create_monitor_data(
    monitor: RealtimeMonitorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建新的监控数据记录"""
    if monitor.user_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="无权限创建其他用户的监控数据")
    return services.create_monitor_record(db, monitor)

@router.get("/data/latest", response_model=List[RealtimeMonitorResponse])
async def get_latest_monitor_data(
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取最新的监控数据记录"""
    return services.get_latest_records(db, current_user["id"], limit)

@router.get("/stats", response_model=RealtimeMonitorStats)
async def get_monitor_stats(
    hours: int = 24,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取监控统计数据"""
    return services.get_stats(db, current_user["id"], hours)

@router.delete("/cleanup")
async def cleanup_monitor_data(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """清理旧的监控数据"""
    deleted_count = services.cleanup_old_records(db, days)
    return {"message": f"成功清理{deleted_count}条旧数据"} 