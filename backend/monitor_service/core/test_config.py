from pydantic_settings import BaseSettings
from typing import List

class TestSettings(BaseSettings):
    # 测试数据库配置
    DATABASE_URL: str = "mysql+mysqlconnector://root:jxp1210@localhost/monitor_test_db"
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3017"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # JWT配置
    SECRET_KEY: str = "test-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env.test"

test_settings = TestSettings() 