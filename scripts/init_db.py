import mysql.connector
import os
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_database():
    """初始化数据库"""
    try:
        # 读取SQL文件
        sql_file = Path(__file__).parent / 'init-db.sql'
        if not sql_file.exists():
            raise FileNotFoundError(f"SQL文件不存在: {sql_file}")
            
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
            
        # 连接MySQL
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='jxp1210',
            charset='utf8mb4'
        )
        
        cursor = conn.cursor()
        
        try:
            # 执行SQL命令
            for command in sql_commands.split(';'):
                if command.strip():
                    cursor.execute(command + ';')
            
            conn.commit()
            logger.info("数据库初始化成功")
            
        except Exception as e:
            conn.rollback()
            logger.error(f"执行SQL命令失败: {str(e)}")
            raise
            
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        init_database()
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")
        exit(1) 