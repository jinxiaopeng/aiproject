from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.monitor import MonitorSettings, MonitorAlert, AlertType, AlertLevel, AlertStatus
from ..schemas.monitor import (
    MonitorSettingsCreate,
    MonitorSettingsUpdate,
    MonitorAlertCreate,
    MonitorAlertUpdate
)

router = APIRouter()

@router.get("/settings")
async def get_monitor_settings(
    user_id: int,
    db: Session = Depends(get_db)
):
    """获取监控设置"""
    settings = db.query(MonitorSettings).filter(
        MonitorSettings.user_id == user_id
    ).first()
    
    if not settings:
        settings = MonitorSettings(
            user_id=user_id,
            notify_methods=["email", "web"]
        )
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return settings

@router.put("/settings")
async def update_monitor_settings(
    user_id: int,
    settings_update: MonitorSettingsUpdate,
    db: Session = Depends(get_db)
):
    """更新监控设置"""
    settings = db.query(MonitorSettings).filter(
        MonitorSettings.user_id == user_id
    ).first()
    
    if not settings:
        raise HTTPException(status_code=404, detail="监控设置不存在")
    
    for key, value in settings_update.dict(exclude_unset=True).items():
        setattr(settings, key, value)
    
    db.commit()
    db.refresh(settings)
    return settings

@router.get("/alerts")
async def get_alerts(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """获取预警记录"""
    alerts = db.query(MonitorAlert).filter(
        MonitorAlert.user_id == user_id
    ).offset(skip).limit(limit).all()
    
    return alerts

@router.post("/alerts")
async def create_alert(
    alert: MonitorAlertCreate,
    db: Session = Depends(get_db)
):
    """创建预警记录"""
    db_alert = MonitorAlert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.put("/alerts/{alert_id}")
async def update_alert(
    alert_id: int,
    alert_update: MonitorAlertUpdate,
    db: Session = Depends(get_db)
):
    """更新预警记录"""
    alert = db.query(MonitorAlert).filter(
        MonitorAlert.id == alert_id
    ).first()
    
    if not alert:
        raise HTTPException(status_code=404, detail="预警记录不存在")
    
    for key, value in alert_update.dict(exclude_unset=True).items():
        setattr(alert, key, value)
    
    db.commit()
    db.refresh(alert)
    return alert 