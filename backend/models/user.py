from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    role = Column(String(20), default="user")  # admin, user
    status = Column(String(20), default="active")  # active, inactive, banned
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)

    # 靶场相关的关联
    lab_instances = relationship("LabInstance", back_populates="user")
    lab_progress = relationship("LabProgress", back_populates="user")
    flags = relationship("Flag", back_populates="user")

    # 关系
    challenges = relationship("UserChallenge", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "challenges": [uc.to_dict() for uc in self.challenges] if self.challenges else []
        }