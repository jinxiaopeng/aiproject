from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base

class HintUnlock(Base):
    __tablename__ = "hint_unlocks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    hint_index = Column(Integer)  # 提示的索引
    cost = Column(Integer)        # 消耗的积分
    unlock_time = Column(DateTime, server_default=func.now())

    # 关联
    user = relationship("User", back_populates="hint_unlocks")
    challenge = relationship("Challenge", back_populates="hint_unlocks") 