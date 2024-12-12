from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class RealtimeMonitor(Base):
    """实时监控数据"""
    __tablename__ = "realtime_monitor"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # 系统资源使用情况
    cpu_usage = Column(Float)  # CPU使用率
    memory_usage = Column(Float)  # 内存使用率
    disk_usage = Column(Float)  # 磁盘使用率
    network_in = Column(Float)  # 网络入流量 (MB/s)
    network_out = Column(Float)  # 网络出流量 (MB/s)
    
    # 系统状态
    system_load = Column(Float)  # 系统负载
    process_count = Column(Integer)  # 进程数
    
    # 时间戳
    timestamp = Column(DateTime, nullable=False, default=datetime.now)
    
    # 额外信息
    node_name = Column(String(50))  # 节点名称
    notes = Column(String(200))  # 备注信息 