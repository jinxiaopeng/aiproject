"""调度器模块"""
import logging
import threading
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .config import Config
from .data.collector import DataCollector
from .core.analyzer import ChallengeAnalyzer

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskScheduler:
    """任务调度器"""
    
    def __init__(self):
        """初始化调度器"""
        self.collector = DataCollector()
        self.analyzer = ChallengeAnalyzer()
        self.is_running = False
        self.tasks = []
        
    def start(self):
        """启动调度器"""
        if self.is_running:
            logger.warning("调度器已在运行")
            return
            
        self.is_running = True
        logger.info("启动调度器")
        
        # 启动定时任务
        self.tasks = [
            threading.Thread(target=self._run_sync_task),
            threading.Thread(target=self._run_analysis_task),
            threading.Thread(target=self._run_recommendation_task)
        ]
        
        for task in self.tasks:
            task.daemon = True
            task.start()
            
    def stop(self):
        """停止调度器"""
        if not self.is_running:
            logger.warning("调度器未在运行")
            return
            
        self.is_running = False
        logger.info("停止调度器")
        
        # 等待任务完成
        for task in self.tasks:
            task.join()
            
        self.tasks = []
        
    def _run_sync_task(self):
        """运行同步任务"""
        while self.is_running:
            logger.info("开始数据同步")
            try:
                self.sync_task()
            except Exception as e:
                logger.error(f"数据同步失败: {str(e)}")
            logger.info("数据同步完成")
            time.sleep(Config.SYNC_INTERVAL)
            
    def _run_analysis_task(self):
        """运行分析任务"""
        while self.is_running:
            logger.info("开始数据分析")
            try:
                self.analyze_task()
            except Exception as e:
                logger.error(f"数据分析失败: {str(e)}")
            logger.info("数据分析完成")
            time.sleep(Config.ANALYSIS_INTERVAL)
            
    def _run_recommendation_task(self):
        """运行推荐任务"""
        while self.is_running:
            logger.info("开始生成推荐")
            try:
                self.recommend_task()
            except Exception as e:
                logger.error(f"推荐生成失败: {str(e)}")
            logger.info("推荐生成完成")
            time.sleep(Config.RECOMMENDATION_INTERVAL)
            
    def sync_task(self):
        """执行同步任务"""
        # 同步用户数据
        self.collector.sync_user_data()
        
        # 同步靶场数据
        self.collector.sync_challenge_data()
        
        # 同步用户进度
        self.collector.sync_user_progress()
        
    def analyze_task(self):
        """执行分析任务"""
        # 获取需要分析的靶场
        challenges = self.get_challenges_for_analysis()
        
        # 分析每个靶场
        for challenge in challenges:
            # 收集分析数据
            self.collector.collect_challenge_analytics(challenge['id'])
            
            # 分析难度
            self.analyzer.analyze_challenge_difficulty(challenge['id'])
            
        # 分析用户表现
        users = self.get_active_users()
        for user in users:
            self.analyzer.analyze_user_performance(user['id'])
            
    def recommend_task(self):
        """执行推荐任务"""
        # 获取活跃用户
        users = self.get_active_users()
        
        # 为每个用户生成推荐
        for user in users:
            self.analyzer.generate_recommendations(user['id'])
            
    def get_challenges_for_analysis(self) -> List[Dict[str, Any]]:
        """获取需要分析的靶场
        
        Returns:
            靶场列表
        """
        # 获取所有靶场
        with self.collector.storage.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, category, difficulty, points
                FROM challenges
                WHERE id IN (
                    SELECT DISTINCT challenge_id
                    FROM user_progress
                    WHERE updated_at > datetime('now', '-1 day')
                )
            """)
            return [dict(row) for row in cursor.fetchall()]
            
    def get_active_users(self) -> List[Dict[str, Any]]:
        """获取活跃用户
        
        Returns:
            用户列表
        """
        # 获取最近活跃的用户
        with self.collector.storage.db.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT u.id, u.username
                FROM users u
                JOIN user_progress up ON u.id = up.user_id
                WHERE up.updated_at > datetime('now', '-1 day')
            """)
            return [dict(row) for row in cursor.fetchall()] 