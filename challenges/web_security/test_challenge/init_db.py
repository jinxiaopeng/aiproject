"""
数据库初始化脚本
"""

import sqlite3
import os
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_db():
    """初始化数据库"""
    try:
        # 如果数据库文件已存在，先删除
        if os.path.exists('test.db'):
            os.remove('test.db')
            logger.info("Removed existing database")
        
        # 连接数据库
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        
        # 创建用户表
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        ''')
        
        # 创建敏感数据表
        c.execute('''
        CREATE TABLE IF NOT EXISTS sensitive_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
        )
        ''')
        
        # 插入测试数据
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                 ("admin", "admin123"))
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                 ("test", "test123"))
        
        # 插入flag
        c.execute("INSERT INTO sensitive_data (key, value) VALUES (?, ?)", 
                 ("flag", "flag{test_sql_injection_success}"))
        c.execute("INSERT INTO sensitive_data (key, value) VALUES (?, ?)", 
                 ("secret_key", "this_is_a_secret_key"))
        
        # 提交更改
        conn.commit()
        logger.info("Database initialized successfully")
        
        # 验证数据
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        logger.info(f"Created users: {users}")
        
        c.execute("SELECT * FROM sensitive_data")
        data = c.fetchall()
        logger.info(f"Created sensitive data: {data}")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    init_db() 