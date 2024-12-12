from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # 数据库配置
    DATABASE_URL: str = "mysql+mysqlconnector://root:jxp1210@localhost/monitor_db"
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3017"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 邮件服务配置
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "your-email@gmail.com"
    SMTP_PASSWORD: str = "your-app-password"
    SENDER_EMAIL: str = "your-email@gmail.com"
    
    # 短信服务配置
    SMS_API_KEY: str = "your-sms-api-key"
    SMS_API_SECRET: str = "your-sms-api-secret"
    SMS_SIGN_NAME: str = "your-sign-name"
    
    # 监控配置
    DEFAULT_MONITOR_INTERVAL: int = 60  # 默认监控间隔（秒）
    MAX_MONITOR_HISTORY: int = 7  # 监控数据保留天数
    
    # 预警配置
    DEFAULT_ALERT_COOLDOWN: int = 300  # 默认预警冷却时间（秒）
    MAX_ALERTS_PER_DAY: int = 100  # 每天最大预警次数
    
    class Config:
        env_file = ".env"

settings = Settings() 