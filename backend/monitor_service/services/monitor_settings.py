from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from ..models.monitor import MonitorSettings
from ..schemas.monitor_settings import MonitorSettingsCreate, MonitorSettingsUpdate

def get_settings(db: Session, user_id: int) -> Optional[MonitorSettings]:
    """获取用户的监控设置"""
    return db.query(MonitorSettings).filter(MonitorSettings.user_id == user_id).first()

def create_settings(db: Session, user_id: int) -> MonitorSettings:
    """创建默认的监控设置"""
    db_settings = MonitorSettings(
        user_id=user_id,
        login_alert=True,
        operation_alert=False,
        security_alert=True,
        notify_methods=["web"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings

def update_settings(
    db: Session, 
    user_id: int, 
    settings: MonitorSettingsUpdate
) -> Optional[MonitorSettings]:
    """更新监控设置"""
    db_settings = get_settings(db, user_id)
    if not db_settings:
        return None
    
    for key, value in settings.model_dump(exclude_unset=True).items():
        setattr(db_settings, key, value)
    
    db_settings.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_settings)
    return db_settings 