"""测试基类模块"""
import os
import sqlite3
import unittest
from datetime import datetime

class TestBase(unittest.TestCase):
    """测试基类"""
    
    def setUp(self):
        """测试初始化"""
        # 创建测试数据库
        self.test_db_path = 'test.db'
        self._init_test_db()
        
    def tearDown(self):
        """测试清理"""
        # 删除测试数据库
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
            
    def _init_test_db(self):
        """初始化测试数据库"""
        conn = sqlite3.connect(self.test_db_path)
        try:
            conn.executescript('''
                -- 创建挑战表
                CREATE TABLE IF NOT EXISTS challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    category TEXT NOT NULL,
                    difficulty INTEGER NOT NULL,
                    points INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                
                -- 创建用户挑战表
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
                );
                
                -- 创建挑战反馈表
                CREATE TABLE IF NOT EXISTS challenge_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    challenge_id INTEGER NOT NULL,
                    difficulty_rating INTEGER NOT NULL,
                    clarity_rating INTEGER NOT NULL,
                    comments TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (challenge_id) REFERENCES challenges (id)
                );
                
                -- 创建分析任务表
                CREATE TABLE IF NOT EXISTS analysis_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    challenge_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    completed_at TEXT,
                    FOREIGN KEY (challenge_id) REFERENCES challenges (id)
                );
                
                -- 创建同步任务表
                CREATE TABLE IF NOT EXISTS sync_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                );
                
                -- 创建挑战同步日志表
                CREATE TABLE IF NOT EXISTS challenges_sync_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sync_time TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT
                );
                
                -- 创建用户进度同步日志表
                CREATE TABLE IF NOT EXISTS user_progress_sync_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sync_time TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT
                );
            ''')
            conn.commit()
        finally:
            conn.close() 