import mysql.connector
from pathlib import Path
import sys

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from backend.config import DB_CONFIG
from backend.core.auth import get_password_hash

def init_db():
    """初始化数据库"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    try:
        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # 删除现有表（如果存在）
        cursor.execute("DROP TABLE IF EXISTS user_sessions")
        cursor.execute("DROP TABLE IF EXISTS learning_progress")
        cursor.execute("DROP TABLE IF EXISTS lab_records")
        cursor.execute("DROP TABLE IF EXISTS knowledge_base")
        cursor.execute("DROP TABLE IF EXISTS users")
        
        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'user',
                status VARCHAR(20) NOT NULL DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """)
        
        # 创建用户会话表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                session_token VARCHAR(255) NOT NULL,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # 创建学习进度表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_progress (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                course_id INT NOT NULL,
                progress FLOAT NOT NULL DEFAULT 0,
                last_position VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        
        # 创建实验记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lab_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                lab_id INT NOT NULL,
                status VARCHAR(20) NOT NULL,
                score FLOAT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_time TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # 创建知识库表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS knowledge_base (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                category VARCHAR(50) NOT NULL,
                tags VARCHAR(255),
                difficulty INT DEFAULT 1,
                vector_embedding JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_category (category),
                INDEX idx_tags (tags)
            )
        """)
        
        # 创建测试用户
        test_users = [
            {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@example.com',
                'role': 'admin'
            },
            {
                'username': 'test',
                'password': 'test123',
                'email': 'test@example.com',
                'role': 'user'
            }
        ]
        
        for user in test_users:
            try:
                cursor.execute("""
                    INSERT INTO users (username, hashed_password, email, role)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    hashed_password = VALUES(hashed_password),
                    email = VALUES(email),
                    role = VALUES(role)
                """, (
                    user['username'],
                    get_password_hash(user['password']),
                    user['email'],
                    user['role']
                ))
            except Exception as e:
                print(f"创建用户 {user['username']} 失败: {str(e)}")
        
        conn.commit()
        print("数据库初始化完成")
        
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        raise
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_db() 