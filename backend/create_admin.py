from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.security import get_password_hash
from models.user import User
from core.config import settings

def create_admin():
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    
    # 创建会话
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # 检查是否已存在管理员用户
        admin = session.query(User).filter(User.username == "admin").first()
        if admin:
            print("管理员用户已存在")
            return
        
        # 创建管理员用户
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            role="USER",
            status="ACTIVE"
        )
        
        session.add(admin)
        session.commit()
        print("管理员用户创建成功")
        
    except Exception as e:
        print(f"创建管理员用户时出错: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    create_admin() 