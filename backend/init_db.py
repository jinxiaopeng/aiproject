from sqlalchemy import create_engine
from core.config import DATABASE_URL
from models import Base, User
from core.security import get_password_hash

def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.drop_all(bind=engine)  # 删除所有表
    Base.metadata.create_all(bind=engine)  # 创建所有表
    
    # 创建测试用户
    from sqlalchemy.orm import Session
    with Session(engine) as session:
        admin = User(
            username="admin",
            email="admin@example.com",
            password=get_password_hash("admin123"),
            role="admin"
        )
        session.add(admin)
        session.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!") 