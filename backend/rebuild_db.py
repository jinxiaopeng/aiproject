from core.database import engine, Base
from models.user import User
from core.security import get_password_hash
import sqlalchemy as sa
from sqlalchemy.orm import Session

def rebuild_database():
    # 删除所有表
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped successfully")
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully")
    
    # 创建管理员用户
    with Session(engine) as session:
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("jxp1210"),
            role="admin"
        )
        session.add(admin)
        session.commit()
        print("Admin user created successfully")

if __name__ == "__main__":
    rebuild_database() 