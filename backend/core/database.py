import databases
import sqlalchemy
from core.config import settings

# 数据库配置
DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)

# SQLAlchemy engine
engine = sqlalchemy.create_engine(DATABASE_URL)

async def get_db():
    if not database.is_connected:
        await database.connect()
    return database 