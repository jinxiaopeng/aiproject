import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).resolve().parent
monitor_service_dir = current_dir.parent
backend_dir = monitor_service_dir.parent
sys.path.append(str(backend_dir))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, relationship
from monitor_service.core.test_config import test_settings
from monitor_service.database import Base
from monitor_service.main import app
from monitor_service.database import get_db
from datetime import datetime

# 使用测试数据库URL
TEST_DATABASE_URL = test_settings.DATABASE_URL

# 创建测试数据库引擎
engine = create_engine(TEST_DATABASE_URL)

# 创建测试会话工厂
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建users表
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关联关系
    alert_rules = relationship("AlertRule", back_populates="user", cascade="all, delete-orphan")

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """设置测试数据库"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # 创建测试用户
    session = TestingSessionLocal()
    test_user = User(
        username="test_user",
        email="test@example.com",
        hashed_password="test_password",
        is_active=True
    )
    session.add(test_user)
    session.commit()
    session.close()
    
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    """创建数据库会话"""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(db):
    """创建测试客户端"""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear() 