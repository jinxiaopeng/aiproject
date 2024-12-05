from sqlalchemy.orm import Session
from models import User
from core.database import get_db

def init_users(db: Session):
    """初始化用户数据"""
    users = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "hashed_password": "admin123",  # 测试阶段使用明文密码
            "role": "admin",
            "status": "active",
            "avatar": "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
        }
    ]
    
    for user_data in users:
        user = User(**user_data)
        db.add(user)
    
    try:
        db.commit()
        print("Successfully initialized user data")
    except Exception as e:
        print(f"Failed to initialize user data: {e}")
        db.rollback()

if __name__ == "__main__":
    db = next(get_db())
    init_users(db) 