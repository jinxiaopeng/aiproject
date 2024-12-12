import mysql.connector
from datetime import datetime

# MySQL 连接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'jxp1210',
    'database': 'cyberlabs'
}

def init_lab_data():
    try:
        # 连接数据库
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # 禁用外键检查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 删除现有表（如果存在）
        cursor.execute("DROP TABLE IF EXISTS lab_steps")
        cursor.execute("DROP TABLE IF EXISTS lab_instances")
        cursor.execute("DROP TABLE IF EXISTS labs")
        
        # 创建靶场表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS labs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            category VARCHAR(50) NOT NULL,
            difficulty ENUM('easy', 'medium', 'hard') NOT NULL DEFAULT 'easy',
            docker_image VARCHAR(255) NOT NULL,
            internal_port INT NOT NULL,
            environment JSON,
            points INT NOT NULL DEFAULT 100,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        # 创建靶场实例表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lab_instances (
            id INT AUTO_INCREMENT PRIMARY KEY,
            lab_id INT NOT NULL,
            user_id INT NOT NULL,
            container_id VARCHAR(100),
            status ENUM('created', 'running', 'stopped', 'completed', 'error') NOT NULL,
            port INT,
            score INT DEFAULT 0,
            completion_rate FLOAT DEFAULT 0,
            start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP NULL,
            FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        # 创建实验步骤表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lab_steps (
            id INT AUTO_INCREMENT PRIMARY KEY,
            instance_id INT NOT NULL,
            step_number INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status ENUM('pending', 'completed', 'skipped') NOT NULL DEFAULT 'pending',
            completed_at TIMESTAMP NULL,
            FOREIGN KEY (instance_id) REFERENCES lab_instances(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """)
        
        # 初始化靶场数据
        labs = [
            (
                "SQL 注入基础训练",
                "学习和实践基本的 SQL 注入技术，包括基于错误的注入、基于布尔的盲注和基于时间的盲注等。",
                "web",
                "easy",
                "webgoat/webgoat",
                8080,
                '{"WEBGOAT_PORT": "8080", "WEBGOAT_SSLENABLED": "false"}',
                100,
                True
            ),
            (
                "XSS 跨站脚本攻击",
                "学习跨站脚本攻击的各种类型，包括存储型 XSS、反射型 XSS 和 DOM-based XSS。",
                "web",
                "medium",
                "webgoat/webgoat",
                8080,
                '{"WEBGOAT_PORT": "8080", "WEBGOAT_SSLENABLED": "false"}',
                150,
                True
            ),
            (
                "CSRF 跨站请求伪造",
                "了解 CSRF 攻击的原理和防御方法，实践各种 CSRF 攻击场景。",
                "web",
                "medium",
                "webgoat/webgoat",
                8080,
                '{"WEBGOAT_PORT": "8080", "WEBGOAT_SSLENABLED": "false"}',
                150,
                True
            )
        ]
        
        # 插入新数据
        insert_query = """
        INSERT INTO labs (name, description, category, difficulty, docker_image, internal_port, environment, points, is_active)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, labs)
        
        # 启用外键检查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # 提交事务
        conn.commit()
        print("靶场数据初始化完成！")
        
    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    init_lab_data() 