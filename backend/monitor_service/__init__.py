"""Monitor Service Package"""

from .core.config import settings
from .database import Base, engine

# 创建数据库表
Base.metadata.create_all(bind=engine) 