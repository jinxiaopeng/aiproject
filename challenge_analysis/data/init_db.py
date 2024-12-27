"""数据库初始化模块"""
from ..utils.db import Database

def init_db(db_path: str) -> bool:
    """初始化数据库
    
    Args:
        db_path: 数据库文件路径
        
    Returns:
        是否初始化成功
    """
    db = Database(db_path)
    
    # 创建挑战表
    challenges_table = """
    CREATE TABLE IF NOT EXISTS challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        difficulty INTEGER NOT NULL,
        points INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """
    
    # 创建用户挑战表
    user_challenges_table = """
    CREATE TABLE IF NOT EXISTS user_challenges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        challenge_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        start_time TEXT NOT NULL,
        completion_time TEXT,
        attempts INTEGER NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (challenge_id) REFERENCES challenges (id)
    )
    """
    
    # 创建挑战反馈表
    challenge_feedback_table = """
    CREATE TABLE IF NOT EXISTS challenge_feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        challenge_id INTEGER NOT NULL,
        difficulty_rating INTEGER NOT NULL,
        clarity_rating INTEGER NOT NULL,
        comments TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (challenge_id) REFERENCES challenges (id)
    )
    """
    
    # 创建用户推荐表
    user_recommendations_table = """
    CREATE TABLE IF NOT EXISTS user_recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        challenge_id INTEGER NOT NULL,
        score REAL NOT NULL,
        reason TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (challenge_id) REFERENCES challenges (id)
    )
    """
    
    # 创建挑战同步日志表
    challenges_sync_log_table = """
    CREATE TABLE IF NOT EXISTS challenges_sync_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sync_time TEXT NOT NULL,
        status TEXT NOT NULL,
        message TEXT
    )
    """
    
    # 创建用户进度同步日志表
    user_progress_sync_log_table = """
    CREATE TABLE IF NOT EXISTS user_progress_sync_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sync_time TEXT NOT NULL,
        status TEXT NOT NULL,
        message TEXT
    )
    """
    
    # 创建索引
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_user_challenges_user ON user_challenges(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_user_challenges_challenge ON user_challenges(challenge_id)",
        "CREATE INDEX IF NOT EXISTS idx_challenge_feedback_user ON challenge_feedback(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_challenge_feedback_challenge ON challenge_feedback(challenge_id)",
        "CREATE INDEX IF NOT EXISTS idx_user_recommendations_user ON user_recommendations(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_user_recommendations_challenge ON user_recommendations(challenge_id)"
    ]
    
    # 执行建表语句
    tables = [
        challenges_table,
        user_challenges_table,
        challenge_feedback_table,
        user_recommendations_table,
        challenges_sync_log_table,
        user_progress_sync_log_table
    ]
    
    try:
        with db.transaction():
            # 创建表
            for table in tables:
                db.execute_script(table)
                
            # 创建索引
            for index in indexes:
                db.execute_script(index)
                
        return True
        
    except Exception as e:
        print(f"初始化数据库失败: {str(e)}")
        return False
    finally:
        db.close()
        
def reset_db(db_path: str) -> bool:
    """重置数据库
    
    Args:
        db_path: 数据库文件路径
        
    Returns:
        是否重置成功
    """
    db = Database(db_path)
    
    # 删除所有表
    tables = [
        'user_progress_sync_log',
        'challenges_sync_log',
        'user_recommendations',
        'challenge_feedback',
        'user_challenges',
        'challenges'
    ]
    
    try:
        with db.transaction():
            # 删除表
            for table in tables:
                db.execute_script(f"DROP TABLE IF EXISTS {table}")
                
        # 重新初始化数据库
        return init_db(db_path)
        
    except Exception as e:
        print(f"重置数据库失败: {str(e)}")
        return False
    finally:
        db.close() 