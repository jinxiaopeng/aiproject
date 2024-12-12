from sqlalchemy import create_engine, text
from backend.knowledge_graph.core.config import settings
from urllib.parse import urlparse

def get_database_name(url):
    """从数据库 URL 中提取数据库名称"""
    parsed = urlparse(url)
    path = parsed.path
    if path.startswith('/'):
        path = path[1:]
    return path

def clean_database():
    """清理所有表"""
    print("开始清理数据库...")
    
    # 创建数据库引擎
    engine = create_engine(settings.DATABASE_URL)
    database_name = get_database_name(settings.DATABASE_URL)
    
    # 获取所有表名
    with engine.connect() as connection:
        # 禁用外键检查
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        
        try:
            # 获取所有表名
            result = connection.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = :schema AND table_type = 'BASE TABLE'"),
                {"schema": database_name}
            )
            tables = [row[0] for row in result]
            
            # 删除所有表
            for table in tables:
                print(f"删除表: {table}")
                connection.execute(text(f"DROP TABLE IF EXISTS {table}"))
            
            # 删除所有枚举类型
            result = connection.execute(text(
                "SELECT DISTINCT column_type FROM information_schema.columns "
                "WHERE table_schema = :schema AND column_type LIKE 'enum%'"),
                {"schema": database_name}
            )
            enums = [row[0] for row in result]
            
            for enum in enums:
                enum_name = enum.split('(')[0].strip()
                print(f"删除枚举类型: {enum_name}")
                connection.execute(text(f"DROP TYPE IF EXISTS {enum_name}"))
            
            connection.commit()
            print("数据库清理完成")
            
        finally:
            # 重新启用外键检查
            connection.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

if __name__ == "__main__":
    clean_database()