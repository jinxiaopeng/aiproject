from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class RealtimeMonitorBase(BaseModel):
    """实时监控数据基础模型"""
    cpu_usage: Optional[float] = None
    memory_usage: Optional[float] = None
    disk_usage: Optional[float] = None
    network_in: Optional[float] = None
    network_out: Optional[float] = None
    system_load: Optional[float] = None
    process_count: Optional[int] = None
    node_name: Optional[str] = None
    notes: Optional[str] = None

class RealtimeMonitorCreate(RealtimeMonitorBase):
    """创建实时监控数据的请求模型"""
    user_id: int

class RealtimeMonitorResponse(RealtimeMonitorBase):
    """实时监控数据的响应模型"""
    id: int
    user_id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class RealtimeMonitorStats(BaseModel):
    """实时监控统计数据"""
    avg_cpu_usage: float
    avg_memory_usage: float
    avg_disk_usage: float
    max_cpu_usage: float
    max_memory_usage: float
    max_disk_usage: float
    total_records: int
    time_range: str 