import sqlite3
from datetime import datetime
import os
from pathlib import Path

class MonitorDB:
    """监控系统数据库操作类"""
    
    def __init__(self, db_name='monitor.db'):
        """初始化数据库连接"""
        # 获取monitor_service目录的路径
        self.base_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = self.base_dir / 'data'
        
        # 确保数据目录存在
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 设置数据库文件路径
        self.db_path = self.data_dir / db_name
        print(f"数据库路径: {self.db_path}")
        
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
    
    def record_video_progress(self, user_id, course_id, chapter_id, progress, duration, current_time):
        """
        记录视频学习进度
        
        Args:
            user_id (int): 用户ID
            course_id (int): 课程ID
            chapter_id (int): 章节ID
            progress (int): 进度百分比(0-100)
            duration (int): 视频总时长(秒)
            current_time (int): 当前播放时间(秒)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT OR REPLACE INTO video_progress 
            (user_id, course_id, chapter_id, progress, duration, current_time, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, course_id, chapter_id, progress, duration, current_time))
            
            conn.commit()
        finally:
            conn.close()
    
    def record_learning_behavior(self, user_id, course_id, behavior_type, content_id, duration=None):
        """
        记录学习行为
        
        Args:
            user_id (int): 用户ID
            course_id (int): 课程ID
            behavior_type (str): 行为类型(video_watch/challenge/quiz)
            content_id (int): 内容ID
            duration (int, optional): 学习时长(秒)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 检查是否有未结束的学习行为
            cursor.execute('''
            SELECT id, start_time FROM learning_behavior 
            WHERE user_id = ? AND course_id = ? AND behavior_type = ? 
            AND content_id = ? AND end_time IS NULL
            ''', (user_id, course_id, behavior_type, content_id))
            
            existing = cursor.fetchone()
            
            if existing:
                # 更新已存在的记录
                behavior_id, start_time = existing
                end_time = datetime.now()
                if not duration:
                    duration = int((end_time - datetime.fromisoformat(start_time)).total_seconds())
                
                cursor.execute('''
                UPDATE learning_behavior 
                SET end_time = ?, duration = ?
                WHERE id = ?
                ''', (end_time.isoformat(), duration, behavior_id))
            else:
                # 创建新记录
                cursor.execute('''
                INSERT INTO learning_behavior 
                (user_id, course_id, behavior_type, content_id, start_time)
                VALUES (?, ?, ?, ?, ?)
                ''', (user_id, course_id, behavior_type, content_id, datetime.now().isoformat()))
            
            conn.commit()
        finally:
            conn.close()
    
    def update_challenge_progress(self, user_id, challenge_id, status, attempts=None, hints=None, score=None):
        """
        更新靶场训练进度
        
        Args:
            user_id (int): 用户ID
            challenge_id (int): 靶场ID
            status (str): 状态(not_started/in_progress/completed)
            attempts (int, optional): 尝试次数
            hints (int, optional): 使用提示数
            score (int, optional): 获得分数
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 检查是否存在记录
            cursor.execute('''
            SELECT id FROM challenge_progress 
            WHERE user_id = ? AND challenge_id = ?
            ''', (user_id, challenge_id))
            
            existing = cursor.fetchone()
            current_time = datetime.now().isoformat()
            
            if existing:
                # 更新已存在的记录
                update_fields = []
                params = []
                
                if status == 'completed':
                    update_fields.extend(['status = ?', 'complete_time = ?'])
                    params.extend([status, current_time])
                elif status:
                    update_fields.append('status = ?')
                    params.append(status)
                
                if attempts is not None:
                    update_fields.append('attempts = attempts + ?')
                    params.append(attempts)
                if hints is not None:
                    update_fields.append('hints_used = hints_used + ?')
                    params.append(hints)
                if score is not None:
                    update_fields.append('score = ?')
                    params.append(score)
                
                if update_fields:
                    query = f'''
                    UPDATE challenge_progress 
                    SET {', '.join(update_fields)}
                    WHERE user_id = ? AND challenge_id = ?
                    '''
                    params.extend([user_id, challenge_id])
                    cursor.execute(query, params)
            else:
                # 创建新记录
                cursor.execute('''
                INSERT INTO challenge_progress 
                (user_id, challenge_id, status, start_time, attempts, hints_used, score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (user_id, challenge_id, status, current_time, 
                     attempts or 0, hints or 0, score or 0))
            
            conn.commit()
        finally:
            conn.close()
    
    def update_daily_stats(self, user_id, study_time=0, video_complete=0, 
                          challenge_complete=0, score=0):
        """
        更新每日学习统计
        
        Args:
            user_id (int): 用户ID
            study_time (int): 学习时长(秒)
            video_complete (int): 完成视频数
            challenge_complete (int): 完成靶场数
            score (int): 获得分数
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            today = datetime.now().date().isoformat()
            
            # 更新或插入每日统计
            cursor.execute('''
            INSERT INTO daily_stats 
            (user_id, stats_date, total_study_time, video_completion_count,
             challenge_completion_count, score_gained)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id, stats_date) DO UPDATE SET
                total_study_time = total_study_time + excluded.total_study_time,
                video_completion_count = video_completion_count + excluded.video_completion_count,
                challenge_completion_count = challenge_completion_count + excluded.challenge_completion_count,
                score_gained = score_gained + excluded.score_gained
            ''', (user_id, today, study_time, video_complete, challenge_complete, score))
            
            conn.commit()
        finally:
            conn.close()
    
    def get_user_stats(self, user_id, days=7):
        """
        获取用户学习统计数据
        
        Args:
            user_id (int): 用户ID
            days (int): 统计天数
            
        Returns:
            dict: 用户统计数据
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 获取指定天数的统计数据
            cursor.execute('''
            SELECT stats_date, total_study_time, video_completion_count,
                   challenge_completion_count, score_gained
            FROM daily_stats 
            WHERE user_id = ? 
            AND stats_date >= date('now', ?)
            ORDER BY stats_date DESC
            ''', (user_id, f'-{days} days'))
            
            daily_stats = cursor.fetchall()
            
            # 获取视频完成进度
            cursor.execute('''
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN progress = 100 THEN 1 ELSE 0 END) as completed
            FROM video_progress 
            WHERE user_id = ?
            ''', (user_id,))
            
            video_stats = cursor.fetchone()
            total_videos = video_stats[0] if video_stats[0] else 0
            completed_videos = video_stats[1] if video_stats[1] else 0
            
            # 获取靶场完成情况
            cursor.execute('''
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                   SUM(score) as total_score
            FROM challenge_progress 
            WHERE user_id = ?
            ''', (user_id,))
            
            challenge_stats = cursor.fetchone()
            total_challenges = challenge_stats[0] if challenge_stats[0] else 0
            completed_challenges = challenge_stats[1] if challenge_stats[1] else 0
            total_score = challenge_stats[2] if challenge_stats[2] else 0
            
            try:
                return {
                    'daily_stats': [{
                        'date': row[0],
                        'study_time': row[1],
                        'videos_completed': row[2],
                        'challenges_completed': row[3],
                        'score_gained': row[4]
                    } for row in daily_stats],
                    'video_stats': {
                        'total': total_videos,
                        'completed': completed_videos,
                        'completion_rate': round(completed_videos / total_videos * 100, 2) if total_videos > 0 else 0
                    },
                    'challenge_stats': {
                        'total': total_challenges,
                        'completed': completed_challenges,
                        'completion_rate': round(completed_challenges / total_challenges * 100, 2) if total_challenges > 0 else 0,
                        'total_score': total_score
                    }
                }
            finally:
                conn.close()
        except Exception as e:
            print(f"获取用户学习统计数据时出错: {e}")
            return {}
    
    def get_user_stats(self, user_id, days=7):
        """
        获取用户学习统计数据
        
        Args:
            user_id (int): 用户ID
            days (int): 统计天数
            
        Returns:
            dict: 用户统计数据
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 获取指定天数的统计数据
            cursor.execute('''
            SELECT stats_date, total_study_time, video_completion_count,
                   challenge_completion_count, score_gained
            FROM daily_stats 
            WHERE user_id = ? 
            AND stats_date >= date('now', ?)
            ORDER BY stats_date DESC
            ''', (user_id, f'-{days} days'))
            
            daily_stats = cursor.fetchall()
            
            # 获取视频完成进度
            cursor.execute('''
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN progress = 100 THEN 1 ELSE 0 END) as completed
            FROM video_progress 
            WHERE user_id = ?
            ''', (user_id,))
            
            video_stats = cursor.fetchone()
            total_videos = video_stats[0] if video_stats[0] else 0
            completed_videos = video_stats[1] if video_stats[1] else 0
            
            # 获取靶场完成情况
            cursor.execute('''
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                   SUM(score) as total_score
            FROM challenge_progress 
            WHERE user_id = ?
            ''', (user_id,))
            
            challenge_stats = cursor.fetchone()
            total_challenges = challenge_stats[0] if challenge_stats[0] else 0
            completed_challenges = challenge_stats[1] if challenge_stats[1] else 0
            total_score = challenge_stats[2] if challenge_stats[2] else 0
            
            try:
                return {
                    'daily_stats': [{
                        'date': row[0],
                        'study_time': row[1],
                        'videos_completed': row[2],
                        'challenges_completed': row[3],
                        'score_gained': row[4]
                    } for row in daily_stats],
                    'video_stats': {
                        'total': total_videos,
                        'completed': completed_videos,
                        'completion_rate': round(completed_videos / total_videos * 100, 2) if total_videos > 0 else 0
                    },
                    'challenge_stats': {
                        'total': total_challenges,
                        'completed': completed_challenges,
                        'completion_rate': round(completed_challenges / total_challenges * 100, 2) if total_challenges > 0 else 0,
                        'total_score': total_score
                    }
                }
            finally:
                conn.close()
        except Exception as e:
            print(f"获取用户学习统计数据时出错: {e}")
            return {} 