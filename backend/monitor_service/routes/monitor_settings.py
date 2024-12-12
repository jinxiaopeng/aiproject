from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..services import monitor_settings
from ..schemas.monitor_settings import MonitorSettingsResponse, MonitorSettingsUpdate
from ..core.auth import get_current_user

router = APIRouter()

@router.get("", response_model=MonitorSettingsResponse)
async def get_monitor_settings(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取当前用户的监控设置"""
    settings = monitor_settings.get_settings(db, current_user["id"])
    if not settings:
        settings = monitor_settings.create_settings(db, current_user["id"])
    return settings

@router.put("", response_model=MonitorSettingsResponse)
async def update_monitor_settings(
    settings_update: MonitorSettingsUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新当前用户的监控设置"""
    updated_settings = monitor_settings.update_settings(
        db, 
        current_user["id"], 
        settings_update
    )
    if not updated_settings:
        raise HTTPException(status_code=404, detail="监控设置不存在")
    return updated_settings 