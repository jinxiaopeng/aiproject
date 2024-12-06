import sys
from pathlib import Path

# 添加backend目录到Python路径
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from sqlalchemy.orm import Session
from core.database import SessionLocal, engine
from models import User, Base

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
                password="admin123",  # 测试阶段使用明文密码
                role="admin",
                status="active"
            )
            db.add(admin)
            db.commit()
            print("管理员用户创建成功")
        else:
            print("管理员用户已存在")

    except Exception as e:
        print(f"初始化数据库失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 