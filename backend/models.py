from core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))  # 存储明文密码，仅用于测试
    role = Column(String(20), default="user")  # admin, user
    status = Column(String(20), default="active")  # active, disabled
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 