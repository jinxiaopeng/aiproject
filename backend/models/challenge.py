"""
靶场模型定义
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.core.database import Base
from backend.models.challenge_enums import ChallengeCategory, ChallengeDifficulty

class Challenge(Base):
    """靶场模型"""
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    difficulty = Column(String(50), nullable=False)
    points = Column(Integer, nullable=False)
    flag = Column(String(255), nullable=False)
    
    # 训练相关
    objectives = Column(JSON, nullable=True)  # List[str]
    prerequisites = Column(JSON, nullable=True)  # List[Dict]
    environment = Column(JSON, nullable=True)  # Dict
    notices = Column(JSON, nullable=True)  # List[str]
    steps = Column(JSON, nullable=True)  # List[Dict]
    hints = Column(JSON, nullable=True)  # List[str]
    
    # 配置相关
    process_config = Column(JSON, nullable=True)  # Dict
    resource_limits = Column(JSON, nullable=True)  # Dict
    timeout_config = Column(JSON, nullable=True)  # Dict
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    users = relationship("UserChallenge", back_populates="challenge")

    def __repr__(self):
        return f"<Challenge {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "difficulty": self.difficulty,
            "points": self.points,
            "objectives": self.objectives,
            "prerequisites": self.prerequisites,
            "environment": self.environment,
            "notices": self.notices,
            "steps": self.steps,
            "hints": self.hints,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }