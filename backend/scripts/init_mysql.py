"""
初始化MySQL数据库
"""

import mysql.connector
from mysql.connector import Error
import logging

logger = logging.getLogger(__name__)

def init_mysql():
    """初始化系统主数据库和靶场数据库"""
    try:
        # 连接MySQL服务器
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="jxp1210"
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # 1. 创建系统主数据库
            logger.info("Creating main database...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS aiproject")
            cursor.execute("USE aiproject")
            
            # 创建用户靶场档案表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_ctf_profiles (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL UNIQUE,
                points INT DEFAULT 0,
                rank INT DEFAULT 0,
                last_challenge_time TIMESTAMP NULL,
                completed_challenges INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)
            
            # 创建靶场表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenges (
                id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(100) NOT NULL,
                description TEXT,
                category VARCHAR(50) NOT NULL,
                difficulty ENUM('easy', 'medium', 'hard') NOT NULL,
                points INT NOT NULL DEFAULT 0,
                flag VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT true,
                process_config JSON,
                resource_limits JSON,
                timeout_config JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """)
            
            # 创建用户技能表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_skills (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                skill_type VARCHAR(50) NOT NULL,
                skill_level INT DEFAULT 0,
                skill_points INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)
            
            # 创建学习路径表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_paths (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                challenge_id INT NOT NULL,
                status ENUM('not_started','in_progress','completed') DEFAULT 'not_started',
                start_time TIMESTAMP NULL,
                complete_time TIMESTAMP NULL,
                attempts INT DEFAULT 0,
                hints_used INT DEFAULT 0,
                score INT DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (challenge_id) REFERENCES challenges(id)
            )
            """)
            
            # 创建提交记录表
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT NOT NULL,
                challenge_id INT NOT NULL,
                submitted_flag VARCHAR(255) NOT NULL,
                is_correct BOOLEAN NOT NULL,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (challenge_id) REFERENCES challenges(id)
            )
            """)
            
            # 2. 创建靶场数据库
            logger.info("Creating challenge databases...")
            
            # SQL注入靶场
            cursor.execute("CREATE DATABASE IF NOT EXISTS ctf_challenge_1")
            cursor.execute("CREATE USER IF NOT EXISTS 'ctf_user_1'@'localhost' IDENTIFIED BY 'ctf_pass_1'")
            cursor.execute("GRANT ALL PRIVILEGES ON ctf_challenge_1.* TO 'ctf_user_1'@'localhost'")
            
            # XSS靶场
            cursor.execute("CREATE DATABASE IF NOT EXISTS ctf_challenge_2")
            cursor.execute("CREATE USER IF NOT EXISTS 'ctf_user_2'@'localhost' IDENTIFIED BY 'ctf_pass_2'")
            cursor.execute("GRANT ALL PRIVILEGES ON ctf_challenge_2.* TO 'ctf_user_2'@'localhost'")
            
            # 文件上传靶场
            cursor.execute("CREATE DATABASE IF NOT EXISTS ctf_challenge_3")
            cursor.execute("CREATE USER IF NOT EXISTS 'ctf_user_3'@'localhost' IDENTIFIED BY 'ctf_pass_3'")
            cursor.execute("GRANT ALL PRIVILEGES ON ctf_challenge_3.* TO 'ctf_user_3'@'localhost'")
            
            # 刷新权限
            cursor.execute("FLUSH PRIVILEGES")
            
            logger.info("Successfully initialized databases and users")
            
    except Error as e:
        logger.error(f"Error initializing MySQL: {str(e)}")
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
    init_mysql() 