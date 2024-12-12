from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from . import Base
import enum

class LearningStatus(str, enum.Enum):
    NOT_STARTED = "not_started"  # 未开始
    IN_PROGRESS = "in_progress"  # 学习中
    COMPLETED = "completed"      # 已完成
    REVIEWING = "reviewing"      # 复习中

class LearningRecord(Base):
    """学习记录"""
    __tablename__ = "kg_learning_records"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    entity_id = Column(Integer, ForeignKey("kg_entities.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(LearningStatus), nullable=False, default=LearningStatus.NOT_STARTED)
    progress = Column(Float, nullable=False, default=0.0)  # 学习进度，0-100
    score = Column(Float)  # 测试得分，可选
    notes = Column(Text)  # 学习笔记
    last_study_at = Column(DateTime)  # 最后学习时间
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="learning_records")
    entity = relationship("Entity", back_populates="learning_records")

class StudySession(Base):
    """学习会话，记录每次学习的详细情况"""
    __tablename__ = "kg_study_sessions"
    
    id = Column(Integer, primary_key=True)
    learning_record_id = Column(Integer, ForeignKey("kg_learning_records.id", ondelete="CASCADE"), nullable=False)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration = Column(Integer)  # 学习时长（分钟）
    progress_delta = Column(Float, default=0.0)  # 本次学习的进度增量
    notes = Column(Text)  # 本次学习的笔记
    
    # 关系
    learning_record = relationship("LearningRecord", backref="study_sessions")

class TestRecord(Base):
    """测试记录"""
    __tablename__ = "kg_test_records"
    
    id = Column(Integer, primary_key=True)
    learning_record_id = Column(Integer, ForeignKey("kg_learning_records.id", ondelete="CASCADE"), nullable=False)
    score = Column(Float, nullable=False)  # 测试得分
    max_score = Column(Float, nullable=False, default=100.0)  # 满分值
    test_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    answers = Column(Text)  # 答题记录，可以存储JSON格式
    
    # 关系
    learning_record = relationship("LearningRecord", backref="test_records") 