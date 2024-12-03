import os
import platform
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any

# 加载环境变量
load_dotenv()

# 基础路径配置
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
LOG_DIR = BASE_DIR / 'logs'
TEMP_DIR = BASE_DIR / 'temp'
UPLOAD_DIR = DATA_DIR / 'uploads'

# 确保必要的目录存在
for directory in [DATA_DIR, LOG_DIR, TEMP_DIR, UPLOAD_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# 数据库配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "jxp1210"),
    "database": os.getenv("DB_NAME", "wsirp_db"),
    "port": int(os.getenv("DB_PORT", "3306"))
}

# JWT配置
JWT_CONFIG = {
    "jwt_secret_key": os.getenv("JWT_SECRET_KEY", "your-secret-key-here-make-it-at-least-32-chars-long"),
    "jwt_algorithm": os.getenv("JWT_ALGORITHM", "HS256"),
    "access_token_expire_minutes": int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
}

# 应用配置
APP_CONFIG = {
    "debug": os.getenv("DEBUG", "True").lower() == "true",
    "host": os.getenv("HOST", "0.0.0.0"),
    "port": int(os.getenv("PORT", "8000")),
    "workers": int(os.getenv("WORKERS", "4")),
    "reload": os.getenv("RELOAD", "True").lower() == "true"
}

# 日志配置
LOG_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": str(LOG_DIR / "app.log"),
    "max_size": int(os.getenv("LOG_MAX_SIZE", "10485760")),  # 10MB
    "backup_count": int(os.getenv("LOG_BACKUP_COUNT", "5"))
}

# 安全配置
SECURITY_CONFIG = {
    "allowed_hosts": os.getenv("ALLOWED_HOSTS", "*").split(","),
    "cors_origins": os.getenv("CORS_ORIGINS", "*").split(","),
    "rate_limit": int(os.getenv("RATE_LIMIT", "100")),
    "ssl_redirect": os.getenv("SSL_REDIRECT", "False").lower() == "true"
}

# 合并所有配置
CONFIG: Dict[str, Any] = {
    "database": DB_CONFIG,
    "jwt": JWT_CONFIG,
    "app": APP_CONFIG,
    "log": LOG_CONFIG,
    "security": SECURITY_CONFIG
}

# 导出常用配置
DEBUG = APP_CONFIG["debug"]
API_PREFIX = "/api"
ACCESS_TOKEN_EXPIRE_MINUTES = JWT_CONFIG["access_token_expire_minutes"]
JWT_SECRET_KEY = JWT_CONFIG["jwt_secret_key"]
JWT_ALGORITHM = JWT_CONFIG["jwt_algorithm"]