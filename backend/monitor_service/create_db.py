import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # 连接MySQL服务器
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="jxp1210"
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 创建数据库
            cursor.execute("CREATE DATABASE IF NOT EXISTS monitor_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("数据库 monitor_db 创建成功")
            
    except Error as e:
        print(f"连接数据库时出错: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    create_database() 