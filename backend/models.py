from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import enum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    avatar = Column(String(200))
    nickname = Column(String(50))
    bio = Column(String(500))
    role = Column(String(20), default="user")
    status = Column(String(20), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class ChallengeCategory(str, enum.Enum):
    WEB = "Web安全"
    CRYPTO = "密码学"
    REVERSE = "逆向工程"
    PWN = "二进制漏洞"
    MISC = "杂项"

class ChallengeDifficulty(str, enum.Enum):
    EASY = "简单"
    MEDIUM = "中等"
    HARD = "困难"

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    category = Column(Enum(ChallengeCategory), nullable=False)
    difficulty = Column(Enum(ChallengeDifficulty), nullable=False)
    points = Column(Integer, nullable=False)
    flag = Column(String(200), nullable=False)
    docker_image = Column(String(200))
    docker_compose = Column(String(1000))
    port_mapping = Column(String(50))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)

    # 关联
    creator = relationship("User", back_populates="created_challenges")
    submissions = relationship("ChallengeSubmission", back_populates="challenge")
    instances = relationship("ChallengeInstance", back_populates="challenge")

class ChallengeSubmission(Base):
    __tablename__ = "challenge_submissions"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    submitted_flag = Column(String(200), nullable=False)
    is_correct = Column(Boolean, default=False)
    points_awarded = Column(Integer, default=0)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    # 关联
    challenge = relationship("Challenge", back_populates="submissions")
    user = relationship("User", back_populates="challenge_submissions")

class ChallengeInstance(Base):
    __tablename__ = "challenge_instances"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    container_id = Column(String(100), nullable=False)
    instance_url = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    # 关联
    challenge = relationship("Challenge", back_populates="instances")
    user = relationship("User", back_populates="challenge_instances")

# 添加用户关联
User.created_challenges = relationship("Challenge", back_populates="creator")
User.challenge_submissions = relationship("ChallengeSubmission", back_populates="user")
User.challenge_instances = relationship("ChallengeInstance", back_populates="user") 