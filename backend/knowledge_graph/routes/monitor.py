from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.deps import get_db, get_current_user
from ..services import monitor as monitor_service
from ..schemas.monitor import (
    MonitorSettings,
    MonitorSettingsCreate,
    MonitorSettingsUpdate,
    MonitorAlert,
    MonitorAlertCreate,
    MonitorAlertUpdate,
    MonitorStats
)
from ..models.user import User

router = APIRouter(prefix="/monitor", tags=["monitor"])

@router.get("/settings", response_model=MonitorSettings)
async def get_monitor_settings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取监控设置"""
    settings = monitor_service.get_monitor_settings(db, current_user.id)
    if not settings:
        # 如果没有设置，创建默认设置
        settings = monitor_service.create_monitor_settings(
            db,
            current_user.id,
            MonitorSettingsCreate()
        )
    return settings

@router.put("/settings", response_model=MonitorSettings)
async def update_monitor_settings(
    settings: MonitorSettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新监控设置"""
    updated_settings = monitor_service.update_monitor_settings(db, current_user.id, settings)
    if not updated_settings:
        raise HTTPException(status_code=404, detail="监控设置不存在")
    return updated_settings

@router.get("/stats", response_model=MonitorStats)
async def get_monitor_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取监控统计数据"""
    return monitor_service.get_monitor_stats(db, current_user.id)

@router.get("/alerts", response_model=List[MonitorAlert])
async def get_monitor_alerts(
    skip: int = 0,
    limit: int = 10,
    time_range: str = 'all',
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取预警记录列表"""
    alerts = monitor_service.get_monitor_alerts(
        db,
        current_user.id,
        skip=skip,
        limit=limit,
        time_range=time_range
    )
    return alerts

@router.get("/alerts/count")
async def get_alerts_count(
    time_range: str = 'all',
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取预警记录总数"""
    total = monitor_service.get_total_alerts_count(db, current_user.id, time_range)
    return {"total": total}

@router.put("/alerts/{alert_id}", response_model=MonitorAlert)
async def update_alert_status(
    alert_id: int,
    update_data: MonitorAlertUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新预警记录状态"""
    updated_alert = monitor_service.update_monitor_alert(
        db,
        alert_id,
        current_user.id,
        update_data
    )
    if not updated_alert:
        raise HTTPException(status_code=404, detail="预警记录不存在")
    return updated_alert 