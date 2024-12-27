import sqlite3
import os
from pathlib import Path

def init_db():
    """
    初始化监控系统数据库
    创建必要的表结构
    """
    # 获取monitor_service目录的路径
    base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    data_dir = base_dir / 'data'
    
    # 确保数据目录存在
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 设置数据库文件路径
    db_path = data_dir / 'monitor.db'
    print(f"初始化数据库: {db_path}")
    
    # 连接到SQLite数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建视频学习记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS video_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        chapter_id INTEGER NOT NULL,
        progress INTEGER DEFAULT 0,      -- 进度百分比(0-100)
        duration INTEGER DEFAULT 0,      -- 视频总时长(秒)
        current_time INTEGER DEFAULT 0,  -- 当前播放时间(秒)
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建学习行为表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS learning_behavior (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        course_id INTEGER NOT NULL,
        start_time DATETIME NOT NULL,    -- 开始学习时间
        end_time DATETIME,              -- 结束学习时间
        duration INTEGER DEFAULT 0,      -- 学习时长(秒)
        behavior_type TEXT NOT NULL,     -- 行为类型(video_watch/challenge/quiz)
        content_id INTEGER NOT NULL      -- 对应内容ID(视频ID/靶场ID/测验ID)
    )
    ''')
    
    # 创建靶场训练记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS challenge_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        challenge_id INTEGER NOT NULL,
        status TEXT CHECK(status IN ('not_started', 'in_progress', 'completed')),
        start_time DATETIME,
        complete_time DATETIME,
        attempts INTEGER DEFAULT 0,      -- 尝试次数
        hints_used INTEGER DEFAULT 0,    -- 使用提示数
        score INTEGER DEFAULT 0          -- 获得分数
    )
    ''')
    
    # 创建每日学习统计表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        stats_date DATE DEFAULT CURRENT_DATE,
        total_study_time INTEGER DEFAULT 0,          -- 当日总学习时长(秒)
        video_completion_count INTEGER DEFAULT 0,     -- 当日完成视频数
        challenge_completion_count INTEGER DEFAULT 0,  -- 当日完成靶场数
        score_gained INTEGER DEFAULT 0,               -- 当日获得分数
        UNIQUE(user_id, stats_date)
    )
    ''')
    
    # 提交事务
    conn.commit()
    conn.close()
    
    print("数据库初始化完成")

if __name__ == '__main__':
    init_db() 