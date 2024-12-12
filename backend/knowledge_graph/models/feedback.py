from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from . import Base
import enum

class FeedbackType(str, enum.Enum):
    CONTENT = "content"      # 内容相关
    DIFFICULTY = "difficulty"  # 难度相关
    SUGGESTION = "suggestion"  # 建议
    BUG = "bug"             # 问题报告
    OTHER = "other"         # 其他

class FeedbackStatus(str, enum.Enum):
    PENDING = "pending"    # 待处理
    PROCESSING = "processing"  # 处理中
    RESOLVED = "resolved"  # 已解决
    REJECTED = "rejected"  # 已拒绝

class Feedback(Base):
    """用户反馈"""
    __tablename__ = "kg_feedback"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    entity_id = Column(Integer, ForeignKey("kg_entities.id", ondelete="CASCADE"), nullable=False)
    feedback_type = Column(Enum(FeedbackType), nullable=False)
    content = Column(Text, nullable=False)
    rating = Column(Integer)  # 评分 1-5
    status = Column(Enum(FeedbackStatus), nullable=False, default=FeedbackStatus.PENDING)
    admin_reply = Column(Text)  # 管理员回复
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    user = relationship("User", back_populates="feedback")
    entity = relationship("Entity", back_populates="feedback")

class FeedbackComment(Base):
    """反馈评论"""
    __tablename__ = "kg_feedback_comments"
    
    id = Column(Integer, primary_key=True)
    feedback_id = Column(Integer, ForeignKey("kg_feedback.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    feedback = relationship("Feedback", backref="comments")
    user = relationship("User", backref="feedback_comments")

class FeedbackVote(Base):
    """反馈投票"""
    __tablename__ = "kg_feedback_votes"
    
    id = Column(Integer, primary_key=True)
    feedback_id = Column(Integer, ForeignKey("kg_feedback.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    is_upvote = Column(Integer, nullable=False)  # 1: 赞同, -1: 反对
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # 关系
    feedback = relationship("Feedback", backref="votes")
    user = relationship("User", backref="feedback_votes") 