import os
from pathlib import Path

# JWT配置
SECRET_KEY = "your-secret-key"  # 在生产环境中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30000
JWT_SECRET_KEY = SECRET_KEY
JWT_ALGORITHM = ALGORITHM

# 数据库配置
DATABASE_URL = "mysql+mysqlconnector://root:jxp1210@localhost/aiproject?charset=utf8mb4"

# 项目路径配置
BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR / "static"
LOGS_DIR = BASE_DIR / "logs"

# 确保必要的目录存在
STATIC_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# 靶场配置
CHALLENGES_DIR = BASE_DIR / "challenges"