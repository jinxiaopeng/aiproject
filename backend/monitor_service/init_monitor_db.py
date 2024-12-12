import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

from sqlalchemy import create_engine, text
from monitor_service.core.config import settings

def init_monitor_db():
    """初始化监控数据库"""
    # 创建到MySQL的连接
    engine = create_engine(settings.DATABASE_URL.replace("/monitor_db", ""))
    
    try:
        # 创建数据库（如果不存在）
        with engine.connect() as conn:
            conn.execute(text("CREATE DATABASE IF NOT EXISTS monitor_db"))
            print("数据库 monitor_db 创建成功或已存在")
        
        # 运行数据库迁移
        os.chdir(str(current_dir))
        os.system("alembic upgrade head")
        print("数据库迁移完成")
        
    except Exception as e:
        print(f"初始化数据库失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    init_monitor_db() 