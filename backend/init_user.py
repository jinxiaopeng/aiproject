from sqlalchemy.orm import Session
from models.user import User
from core.database import get_db, engine, Base
from core.security import get_password_hash
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """创建数据库表"""
    try:
        logger.info("开始创建数据库表...")
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"创建数据库表失败: {str(e)}")
        raise

def init_users(db: Session):
    """初始化用户数据"""
    try:
        # 检查是否已存在用户
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            logger.info("管理员用户已存在")
            return

        logger.info("开始创建管理员用户...")
        user_data = {
            "username": "admin",
            "email": "admin@example.com",
            "password": get_password_hash("admin123"),
            "role": "admin",
            "status": "active"
        }
        
        user = User(**user_data)
        db.add(user)
        db.commit()
        logger.info("管理员用户创建成功")
        
    except Exception as e:
        logger.error(f"初始化用户数据失败: {str(e)}")
        db.rollback()
        raise

if __name__ == "__main__":
    try:
        init_db()
        db = next(get_db())
        init_users(db)
        print("用户初始化成功")
    except Exception as e:
        print(f"用户初始化失败: {str(e)}") 