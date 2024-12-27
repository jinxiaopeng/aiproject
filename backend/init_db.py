from sqlalchemy.orm import Session
from backend.core.database import SessionLocal, Base, engine
from backend.core.security import get_password_hash
from backend.models.user import User
from datetime import datetime

def init_database():
    # 创建所有表
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
                hashed_password=get_password_hash("jxp1210"),
                role="admin",
                status="active",
                created_at=datetime.now()
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
    init_database() 