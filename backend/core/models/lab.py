from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Lab(Base):
    __tablename__ = "labs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(Enum('web', 'system', 'network', 'crypto', 'reverse', name='lab_category'), nullable=False)
    difficulty = Column(Enum('easy', 'medium', 'hard', name='lab_difficulty'), nullable=False)
    docker_image = Column(String(255), nullable=False)
    internal_port = Column(Integer, nullable=False)
    environment = Column(JSON)
    points = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    instances = relationship("LabInstance", back_populates="lab")
    reports = relationship("LabReport", back_populates="lab")
    progress = relationship("LabProgress", back_populates="lab")

class LabInstance(Base):
    __tablename__ = "lab_instances"
    
    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("labs.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    container_id = Column(String(100), nullable=False)
    status = Column(Enum('running', 'stopped', 'completed', 'error', 'expired', name='instance_status'), nullable=False)
    port = Column(Integer, nullable=False)
    score = Column(Integer, default=0)
    completion_rate = Column(Float, default=0.0)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)

    # 关系
    lab = relationship("Lab", back_populates="instances")
    user = relationship("User", back_populates="lab_instances")
    steps = relationship("LabStep", back_populates="instance")

class LabStep(Base):
    __tablename__ = "lab_steps"
    
    id = Column(Integer, primary_key=True, index=True)
    instance_id = Column(Integer, ForeignKey("lab_instances.id", ondelete="CASCADE"))
    step_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum('pending', 'completed', 'skipped', name='step_status'), nullable=False, default='pending')
    completed_at = Column(DateTime)

    # 关系
    instance = relationship("LabInstance", back_populates="steps")

class LabReport(Base):
    __tablename__ = "lab_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    instance_id = Column(Integer, ForeignKey("lab_instances.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    findings = Column(Text)
    conclusion = Column(Text)
    attachments = Column(JSON)
    score = Column(Integer, default=0)
    feedback = Column(Text)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    instance = relationship("LabInstance")
    user = relationship("User", back_populates="lab_reports")
    lab = relationship("Lab", back_populates="reports")
    comments = relationship("ReportComment", back_populates="report")

class ReportComment(Base):
    __tablename__ = "report_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("lab_reports.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    report = relationship("LabReport", back_populates="comments")
    user = relationship("User", back_populates="report_comments")

class LabProgress(Base):
    __tablename__ = "lab_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    lab_id = Column(Integer, ForeignKey("labs.id", ondelete="CASCADE"))
    status = Column(Enum('not_started', 'in_progress', 'completed', name='progress_status'), nullable=False, default='not_started')
    score = Column(Integer, default=0)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # 关系
    user = relationship("User", back_populates="lab_progress")
    lab = relationship("Lab", back_populates="progress") 