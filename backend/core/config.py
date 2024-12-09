from typing import Optional

# JWT配置
JWT_SECRET_KEY = "your-secret-key-keep-it-secret"  # 在生产环境中应该使用环境变量
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 