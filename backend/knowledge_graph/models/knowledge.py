from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Enum
from sqlalchemy.orm import relationship
import enum

# 导入 Base 类
from . import Base

# 枚举类型定义
class EntityStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"

class AttackStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"

class VulnerabilityStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"

class VulnerabilitySeverity(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class LearningStatus(str, enum.Enum):
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    NOT_STARTED = "not_started"

# 实体模型
class Entity(Base):
    """知识图谱实体基类"""
    __tablename__ = "kg_entities"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    entity_type = Column(String(50), nullable=False)
    description = Column(Text)
    properties = Column(JSON)
    status = Column(Enum(EntityStatus), nullable=False, default=EntityStatus.ACTIVE)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    learning_records = relationship("LearningRecord", back_populates="knowledge_point")
    feedback = relationship("Feedback", back_populates="knowledge_point")

class AttackType(Base):
    """攻击类型"""
    __tablename__ = "kg_attack_types"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    impact = Column(Text)
    mitigation = Column(Text)
    status = Column(Enum(AttackStatus), nullable=False, default=AttackStatus.ACTIVE)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class Vulnerability(Base):
    """漏洞"""
    __tablename__ = "kg_vulnerabilities"
    
    id = Column(Integer, primary_key=True)
    cve_id = Column(String(20))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    severity = Column(Enum(VulnerabilitySeverity), nullable=False, default=VulnerabilitySeverity.MEDIUM)
    affected_systems = Column(JSON)
    solution = Column(Text)
    status = Column(Enum(VulnerabilityStatus), nullable=False, default=VulnerabilityStatus.ACTIVE)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class LearningRecord(Base):
    """学习记录"""
    __tablename__ = "kg_learning_records"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    knowledge_point_id = Column(Integer, ForeignKey("kg_entities.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(LearningStatus), nullable=False, default=LearningStatus.NOT_STARTED)
    progress = Column(Integer, nullable=False, default=0)
    last_study_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    knowledge_point = relationship("Entity", back_populates="learning_records")
    user = relationship("User", back_populates="learning_records")

class Feedback(Base):
    """反馈"""
    __tablename__ = "kg_feedback"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    knowledge_point_id = Column(Integer, ForeignKey("kg_entities.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # 关系
    knowledge_point = relationship("Entity", back_populates="feedback")
    user = relationship("User", back_populates="feedback") 