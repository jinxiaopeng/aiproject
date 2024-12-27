"""调度器模块"""
import logging
from datetime import datetime
from challenge_analysis.config import Config
from challenge_analysis.data.storage import DatabaseUtils

class ChallengeScheduler:
    """靶场调度器"""
    
    def __init__(self):
        """初始化调度器"""
        self.db_utils = DatabaseUtils(Config.SQLITE_DB_PATH)
        self.logger = logging.getLogger(__name__)
        
    def schedule_challenge(self, user_id):
        """为用户调度下一个靶场题目
        
        Args:
            user_id: 用户ID
            
        Returns:
            dict: 调度的靶场题目信息，如果没有合适的题目则返回None
        """
        # 获取用户已完成的题目
        completed_challenges = self.db_utils.execute_query("""
            SELECT challenge_id 
            FROM user_progress
            WHERE user_id = ? AND completed = 1
        """, (user_id,))
        completed_ids = [r['challenge_id'] for r in completed_challenges]
        
        # 获取用户技能水平
        user_skills = self.db_utils.execute_query("""
            SELECT skill_type, skill_level
            FROM user_skills
            WHERE user_id = ?
        """, (user_id,))
        
        # 构建技能水平字典
        skill_levels = {s['skill_type']: s['skill_level'] for s in user_skills}
        
        # 查找合适难度的未完成题目
        where_clause = "1=1"
        params = []
        if completed_ids:
            where_clause += f" AND id NOT IN ({','.join(['?' for _ in completed_ids])})"
            params.extend(completed_ids)
            
        challenges = self.db_utils.execute_query(f"""
            SELECT *
            FROM challenges
            WHERE {where_clause}
            ORDER BY difficulty ASC
        """, tuple(params))
        
        # 根据用户技能水平筛选合适的题目
        for challenge in challenges:
            skill_type = challenge['category']
            challenge_difficulty = challenge['difficulty']
            
            # 如果用户没有相关技能记录，或者题目难度在用户能力范围内
            if skill_type not in skill_levels or challenge_difficulty <= skill_levels[skill_type] + 1:
                return challenge
                
        return None
        
    def update_user_skills(self, user_id, challenge_id):
        """更新用户技能水平
        
        Args:
            user_id: 用户ID
            challenge_id: 完成的靶场题目ID
            
        Returns:
            bool: 更新是否成功
        """
        try:
            # 获取题目信息
            challenge = self.db_utils.execute_query("""
                SELECT category, difficulty
                FROM challenges
                WHERE id = ?
            """, (challenge_id,))[0]
            
            # 获取用户当前技能水平
            current_skill = self.db_utils.execute_query("""
                SELECT skill_level, skill_points
                FROM user_skills
                WHERE user_id = ? AND skill_type = ?
            """, (user_id, challenge['category']))
            
            if current_skill:
                # 更新现有技能
                current_skill = current_skill[0]
                new_points = current_skill['skill_points'] + challenge['difficulty'] * 100
                new_level = new_points // 500  # 每500点升一级
                
                self.db_utils.execute_query("""
                    UPDATE user_skills
                    SET skill_level = ?,
                        skill_points = ?,
                        updated_at = ?
                    WHERE user_id = ? AND skill_type = ?
                """, (new_level, new_points, datetime.now(), user_id, challenge['category']))
            else:
                # 创建新技能记录
                points = challenge['difficulty'] * 100
                level = points // 500
                
                self.db_utils.execute_query("""
                    INSERT INTO user_skills (user_id, skill_type, skill_level, skill_points, updated_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, challenge['category'], level, points, datetime.now()))
                
            return True
        except Exception as e:
            self.logger.error(f"更新用户技能失败: {str(e)}")
            return False 