from sqlalchemy import text
from core.database import engine
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_db():
    """清理数据库中的所有表"""
    try:
        with engine.connect() as conn:
            logger.info("开始清理数据库...")
            conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            
            # 获取所有表名
            result = conn.execute(text("SHOW TABLES"))
            tables = [row[0] for row in result]
            logger.info(f"找到以下表: {tables}")
            
            # 删除所有表
            for table in tables:
                logger.info(f"删除表: {table}")
                conn.execute(text(f"DROP TABLE IF EXISTS {table}"))
            
            conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            conn.commit()
            logger.info("数据库清理完成")
    except Exception as e:
        logger.error(f"清理数据库时出错: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        clean_db()
        print("数据库清理成功")
    except Exception as e:
        print(f"数据库清理失败: {str(e)}") 