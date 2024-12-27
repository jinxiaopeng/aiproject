from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from backend.core.database import Base

class Flag(Base):
    """Flag提交记录表"""
    __tablename__ = "flags"

    id = Column(Integer, primary_key=True)
    lab_id = Column(Integer, ForeignKey("practice_labs.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    flag_value = Column(String(255))
    is_correct = Column(Boolean, default=False)
    submitted_at = Column(DateTime, default=datetime.now)

    # 关联
    lab = relationship("Lab", back_populates="flags")
    user = relationship("User", back_populates="flags") 