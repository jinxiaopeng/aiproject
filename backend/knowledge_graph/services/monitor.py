from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Optional
from ..models.monitor import MonitorSettings, MonitorAlert
from ..schemas.monitor import (
    MonitorSettingsCreate,
    MonitorSettingsUpdate,
    MonitorAlertCreate,
    MonitorAlertUpdate,
    MonitorStats
)

def get_monitor_settings(db: Session, user_id: int) -> Optional[MonitorSettings]:
    """获取用户的监控设置"""
    return db.query(MonitorSettings).filter(MonitorSettings.user_id == user_id).first()

def create_monitor_settings(db: Session, user_id: int, settings: MonitorSettingsCreate) -> MonitorSettings:
    """创建用户的监控设置"""
    db_settings = MonitorSettings(
        user_id=user_id,
        **settings.dict()
    )
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings

def update_monitor_settings(db: Session, user_id: int, settings: MonitorSettingsUpdate) -> Optional[MonitorSettings]:
    """更新用户的监控设置"""
    db_settings = get_monitor_settings(db, user_id)
    if not db_settings:
        return None
    
    for key, value in settings.dict(exclude_unset=True).items():
        setattr(db_settings, key, value)
    
    db.commit()
    db.refresh(db_settings)
    return db_settings

def get_monitor_stats(db: Session, user_id: int) -> MonitorStats:
    """获取用户的监控统计数据"""
    unhandled_alerts = db.query(
        func.count(MonitorAlert.id).filter(MonitorAlert.type == 'login_alert').label('login_alerts'),
        func.count(MonitorAlert.id).filter(MonitorAlert.type == 'operation_alert').label('operation_alerts'),
        func.count(MonitorAlert.id).filter(MonitorAlert.type == 'security_alert').label('security_alerts')
    ).filter(
        MonitorAlert.user_id == user_id,
        MonitorAlert.status == 'unread'
    ).first()

    return MonitorStats(
        login_alerts=unhandled_alerts.login_alerts,
        operation_alerts=unhandled_alerts.operation_alerts,
        security_alerts=unhandled_alerts.security_alerts
    )

def get_monitor_alerts(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    time_range: str = 'all'
) -> List[MonitorAlert]:
    """获取用户的预警记录"""
    query = db.query(MonitorAlert).filter(MonitorAlert.user_id == user_id)

    # 根据时间范围筛选
    if time_range == 'today':
        query = query.filter(func.date(MonitorAlert.created_at) == func.current_date())
    elif time_range == 'week':
        query = query.filter(
            MonitorAlert.created_at >= func.date_sub(func.current_date(), text('INTERVAL 7 DAY'))
        )
    elif time_range == 'month':
        query = query.filter(
            MonitorAlert.created_at >= func.date_sub(func.current_date(), text('INTERVAL 30 DAY'))
        )

    return query.order_by(MonitorAlert.created_at.desc()).offset(skip).limit(limit).all()

def create_monitor_alert(db: Session, alert: MonitorAlertCreate) -> MonitorAlert:
    """创建预警记录"""
    db_alert = MonitorAlert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def update_monitor_alert(
    db: Session,
    alert_id: int,
    user_id: int,
    update_data: MonitorAlertUpdate
) -> Optional[MonitorAlert]:
    """更新预警记录状态"""
    db_alert = db.query(MonitorAlert).filter(
        MonitorAlert.id == alert_id,
        MonitorAlert.user_id == user_id
    ).first()

    if not db_alert:
        return None

    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_alert, key, value)

    if update_data.status == 'handled' and not db_alert.handled_at:
        db_alert.handled_at = datetime.utcnow()

    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_total_alerts_count(db: Session, user_id: int, time_range: str = 'all') -> int:
    """获取预警记录总数"""
    query = db.query(func.count(MonitorAlert.id)).filter(MonitorAlert.user_id == user_id)

    if time_range == 'today':
        query = query.filter(func.date(MonitorAlert.created_at) == func.current_date())
    elif time_range == 'week':
        query = query.filter(
            MonitorAlert.created_at >= func.date_sub(func.current_date(), text('INTERVAL 7 DAY'))
        )
    elif time_range == 'month':
        query = query.filter(
            MonitorAlert.created_at >= func.date_sub(func.current_date(), text('INTERVAL 30 DAY'))
        )

    return query.scalar() 