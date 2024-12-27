from backend.core.database import SessionLocal

def check_user():
    db = SessionLocal()
    try:
        result = db.execute("SELECT * FROM users WHERE username = 'admin'").first()
        if result:
            print(f"用户ID: {result[0]}")
            print(f"用户名: {result[1]}")
            print(f"邮箱: {result[2]}")
            print(f"密码哈希: {result[3]}")
            print(f"角色: {result[4]}")
            print(f"状态: {result[5]}")
        else:
            print("未找到admin用户")
    except Exception as e:
        print(f"查询失败: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_user() 