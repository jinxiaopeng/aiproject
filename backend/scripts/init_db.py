import sys
from pathlib import Path

# 添加backend目录到Python路径
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from sqlalchemy.orm import Session
from core.database import SessionLocal, engine
from models import User, Base
from core.security import get_password_hash

def init_db():
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 检查是否已存在管理员用户
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # 创建管理员用户
            admin = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),  # 使用安全的密码哈希
                role="admin",
                status="active",
                nickname="管理员",
                bio="系统管理员",
                avatar="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
            )
            db.add(admin)
            db.commit()
            print("管理员用户创建成功")
        else:
            print("管理员用户已存在")
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 