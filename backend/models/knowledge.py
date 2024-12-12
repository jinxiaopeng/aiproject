from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from .base import Base

# 知识点和前置知识点的关联表
node_prerequisites = Table(
    'node_prerequisites',
    Base.metadata,
    Column('node_id', Integer, ForeignKey('knowledge_nodes.id'), primary_key=True),
    Column('prerequisite_id', Integer, ForeignKey('knowledge_nodes.id'), primary_key=True)
)

class KnowledgeNode(Base):
    """知识点"""
    __tablename__ = "knowledge_nodes"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    difficulty = Column(String(20), nullable=False)
    value = Column(Float, nullable=False, default=1.0)
    description = Column(String(500))
    key_points = Column(JSON)  # 存储关键点列表
    resources = Column(JSON)   # 存储资源列表
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    prerequisites = relationship(
        "KnowledgeNode",
        secondary=node_prerequisites,
        primaryjoin=id==node_prerequisites.c.node_id,
        secondaryjoin=id==node_prerequisites.c.prerequisite_id,
        backref="dependent_nodes"
    ) 