from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Enum, Table
from sqlalchemy.orm import relationship
from . import Base
import enum

class RelationshipStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    DELETED = "deleted"

class RelationshipType(str, enum.Enum):
    PREREQUISITE = "prerequisite"        # 前置知识
    RELATED = "related"                  # 相关知识
    INCLUDES = "includes"                # 包含关系
    LEADS_TO = "leads_to"               # 导致关系
    MITIGATES = "mitigates"             # 缓解/防御关系
    EXPLOITS = "exploits"               # 利用关系
    AFFECTS = "affects"                  # 影响关系

class EntityRelationship(Base):
    """实体关系模型"""
    __tablename__ = "kg_entity_relationships"
    
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey("kg_entities.id", ondelete="CASCADE"), nullable=False)
    target_id = Column(Integer, ForeignKey("kg_entities.id", ondelete="CASCADE"), nullable=False)
    relationship_type = Column(Enum(RelationshipType), nullable=False)
    properties = Column(JSON)  # 存储关系的其他属性
    status = Column(Enum(RelationshipStatus), nullable=False, default=RelationshipStatus.ACTIVE)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    source = relationship("Entity", foreign_keys=[source_id], backref="outgoing_relationships")
    target = relationship("Entity", foreign_keys=[target_id], backref="incoming_relationships")

# 多对多关系辅助表
entity_prerequisites = Table(
    "kg_entity_prerequisites",
    Base.metadata,
    Column("entity_id", Integer, ForeignKey("kg_entities.id", ondelete="CASCADE"), primary_key=True),
    Column("prerequisite_id", Integer, ForeignKey("kg_entities.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow)
)

entity_related = Table(
    "kg_entity_related",
    Base.metadata,
    Column("entity_id", Integer, ForeignKey("kg_entities.id", ondelete="CASCADE"), primary_key=True),
    Column("related_id", Integer, ForeignKey("kg_entities.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime, nullable=False, default=datetime.utcnow)
) 