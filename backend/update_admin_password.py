from sqlalchemy.orm import Session
from backend.core.database import SessionLocal
from backend.core.security import get_password_hash
from backend.models.user import User

def update_admin_password():
    db = SessionLocal()
    try:
        # 查找管理员用户
        admin = db.query(User).filter(User.username == "admin").first()
        if admin:
            # 更新密码
            admin.hashed_password = get_password_hash("jxp1210")
            db.commit()
            print("管理员密码已更新")
        else:
            print("未找到管理员用户")
    except Exception as e:
        print(f"更新密码失败: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_admin_password() 