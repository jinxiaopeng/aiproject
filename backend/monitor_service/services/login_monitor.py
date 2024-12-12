from datetime import datetime
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.monitor import LoginMonitor, LoginEventType
from ..schemas.monitor import LoginMonitorCreate

class LoginMonitorService:
    def __init__(self, db: Session):
        self.db = db

    def create_login_event(self, event: LoginMonitorCreate) -> LoginMonitor:
        """创建登录事件记录"""
        db_event = LoginMonitor(**event.dict())
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def get_login_events(
        self,
        user_id: Optional[int] = None,
        event_type: Optional[LoginEventType] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[LoginMonitor]:
        """获取登录事件记录"""
        query = self.db.query(LoginMonitor)
        
        if user_id is not None:
            query = query.filter(LoginMonitor.user_id == user_id)
        if event_type is not None:
            query = query.filter(LoginMonitor.event_type == event_type)
        if start_time is not None:
            query = query.filter(LoginMonitor.created_at >= start_time)
        if end_time is not None:
            query = query.filter(LoginMonitor.created_at <= end_time)
            
        return query.order_by(LoginMonitor.created_at.desc()).offset(skip).limit(limit).all()

    def get_failed_login_attempts(
        self,
        user_id: int,
        minutes: int = 30
    ) -> int:
        """获取指定时间内的失败登录次数"""
        cutoff_time = datetime.utcnow().subtract(minutes=minutes)
        return self.db.query(LoginMonitor).filter(
            LoginMonitor.user_id == user_id,
            LoginMonitor.event_type == LoginEventType.FAILED,
            LoginMonitor.created_at >= cutoff_time
        ).count()

    def get_login_statistics(
        self,
        user_id: Optional[int] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """获取登录统计信息"""
        query = self.db.query(LoginMonitor)
        
        if user_id is not None:
            query = query.filter(LoginMonitor.user_id == user_id)
        if start_time is not None:
            query = query.filter(LoginMonitor.created_at >= start_time)
        if end_time is not None:
            query = query.filter(LoginMonitor.created_at <= end_time)
            
        total_events = query.count()
        success_events = query.filter(LoginMonitor.event_type == LoginEventType.SUCCESS).count()
        failed_events = query.filter(LoginMonitor.event_type == LoginEventType.FAILED).count()
        
        return {
            "total_events": total_events,
            "success_events": success_events,
            "failed_events": failed_events,
            "success_rate": (success_events / total_events * 100) if total_events > 0 else 0
        } 