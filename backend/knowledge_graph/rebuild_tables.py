from sqlalchemy import create_engine
from .models import Base
from .core.config import settings

def rebuild_tables():
    """重建所有数据库表"""
    print("开始重建数据库表...")
    
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    
    # 删除所有现有表
    Base.metadata.drop_all(engine)
    print("已删除现有表")
    
    # 创建新表
    Base.metadata.create_all(engine)
    print("已创建新表")
    
if __name__ == "__main__":
    rebuild_tables() 