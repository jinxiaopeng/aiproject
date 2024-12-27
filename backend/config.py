from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 主数据库配置
    DATABASE_URL: str = "mysql+mysqlconnector://root:jxp1210@localhost/aiproject"
    
    # 靶场数据库配置
    CTF_CHALLENGE_1_URL: str = "mysql+mysqlconnector://ctf_user_1:ctf_pass_1@localhost/ctf_challenge_1"
    CTF_CHALLENGE_2_URL: str = "mysql+mysqlconnector://ctf_user_2:ctf_pass_2@localhost/ctf_challenge_2"
    CTF_CHALLENGE_3_URL: str = "mysql+mysqlconnector://ctf_user_3:ctf_pass_3@localhost/ctf_challenge_3"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"  # 在生产环境中应该使用更安全的密钥
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 挑战配置
    CHALLENGES_BASE_PATH: str = "challenges"
    MAX_CONTAINER_COUNT: int = 10
    CONTAINER_MEMORY_LIMIT: str = "512m"
    CONTAINER_CPU_LIMIT: float = 0.5
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()