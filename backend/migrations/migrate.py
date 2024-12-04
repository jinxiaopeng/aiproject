import os
import sys
from pathlib import Path
import mysql.connector
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from config import CONFIG

def get_db_connection():
    """获取数据库连接"""
    return mysql.connector.connect(**CONFIG['database'])

def execute_migration(cursor, sql_file):
    """执行迁移文件中的SQL语句"""
    print(f"执行迁移文件: {sql_file}")
    
    # 读取SQL文件内容
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 分割SQL语句
    statements = sql_content.split(';')
    
    # 执行每个SQL语句
    for statement in statements:
        if statement.strip():
            try:
                cursor.execute(statement.strip())
                print(f"SQL执行成功: {statement[:100]}...")
            except Exception as e:
                print(f"SQL执行失败: {str(e)}")
                print(f"问题SQL: {statement}")
                raise

def create_migrations_table(cursor):
    """创建迁移记录表"""
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id INT PRIMARY KEY AUTO_INCREMENT,
            migration_file VARCHAR(255) NOT NULL,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

def get_executed_migrations(cursor):
    """获取已执行的迁移记录"""
    cursor.execute("SELECT migration_file FROM migrations")
    return {row[0] for row in cursor.fetchall()}

def record_migration(cursor, migration_file):
    """记录迁移执行"""
    cursor.execute(
        "INSERT INTO migrations (migration_file) VALUES (%s)",
        (migration_file,)
    )

def main():
    """主函数"""
    try:
        # 获取数据库连接
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 创建迁移记录表
        create_migrations_table(cursor)
        
        # 获取已执行的迁移
        executed_migrations = get_executed_migrations(cursor)
        
        # 获取迁移文件列表
        migrations_dir = Path(__file__).parent
        migration_files = sorted([
            f for f in os.listdir(migrations_dir)
            if f.endswith('.sql')
        ])
        
        # 执行未执行的迁移
        for migration_file in migration_files:
            if migration_file not in executed_migrations:
                # 执行迁移
                execute_migration(
                    cursor,
                    os.path.join(migrations_dir, migration_file)
                )
                
                # 记录迁移
                record_migration(cursor, migration_file)
                
                # 提交事务
                conn.commit()
                
                print(f"迁移完成: {migration_file}")
        
        print("所有迁移执行完成")
        
    except Exception as e:
        print(f"迁移失败: {str(e)}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main() 