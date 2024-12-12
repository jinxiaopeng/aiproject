from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List, Optional
from .models import RealtimeMonitor
from .schemas import RealtimeMonitorCreate, RealtimeMonitorStats

def create_monitor_record(db: Session, monitor: RealtimeMonitorCreate) -> RealtimeMonitor:
    """创建新的监控记录"""
    db_monitor = RealtimeMonitor(**monitor.model_dump())
    db.add(db_monitor)
    db.commit()
    db.refresh(db_monitor)
    return db_monitor

def get_latest_records(db: Session, user_id: int, limit: int = 100) -> List[RealtimeMonitor]:
    """获取最新的监控记录"""
    return db.query(RealtimeMonitor)\
        .filter(RealtimeMonitor.user_id == user_id)\
        .order_by(RealtimeMonitor.timestamp.desc())\
        .limit(limit)\
        .all()

def get_stats(db: Session, user_id: int, hours: int = 24) -> RealtimeMonitorStats:
    """获取监控统计数据"""
    time_threshold = datetime.now() - timedelta(hours=hours)
    
    result = db.query(
        func.avg(RealtimeMonitor.cpu_usage).label('avg_cpu'),
        func.avg(RealtimeMonitor.memory_usage).label('avg_memory'),
        func.avg(RealtimeMonitor.disk_usage).label('avg_disk'),
        func.max(RealtimeMonitor.cpu_usage).label('max_cpu'),
        func.max(RealtimeMonitor.memory_usage).label('max_memory'),
        func.max(RealtimeMonitor.disk_usage).label('max_disk'),
        func.count(RealtimeMonitor.id).label('total')
    ).filter(
        RealtimeMonitor.user_id == user_id,
        RealtimeMonitor.timestamp >= time_threshold
    ).first()
    
    return RealtimeMonitorStats(
        avg_cpu_usage=float(result.avg_cpu or 0),
        avg_memory_usage=float(result.avg_memory or 0),
        avg_disk_usage=float(result.avg_disk or 0),
        max_cpu_usage=float(result.max_cpu or 0),
        max_memory_usage=float(result.max_memory or 0),
        max_disk_usage=float(result.max_disk or 0),
        total_records=result.total,
        time_range=f"最近{hours}小时"
    )

def cleanup_old_records(db: Session, days: int = 30) -> int:
    """清理旧的监控记录"""
    time_threshold = datetime.now() - timedelta(days=days)
    deleted = db.query(RealtimeMonitor)\
        .filter(RealtimeMonitor.timestamp < time_threshold)\
        .delete()
    db.commit()
    return deleted 