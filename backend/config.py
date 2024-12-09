import os
import secrets
import platform

# JWT配置
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'wsirp-jwt-secret-key-please-change-in-production-environment')  # 在生产环境中使用环境变量
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'jxp1210',
    'database': 'aiproject',
    'raise_on_warnings': True
}

# 调试模式
DEBUG = True

# 文件上传配置
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

# 靶场配置
DOCKER_API_URL = "npipe:////./pipe/docker_engine" if platform.system() == "Windows" else "unix://var/run/docker.sock"
CHALLENGE_CONTAINER_PREFIX = "wsirp_challenge_"
CHALLENGE_NETWORK = "wsirp_network"
CHALLENGE_EXPIRE_MINUTES = 30

# 日志配置
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

# 创建必要的目录
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)