"""
用户挑战关系模型
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from backend.core.database import Base

class UserChallenge(Base):
    """用户挑战关系模型"""
    __tablename__ = "user_challenges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    status = Column(String(20), default="not_started")  # not_started, in_progress, completed
    progress = Column(Integer, default=0)  # 0-100
    start_time = Column(DateTime, nullable=True)
    complete_time = Column(DateTime, nullable=True)
    attempts = Column(Integer, default=0)
    last_attempt_time = Column(DateTime, nullable=True)
    hints_unlocked = Column(JSON, default=list)  # List of unlocked hint indices
    
    # 关系
    user = relationship("User", back_populates="challenges")
    challenge = relationship("Challenge", back_populates="users")

    def __repr__(self):
        return f"<UserChallenge user_id={self.user_id} challenge_id={self.challenge_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "challenge_id": self.challenge_id,
            "status": self.status,
            "progress": self.progress,
            "start_time": self.start_time,
            "complete_time": self.complete_time,
            "attempts": self.attempts,
            "last_attempt_time": self.last_attempt_time,
            "hints_unlocked": self.hints_unlocked
        } 