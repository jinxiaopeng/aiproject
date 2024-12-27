"""
XSS靶场的数据库初始化脚本
"""

import mysql.connector
from mysql.connector import Error
import logging

logger = logging.getLogger(__name__)

def init_db():
    """初始化XSS靶场的数据库"""
    try:
        # 使用root用户连接数据库
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="jxp1210"
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # 创建数据库
            cursor.execute("DROP DATABASE IF EXISTS ctf_challenge_2")
            cursor.execute("CREATE DATABASE ctf_challenge_2 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute("USE ctf_challenge_2")
            
            # 创建用户表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenge_users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # 创建帖子表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenge_posts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                content TEXT,
                author_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # 创建评论表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenge_comments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                content TEXT,
                post_id INT,
                author_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # 插入示例数据
            cursor.execute("INSERT INTO challenge_users (username, password, email) VALUES (%s, %s, %s)",
                         ("admin", "admin123", "admin@test.com"))
            cursor.execute("INSERT INTO challenge_users (username, password, email) VALUES (%s, %s, %s)",
                         ("test", "test123", "test@test.com"))
            
            cursor.execute("INSERT INTO challenge_posts (title, content, author_id) VALUES (%s, %s, %s)",
                         ("Welcome", "Welcome to our forum!", 1))
            cursor.execute("INSERT INTO challenge_posts (title, content, author_id) VALUES (%s, %s, %s)",
                         ("Share your thoughts", "Feel free to comment below", 1))
            
            cursor.execute("INSERT INTO challenge_comments (content, post_id, author_id) VALUES (%s, %s, %s)",
                         ("Great forum!", 1, 2))
            
            conn.commit()
            logger.info("Successfully initialized XSS challenge database")
            
    except Error as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    init_db() 