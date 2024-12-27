"""数据存储模块"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..utils.db import Database

class DatabaseUtils:
    """数据库工具类，提供高层业务逻辑"""
    
    def __init__(self, db_path: str):
        """初始化数据库工具
        
        Args:
            db_path: 数据库文件路径
        """
        self.db = Database(db_path)
        
    def get_challenge_stats(self, challenge_id: int) -> Dict[str, Any]:
        """获取挑战统计数据
        
        Args:
            challenge_id: 挑战ID
            
        Returns:
            统计数据字典
        """
        stats = self.db.execute("""
            SELECT 
                AVG(difficulty_rating) as avg_difficulty_rating,
                AVG(clarity_rating) as avg_clarity_rating,
                COUNT(*) as total_feedback
            FROM challenge_feedback
            WHERE challenge_id = ?
        """, (challenge_id,))
        
        return stats[0] if stats else {}
        
    def get_user_progress(self, user_id: int) -> Dict[str, Any]:
        """获取用户进度数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            进度数据字典
        """
        progress = self.db.execute("""
            SELECT 
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_count,
                COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress_count,
                COUNT(*) as total_challenges,
                AVG(CASE WHEN status = 'completed' THEN attempts END) as avg_attempts
            FROM user_challenges
            WHERE user_id = ?
        """, (user_id,))
        
        return progress[0] if progress else {}
        
    def get_user_recommendations(self, user_id: int) -> List[Dict[str, Any]]:
        """获取用户推荐数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            推荐数据列表
        """
        return self.db.execute("""
            SELECT r.*, c.title, c.category, c.difficulty, c.points
            FROM user_recommendations r
            JOIN challenges c ON r.challenge_id = c.id
            WHERE r.user_id = ?
            ORDER BY r.score DESC
        """, (user_id,))
        
    def record_challenge_attempt(self, user_id: int, challenge_id: int, 
                               status: str, completion_time: Optional[str] = None) -> bool:
        """记录挑战尝试
        
        Args:
            user_id: 用户ID
            challenge_id: 挑战ID
            status: 状态
            completion_time: 完成时间
            
        Returns:
            是否记录成功
        """
        now = datetime.now().isoformat()
        data = {
            'user_id': user_id,
            'challenge_id': challenge_id,
            'status': status,
            'start_time': now,
            'completion_time': completion_time,
            'attempts': 1,
            'created_at': now,
            'updated_at': now
        }
        
        return self.db.insert('user_challenges', data) is not None
        
    def collect_user_feedback(self, user_id: int, challenge_id: int,
                            difficulty_rating: int, clarity_rating: int,
                            comments: Optional[str] = None) -> bool:
        """收集用户反馈
        
        Args:
            user_id: 用户ID
            challenge_id: 挑战ID
            difficulty_rating: 难度评分
            clarity_rating: 清晰度评分
            comments: 评论
            
        Returns:
            是否收集成功
        """
        data = {
            'user_id': user_id,
            'challenge_id': challenge_id,
            'difficulty_rating': difficulty_rating,
            'clarity_rating': clarity_rating,
            'comments': comments,
            'created_at': datetime.now().isoformat()
        }
        
        return self.db.insert('challenge_feedback', data) is not None
        
    def sync_challenge_data(self, challenges: List[Dict[str, Any]]) -> bool:
        """同步挑战数据
        
        Args:
            challenges: 挑战数据列表
            
        Returns:
            是否同步成功
        """
        try:
            self.db.begin_transaction()
            
            # 记录同步开始
            sync_time = datetime.now().isoformat()
            self.db.insert('challenges_sync_log', {
                'sync_time': sync_time,
                'status': 'started',
                'message': f'开始同步 {len(challenges)} 条记录'
            })
            
            # 同步数据
            for challenge in challenges:
                self.db.execute("""
                    INSERT OR REPLACE INTO challenges 
                    (id, title, description, category, difficulty, points, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    challenge['id'],
                    challenge['title'],
                    challenge['description'],
                    challenge['category'],
                    challenge['difficulty'],
                    challenge['points'],
                    challenge.get('created_at', sync_time),
                    challenge.get('updated_at', sync_time)
                ))
            
            # 记录同步完成
            self.db.insert('challenges_sync_log', {
                'sync_time': datetime.now().isoformat(),
                'status': 'completed',
                'message': f'成功同步 {len(challenges)} 条记录'
            })
            
            self.db.commit_transaction()
            return True
            
        except Exception as e:
            self.db.rollback_transaction()
            
            # 记录同步失败
            self.db.insert('challenges_sync_log', {
                'sync_time': datetime.now().isoformat(),
                'status': 'failed',
                'message': str(e)
            })
            
            return False
            
    def sync_user_progress(self, progress_data: List[Dict[str, Any]]) -> bool:
        """同步用户进度数据
        
        Args:
            progress_data: 进度数据列表
            
        Returns:
            是否同步成功
        """
        try:
            self.db.begin_transaction()
            
            # 记录同步开始
            sync_time = datetime.now().isoformat()
            self.db.insert('user_progress_sync_log', {
                'sync_time': sync_time,
                'status': 'started',
                'message': f'开始同步 {len(progress_data)} 条记录'
            })
            
            # 同步数据
            for progress in progress_data:
                self.db.execute("""
                    INSERT OR REPLACE INTO user_challenges
                    (user_id, challenge_id, status, start_time, completion_time, 
                     attempts, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    progress['user_id'],
                    progress['challenge_id'],
                    progress['status'],
                    progress['start_time'],
                    progress.get('completion_time'),
                    progress['attempts'],
                    progress.get('created_at', sync_time),
                    progress.get('updated_at', sync_time)
                ))
            
            # 记录同步完成
            self.db.insert('user_progress_sync_log', {
                'sync_time': datetime.now().isoformat(),
                'status': 'completed',
                'message': f'成功同步 {len(progress_data)} 条记录'
            })
            
            self.db.commit_transaction()
            return True
            
        except Exception as e:
            self.db.rollback_transaction()
            
            # 记录同步失败
            self.db.insert('user_progress_sync_log', {
                'sync_time': datetime.now().isoformat(),
                'status': 'failed',
                'message': str(e)
            })
            
            return False
        
    def get_next_challenge(self, user_id: int, current_challenge_id: int) -> Optional[Dict[str, Any]]:
        """获取下一题推荐
        
        Args:
            user_id: 用户ID
            current_challenge_id: 当前题目ID
            
        Returns:
            下一题信息，如果没有合适的题目则返回None
        """
        # 获取当前题目信息
        current = self.db.execute(
            "SELECT category, difficulty FROM challenges WHERE id = ?",
            (current_challenge_id,)
        )[0]
        
        # 获取用户已完成的题目
        completed = self.db.execute(
            "SELECT challenge_id FROM user_challenges WHERE user_id = ? AND status = 'completed'",
            (user_id,)
        )
        completed_ids = [c['challenge_id'] for c in completed]
        
        # 查找同类型同难度的未完成题目
        next_challenge = self.db.execute("""
            SELECT id, title, description, category, difficulty, points 
            FROM challenges
            WHERE category = ?
            AND difficulty = ?
            AND id != ?
            AND id NOT IN ({})
            LIMIT 1
        """.format(','.join('?' * len(completed_ids))),
            (current['category'], current['difficulty'], current_challenge_id, *completed_ids)
        )
        
        # 如果没有同类型同难度的题，尝试找难度+1的题
        if not next_challenge:
            difficulties = ['easy', 'medium', 'hard']
            current_idx = difficulties.index(current['difficulty'])
            
            # 如果还有更难的难度等级
            if current_idx < len(difficulties) - 1:
                next_difficulty = difficulties[current_idx + 1]
                next_challenge = self.db.execute("""
                    SELECT id, title, description, category, difficulty, points 
                    FROM challenges
                    WHERE category = ?
                    AND difficulty = ?
                    AND id NOT IN ({})
                    LIMIT 1
                """.format(','.join('?' * len(completed_ids))),
                    (current['category'], next_difficulty, *completed_ids)
                )
        
        return next_challenge[0] if next_challenge else None
        
    def update_challenge_completion(self, user_id: int, challenge_id: int) -> bool:
        """更新题目完成状态
        
        Args:
            user_id: 用户ID
            challenge_id: 题目ID
            
        Returns:
            是否更新成功
        """
        try:
            # 更新完成状态
            self.db.execute("""
                UPDATE user_challenges 
                SET status = 'completed',
                    completion_time = ?,
                    updated_at = ?
                WHERE user_id = ? AND challenge_id = ?
            """, (
                datetime.now().isoformat(),
                datetime.now().isoformat(),
                user_id,
                challenge_id
            ))
            return True
        except Exception:
            return False

    def handle_flag_submission(self, user_id: int, challenge_id: int, flag: str) -> Dict[str, Any]:
        """处理flag提交
        
        Args:
            user_id: 用户ID
            challenge_id: 题目ID
            flag: 提交的flag
            
        Returns:
            处理结果
        """
        # 获取正确的flag
        challenge = self.db.execute(
            "SELECT flag FROM challenges WHERE id = ?",
            (challenge_id,)
        )[0]
        
        # 验证flag
        is_correct = flag.strip() == challenge['flag'].strip()
        
        # 记录提交
        self.db.execute("""
            INSERT INTO submissions (user_id, challenge_id, submitted_flag, is_correct)
            VALUES (?, ?, ?, ?)
        """, (user_id, challenge_id, flag, is_correct))
        
        result = {
            "success": is_correct,
            "message": "恭喜完成挑战！" if is_correct else "flag不正确，请重试"
        }
        
        # 如果flag正确，更新完成状态并获取下一题推荐
        if is_correct:
            self.update_challenge_completion(user_id, challenge_id)
            next_challenge = self.get_next_challenge(user_id, challenge_id)
            if next_challenge:
                result["next_challenge"] = next_challenge
        
        return result
