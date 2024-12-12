import sys
from pathlib import Path

# 添加项目根目录到Python路径
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from monitor_service.database import Base, engine
from monitor_service.models.monitor import MonitorSettings, MonitorAlert

def init_db():
    """初始化数据库表"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db() 