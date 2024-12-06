from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
import enum

class ChallengeCategory(str, enum.Enum):
    WEB = "WEB"
    CRYPTO = "CRYPTO"
    REVERSE = "REVERSE"
    PWN = "PWN"
    MISC = "MISC"

class ChallengeDifficulty(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, index=True)
    description = Column(String(1000))
    category = Column(Enum(ChallengeCategory))
    difficulty = Column(Enum(ChallengeDifficulty))
    points = Column(Integer, default=0)
    flag = Column(String(255))
    docker_image = Column(String(255))
    port_mapping = Column(String(20))
    created_by = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联
    creator = relationship("User", back_populates="challenges")
    instances = relationship("ChallengeInstance", back_populates="challenge")
    submissions = relationship("ChallengeSubmission", back_populates="challenge")

class ChallengeInstance(Base):
    __tablename__ = "challenge_instances"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    container_id = Column(String(64))
    instance_url = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    # 关联
    challenge = relationship("Challenge", back_populates="instances")
    user = relationship("User", back_populates="challenge_instances")

class ChallengeSubmission(Base):
    __tablename__ = "challenge_submissions"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    submitted_flag = Column(String(255))
    is_correct = Column(Boolean)
    points_awarded = Column(Integer, default=0)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    # 关联
    challenge = relationship("Challenge", back_populates="submissions")
    user = relationship("User", back_populates="challenge_submissions") 