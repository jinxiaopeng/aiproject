"""配置模块"""

class Config:
    """配置类"""
    
    # 数据库配置
    SQLITE_DB_PATH = "challenge_analysis.db"
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""
    MYSQL_DATABASE = "ctf_platform"
    
    # 分析配置
    MIN_ATTEMPTS_FOR_ANALYSIS = 10  # 分析所需的最少尝试次数
    MIN_FEEDBACK_FOR_ANALYSIS = 5   # 分析所需的最少反馈数
    
    # 调度配置
    SYNC_INTERVAL = 300        # 数据同步间隔(秒)
    ANALYSIS_INTERVAL = 3600   # 数据分析间隔(秒)
    RECOMMENDATION_INTERVAL = 1800  # 推荐生成间隔(秒)
    ACTIVE_USER_WINDOW = 86400     # 活跃用户时间窗口(秒)
    
    # 推荐配置
    MAX_RECOMMENDATIONS = 5    # 每个用户的最大推荐数
    RECOMMENDATION_EXPIRE = 86400  # 推荐过期时间(秒)
    
    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
