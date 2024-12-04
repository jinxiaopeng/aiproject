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
    "database": os.getenv("DB_NAME", "cybersecurity"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
    "use_unicode": True,
    "connect_timeout": 10,
    "pool_name": "mypool",
    "pool_size": 5
}

# JWT配置
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-super-secret-key-here")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 日志配置
LOG_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": str(LOG_DIR / "app.log"),
    "max_size": int(os.getenv("LOG_MAX_SIZE", "10485760")),  # 10MB
    "backup_count": int(os.getenv("LOG_BACKUP_COUNT", "5"))
}

# 安全配置
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3013,http://127.0.0.1:3013").split(",")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", "100"))  # 每分钟请求次数

# Docker配置
DOCKER_CONFIG = {
    "base_url": os.getenv("DOCKER_BASE_URL", "unix://var/run/docker.sock"),
    "version": os.getenv("DOCKER_API_VERSION", "auto"),
    "timeout": int(os.getenv("DOCKER_TIMEOUT", "30")),
    "max_pool_size": int(os.getenv("DOCKER_MAX_POOL_SIZE", "10"))
}

# AI配置
AI_CONFIG = {
    "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
    "model": os.getenv("AI_MODEL", "gpt-3.5-turbo"),
    "temperature": float(os.getenv("AI_TEMPERATURE", "0.7")),
    "max_tokens": int(os.getenv("AI_MAX_TOKENS", "2000"))
}

# 靶场配置
LAB_CONFIG = {
    "max_instances_per_user": int(os.getenv("LAB_MAX_INSTANCES_PER_USER", "3")),
    "max_runtime_hours": int(os.getenv("LAB_MAX_RUNTIME_HOURS", "12")),
    "cleanup_interval_minutes": int(os.getenv("LAB_CLEANUP_INTERVAL_MINUTES", "60"))
}

# 系统配置
SYSTEM_CONFIG = {
    "debug": os.getenv("DEBUG", "True").lower() == "true",
    "host": os.getenv("HOST", "127.0.0.1"),
    "port": int(os.getenv("PORT", "3000")),
    "workers": int(os.getenv("WORKERS", "4")),
    "reload": os.getenv("RELOAD", "True").lower() == "true"
}

# 合并所有配置
CONFIG: Dict[str, Any] = {
    "database": DB_CONFIG,
    "jwt": {
        "secret_key": JWT_SECRET_KEY,
        "algorithm": JWT_ALGORITHM,
        "access_token_expire_minutes": ACCESS_TOKEN_EXPIRE_MINUTES
    },
    "log": LOG_CONFIG,
    "security": {
        "allowed_hosts": ALLOWED_HOSTS,
        "cors_origins": CORS_ORIGINS,
        "rate_limit": RATE_LIMIT
    },
    "docker": DOCKER_CONFIG,
    "ai": AI_CONFIG,
    "lab": LAB_CONFIG,
    "system": SYSTEM_CONFIG
}

# 导出常用配置
DEBUG = SYSTEM_CONFIG["debug"]
API_PREFIX = "/api"
ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
JWT_SECRET_KEY = JWT_SECRET_KEY
JWT_ALGORITHM = JWT_ALGORITHM