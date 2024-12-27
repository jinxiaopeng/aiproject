"""数据收集模块"""
import logging
import mysql.connector
from datetime import datetime
from typing import List, Dict, Any, Optional
from challenge_analysis.config import Config
from challenge_analysis.data.storage import DatabaseUtils

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataCollector:
    """数据收集类"""
    
    def __init__(self):
        """初始化收集器"""
        self.db_utils = DatabaseUtils(Config.SQLITE_DB_PATH)
        self._connect_mysql()
        
    def _connect_mysql(self):
        """连接MySQL数据库"""
        self.mysql_conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        self.mysql_cursor = self.mysql_conn.cursor(dictionary=True)
        
    def __del__(self):
        """清理资源"""
        if hasattr(self, 'mysql_cursor'):
            self.mysql_cursor.close()
        if hasattr(self, 'mysql_conn'):
            self.mysql_conn.close()
            
    def sync_user_data(self) -> bool:
        """同步用户数据
        
        从MySQL同步用户数据到SQLite
        
        Returns:
            是否同步成功
        """
        try:
            # 获取MySQL中的用户数据
            self.mysql_cursor.execute("""
                SELECT id, username, created_at, updated_at
                FROM users
                WHERE updated_at > (
                    SELECT COALESCE(MAX(updated_at), '1970-01-01')
                    FROM users_sync_log
                )
            """)
            users = self.mysql_cursor.fetchall()
            
            if not users:
                return True
                
            # 更新SQLite
            for user in users:
                self.db_utils.execute_query("""
                    INSERT OR REPLACE INTO users (
                        id, username, created_at, updated_at
                    ) VALUES (?, ?, ?, ?)
                """, (
                    user['id'],
                    user['username'],
                    user['created_at'],
                    user['updated_at']
                ))
                
            # 记录同步时间
            self.db_utils.execute_query("""
                INSERT INTO users_sync_log (sync_time)
                VALUES (?)
            """, (datetime.now().isoformat(),))
                
            logger.info(f"同步用户数据成功: {len(users)}条记录")
            return True
            
        except Exception as e:
            logger.error(f"同步用户数据失败: {str(e)}")
            return False
            
    def sync_challenge_data(self) -> bool:
        """同步靶场数据
        
        从MySQL同步靶场数据到SQLite
        
        Returns:
            是否同步成功
        """
        try:
            # 获取MySQL中的靶场数据
            self.mysql_cursor.execute("""
                SELECT id, title, category, difficulty, points, created_at, updated_at
                FROM challenges
                WHERE updated_at > (
                    SELECT COALESCE(MAX(sync_time), '1970-01-01')
                    FROM challenges_sync_log
                )
            """)
            challenges = self.mysql_cursor.fetchall()
            
            if not challenges:
                logger.info("没有新的靶场数据需要同步")
                return True
                
            # 更新SQLite
            for challenge in challenges:
                self.db_utils.execute_query("""
                    INSERT OR REPLACE INTO challenges (
                        id, title, category, difficulty, points,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    challenge['id'],
                    challenge['title'],
                    challenge['category'],
                    challenge['difficulty'],
                    challenge['points'],
                    challenge['created_at'],
                    challenge['updated_at']
                ))
                
            # 记录同步时间
            self.db_utils.execute_query("""
                INSERT INTO challenges_sync_log (sync_time, status, message)
                VALUES (?, ?, ?)
            """, (
                datetime.now().isoformat(),
                'success',
                f'同步了{len(challenges)}条记录'
            ))
                
            logger.info(f"同步靶场数据成功: {len(challenges)}条记录")
            return True
            
        except Exception as e:
            logger.error(f"同步靶场数据失败: {str(e)}")
            # 记录失败日志
            self.db_utils.execute_query("""
                INSERT INTO challenges_sync_log (sync_time, status, message)
                VALUES (?, ?, ?)
            """, (
                datetime.now().isoformat(),
                'error',
                str(e)
            ))
            return False
            
    def sync_user_progress(self):
        """同步用户进度数据"""
        try:
            # 从MySQL获取用户进度数据
            self.mysql_cursor.execute("""
                SELECT 
                    uc.user_id,
                    uc.challenge_id,
                    uc.start_time,
                    uc.completion_time,
                    uc.attempts,
                    uc.hints_used,
                    uc.status,
                    uc.updated_at
                FROM user_challenges uc
                WHERE uc.updated_at > (
                    SELECT COALESCE(MAX(sync_time), '1970-01-01')
                    FROM user_progress_sync_log
                )
            """)
            progress_data = self.mysql_cursor.fetchall()
            
            if not progress_data:
                logger.info("没有新的用户进度数据需要同步")
                return True
                
            # 更新进度数据
            for progress in progress_data:
                self.db_utils.execute_query("""
                    INSERT OR REPLACE INTO user_challenges (
                        user_id, challenge_id, start_time, completion_time,
                        attempts, hints_used, status, updated_at, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    progress['user_id'],
                    progress['challenge_id'],
                    progress['start_time'],
                    progress['completion_time'],
                    progress['attempts'],
                    progress['hints_used'],
                    progress['status'],
                    progress['updated_at'],
                    progress['start_time']  # 使用start_time作为created_at
                ))
                
            # 记录同步时间
            self.db_utils.execute_query("""
                INSERT INTO user_progress_sync_log (sync_time, status, message)
                VALUES (?, ?, ?)
            """, (
                datetime.now().isoformat(),
                'success',
                f'同步了{len(progress_data)}条记录'
            ))
            
            logger.info(f"同步用户进度数据成功: {len(progress_data)}条记录")
            return True
            
        except Exception as e:
            logger.error(f"同步用户进度数据失败: {str(e)}")
            # 记录失败日志
            self.db_utils.execute_query("""
                INSERT INTO user_progress_sync_log (sync_time, status, message)
                VALUES (?, ?, ?)
            """, (
                datetime.now().isoformat(),
                'error',
                str(e)
            ))
            return False
            
    def collect_challenge_analytics(self, challenge_id: int) -> bool:
        """收集靶场分析数据
        
        收集更新靶场的分析数据
        
        Args:
            challenge_id: 靶场ID
            
        Returns:
            是否收集成功
        """
        try:
            # 获取MySQL中的分析数据
            self.mysql_cursor.execute("""
                SELECT 
                    COUNT(*) as total_attempts,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as successful_attempts,
                    AVG(CASE WHEN status = 'completed' THEN completion_time ELSE NULL END) as avg_completion_time,
                    AVG(hints_used) as avg_hints_used
                FROM user_challenges
                WHERE challenge_id = ?
            """, (challenge_id,))
            analytics = self.mysql_cursor.fetchone()
            
            if not analytics:
                return True
                
            # 更新SQLite
            self.db_utils.execute_query("""
                INSERT OR REPLACE INTO challenge_analytics (
                    challenge_id, total_attempts, successful_attempts,
                    avg_completion_time, avg_hints_used, last_analysis_time
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                challenge_id,
                analytics['total_attempts'],
                analytics['successful_attempts'],
                analytics['avg_completion_time'],
                analytics['avg_hints_used'],
                datetime.now().isoformat()
            ))
            
            logger.info(f"收集靶场[{challenge_id}]分析数据成功")
            return True
            
        except Exception as e:
            logger.error(f"收集靶场[{challenge_id}]分析数据失败: {str(e)}")
            return False
            
    def collect_user_feedback(self, user_id, challenge_id, feedback_data):
        """收集用户反馈"""
        try:
            # 更新反馈数据
            feedback = {
                'user_id': user_id,
                'challenge_id': challenge_id,
                'difficulty_rating': feedback_data.get('difficulty_rating', 3),
                'clarity_rating': feedback_data.get('clarity_rating', 0),
                'hint_helpfulness': feedback_data.get('hint_helpfulness', 0),
                'comments': feedback_data.get('comments', ''),
                'created_at': datetime.now().isoformat()
            }
            
            self.db_utils.execute_query("""
                INSERT INTO challenge_feedback (
                    user_id, challenge_id, difficulty_rating,
                    clarity_rating, hint_helpfulness, comments,
                    created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                feedback['user_id'],
                feedback['challenge_id'],
                feedback['difficulty_rating'],
                feedback['clarity_rating'],
                feedback['hint_helpfulness'],
                feedback['comments'],
                feedback['created_at']
            ))
            
            logger.info(f"收集用户[{user_id}]对靶场[{challenge_id}]的反馈成功")
            return True
            
        except Exception as e:
            logger.error(f"收集用户反馈失败: {str(e)}")
            return False
            
    def record_challenge_attempt(self, user_id: int, challenge_id: int, attempt_data: Dict[str, Any]) -> bool:
        """记录解题尝试
        
        记录用户的解题尝试数据
        
        Args:
            user_id: 用户ID
            challenge_id: 靶场ID
            attempt_data: 尝试数据
            
        Returns:
            是否记录成功
        """
        try:
            # 更新MySQL
            self.mysql_cursor.execute("""
                INSERT INTO user_challenges (
                    user_id, challenge_id, status,
                    start_time, completion_time, hints_used, attempts,
                    created_at, updated_at
                ) VALUES (
                    %(user_id)s, %(challenge_id)s, %(status)s,
                    NOW(), %(completion_time)s, %(hints_used)s, %(attempts)s,
                    NOW(), NOW()
                )
            """, {
                'user_id': user_id,
                'challenge_id': challenge_id,
                'status': attempt_data['status'],
                'completion_time': attempt_data['completion_time'],
                'hints_used': attempt_data['hints_used'],
                'attempts': attempt_data['attempts']
            })
            self.mysql_conn.commit()
            
            # 同步到SQLite
            self.db_utils.execute_query("""
                INSERT INTO user_challenges (
                    user_id, challenge_id, status,
                    start_time, completion_time, hints_used, attempts,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                challenge_id,
                attempt_data['status'],
                datetime.now().isoformat(),
                attempt_data['completion_time'],
                attempt_data['hints_used'],
                attempt_data['attempts'],
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
                
            # 更新分析数据
            self.collect_challenge_analytics(challenge_id)
            
            logger.info(f"记录用户[{user_id}]对靶场[{challenge_id}]的解题尝试成功")
            return True
            
        except Exception as e:
            logger.error(f"记录解题尝试失败: {str(e)}")
            return False
