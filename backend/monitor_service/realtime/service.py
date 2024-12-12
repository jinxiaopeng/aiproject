from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
from . import models, schemas

def create_login_event(db: Session, event: schemas.LoginMonitorCreate) -> models.LoginMonitor:
    """创建登录事件记录"""
    db_event = models.LoginMonitor(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_login_events(
    db: Session,
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.LoginMonitor]:
    """获取登录事件记录"""
    query = db.query(models.LoginMonitor)
    if user_id:
        query = query.filter(models.LoginMonitor.user_id == user_id)
    return query.order_by(models.LoginMonitor.created_at.desc()).offset(skip).limit(limit).all()

def create_operation_event(db: Session, event: schemas.OperationMonitorCreate) -> models.OperationMonitor:
    """创建操作事件记录"""
    db_event = models.OperationMonitor(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_operation_events(
    db: Session,
    user_id: Optional[int] = None,
    resource_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.OperationMonitor]:
    """获取操作事件记录"""
    query = db.query(models.OperationMonitor)
    if user_id:
        query = query.filter(models.OperationMonitor.user_id == user_id)
    if resource_type:
        query = query.filter(models.OperationMonitor.resource_type == resource_type)
    return query.order_by(models.OperationMonitor.created_at.desc()).offset(skip).limit(limit).all()

def create_security_event(db: Session, event: schemas.SecurityMonitorCreate) -> models.SecurityMonitor:
    """创建安全事件记录"""
    db_event = models.SecurityMonitor(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_security_events(
    db: Session,
    user_id: Optional[int] = None,
    severity: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.SecurityMonitor]:
    """获取安全事件记录"""
    query = db.query(models.SecurityMonitor)
    if user_id:
        query = query.filter(models.SecurityMonitor.user_id == user_id)
    if severity:
        query = query.filter(models.SecurityMonitor.severity == severity)
    return query.order_by(models.SecurityMonitor.created_at.desc()).offset(skip).limit(limit).all()

def get_recent_events_count(db: Session, hours: int = 24) -> dict:
    """获取最近一段时间内的事件统计"""
    time_threshold = datetime.utcnow() - timedelta(hours=hours)
    
    login_count = db.query(models.LoginMonitor).filter(
        models.LoginMonitor.created_at >= time_threshold
    ).count()
    
    operation_count = db.query(models.OperationMonitor).filter(
        models.OperationMonitor.created_at >= time_threshold
    ).count()
    
    security_count = db.query(models.SecurityMonitor).filter(
        models.SecurityMonitor.created_at >= time_threshold
    ).count()
    
    return {
        "login_events": login_count,
        "operation_events": operation_count,
        "security_events": security_count,
        "total": login_count + operation_count + security_count
    } 