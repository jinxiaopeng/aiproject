from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class MetricType(str, enum.Enum):
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    SYSTEM_LOAD = "system_load"
    PROCESS = "process"

class ComparisonOperator(str, enum.Enum):
    GT = ">"  # 大于
    GTE = ">="  # 大于等于
    LT = "<"  # 小于
    LTE = "<="  # 小于等于
    EQ = "=="  # 等于
    NEQ = "!="  # 不等于

class AlertRule(Base):
    """预警规则"""
    __tablename__ = "alert_rules"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    metric_type = Column(Enum(MetricType), nullable=False)
    operator = Column(Enum(ComparisonOperator), nullable=False)
    threshold = Column(Float, nullable=False)
    duration = Column(Integer, default=0)  # 持续时间（秒），0表示立即触发
    enabled = Column(Boolean, default=True)
    notify_methods = Column(JSON)  # ["email", "web", "sms"]
    cooldown = Column(Integer, default=300)  # 冷却时间（秒）
    last_triggered = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联关系
    user = relationship("User", back_populates="alert_rules")
    alerts = relationship("MonitorAlert", back_populates="rule") 