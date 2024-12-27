from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Lab(Base):
    """靶场表"""
    __tablename__ = "practice_labs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)  # web, system, network, crypto, reverse
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard
    points = Column(Integer, default=100)
    docker_image = Column(String(255), nullable=False)
    port_mapping = Column(String(50), nullable=False)
    flag = Column(String(255))
    hints = Column(JSON)
    resource_limits = Column(JSON)  # CPU、内存等限制
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    instances = relationship("LabInstance", back_populates="lab")
    progress = relationship("LabProgress", back_populates="lab")
    flags = relationship("Flag", back_populates="lab")

class LabInstance(Base):
    """靶场实例表"""
    __tablename__ = "practice_instances"

    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("practice_labs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    container_id = Column(String(100))
    instance_url = Column(String(255))
    status = Column(String(20))  # running, stopped, completed, error
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)

    # 关联
    lab = relationship("Lab", back_populates="instances")
    user = relationship("User", back_populates="lab_instances")

class LabProgress(Base):
    """靶场进度表"""
    __tablename__ = "practice_progress"

    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("practice_labs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20))  # not_started, in_progress, completed
    score = Column(Integer, default=0)
    attempts = Column(Integer, default=0)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    lab = relationship("Lab", back_populates="progress")
    user = relationship("User", back_populates="lab_progress") 