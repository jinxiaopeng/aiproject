import os
import mysql.connector
from pathlib import Path

# 获取当前脚本所在目录
script_dir = Path(__file__).parent
sql_file = script_dir / 'init_db.sql'

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "jxp1210",
    "port": 3306
}

def init_database():
    """初始化数据库"""
    try:
        # 连接MySQL服务器
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("开始初始化数据库...")
        
        # 读取SQL文件
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
        
        # 执行SQL命令
        for command in sql_commands.split(';'):
            command = command.strip()
            if command:
                cursor.execute(command)
                conn.commit()
        
        print("数据库初始化完成！")
        
        # 验证数据
        cursor.execute("USE cybersecurity")
        
        # 检查用户表
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"用户表中有 {user_count} 条记录")
        
        # 检查靶场表
        cursor.execute("SELECT COUNT(*) FROM labs")
        lab_count = cursor.fetchone()[0]
        print(f"靶场表中有 {lab_count} 条记录")
        
    except mysql.connector.Error as err:
        print(f"数据库错误: {err}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    init_database() 