from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 直接使用数据库连接URL
DATABASE_URL = "mysql+mysqlconnector://root:jxp1210@localhost/aiproject"
logger.info(f"Database URL: {DATABASE_URL}")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True
)

@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    logger.info("Database connected successfully")
    # 确保数据库存在
    try:
        with dbapi_connection.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS aiproject")
            cursor.execute("USE aiproject")
            logger.info("Database 'aiproject' selected")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")

@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    logger.info("Database connection checked out")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        logger.info("Creating new database session")
        yield db
    finally:
        logger.info("Closing database session")
        db.close() 