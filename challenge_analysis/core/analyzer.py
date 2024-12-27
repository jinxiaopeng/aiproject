"""分析器模块"""
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from challenge_analysis.config import Config
from challenge_analysis.data.storage import DatabaseUtils

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChallengeAnalyzer:
    """靶场分析器"""
    
    def __init__(self):
        """初始化分析器"""
        self.db_utils = DatabaseUtils(Config.SQLITE_DB_PATH)
        
    def analyze_challenge_difficulty(self, challenge_id: int) -> Optional[float]:
        """分析题目难度
        
        Args:
            challenge_id: 靶场ID
            
        Returns:
            难度分数，如果分析失败则返回None
        """
        try:
            # 获取题目统计数据
            stats = self.db_utils.execute_query("""
                SELECT 
                    COUNT(*) as total_attempts,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as successful_attempts,
                    AVG(CASE 
                        WHEN status = 'completed' 
                        THEN CAST((julianday(completion_time) - julianday(start_time)) * 24 * 60 * 60 AS INTEGER)
                        ELSE NULL 
                    END) as avg_completion_time,
                    AVG(hints_used) as avg_hints_used,
                    (SELECT AVG(difficulty_rating) FROM challenge_feedback WHERE challenge_id = ?) as avg_difficulty_rating
                FROM user_challenges
                WHERE challenge_id = ?
            """, (challenge_id, challenge_id))
            
            if not stats or not stats[0]['total_attempts']:
                return None
                
            stats = stats[0]
                
            # 计算难度分数
            difficulty_score = 0.0
            weights = 0.0
            
            # 1. 完成率权重 40%
            completion_rate = stats['successful_attempts'] / stats['total_attempts']
            difficulty_score += (1 - completion_rate) * 0.4
            weights += 0.4
                
            # 2. 平均完成时间权重 30%
            if stats['avg_completion_time']:
                # 假设超过2小时算最难
                time_score = min(stats['avg_completion_time'] / 7200, 1)
                difficulty_score += time_score * 0.3
                weights += 0.3
                
            # 3. 平均使用提示数权重 20%
            if stats['avg_hints_used'] is not None:
                # 假设使用5个以上提示算最难
                hint_score = min(stats['avg_hints_used'] / 5, 1)
                difficulty_score += hint_score * 0.2
                weights += 0.2
                
            # 4. 用户反馈难度权重 10%
            if stats['avg_difficulty_rating']:
                # 难度评分是1-5，转换为0-1
                feedback_score = (stats['avg_difficulty_rating'] - 1) / 4
                difficulty_score += feedback_score * 0.1
                weights += 0.1
                
            # 根据实际权重调整分数
            if weights > 0:
                difficulty_score = difficulty_score / weights
                
            return difficulty_score
            
        except Exception as e:
            logger.error(f"分析题目难度失败: {str(e)}")
            return None
            
    def analyze_user_performance(self, user_id: int) -> Optional[Dict[str, Any]]:
        """分析用户表现
        
        Args:
            user_id: 用户ID
            
        Returns:
            表现数据，如果分析失败则返回None
        """
        try:
            # 获取用户进度数据
            progress = self.db_utils.execute_query("""
                SELECT 
                    COUNT(*) as completed_challenges,
                    SUM(c.points) as total_points,
                    (SELECT COUNT(*) FROM challenges) as total_challenges
                FROM user_challenges uc
                JOIN challenges c ON uc.challenge_id = c.id
                WHERE uc.user_id = ? AND uc.status = 'completed'
            """, (user_id,))
            
            if not progress:
                return None
                
            # 获取用户技能数据
            skills = self.db_utils.execute_query("""
                SELECT skill_type, skill_level, skill_points
                FROM user_skills
                WHERE user_id = ?
            """, (user_id,))
            
            # 计算表现指标
            performance = {
                'completed_challenges': progress[0]['completed_challenges'],
                'total_points': progress[0]['total_points'],
                'total_challenges': progress[0]['total_challenges'],
                'skill_levels': {
                    skill['skill_type']: {
                        'level': skill['skill_level'],
                        'points': skill['skill_points']
                    }
                    for skill in skills
                }
            }
            
            # 获取挑战完成数据
            challenges = self.db_utils.execute_query("""
                SELECT 
                    completion_time,
                    start_time,
                    hints_used,
                    status
                FROM user_challenges
                WHERE user_id = ? AND completion_time IS NOT NULL
            """, (user_id,))
            
            # 计算整体统计数据
            overall_stats = {
                'avg_completion_time': 0,
                'avg_hints_used': 0,
                'success_rate': 0,
                'total_attempts': len(challenges) if challenges else 0,
                'total_challenges': progress[0]['total_challenges']
            }
            
            if challenges:
                # 计算平均完成时间
                completion_times = [
                    self._parse_time_diff(c['completion_time'], c['start_time'])
                    for c in challenges 
                    if c['status'] == 'completed'
                ]
                if completion_times:
                    overall_stats['avg_completion_time'] = sum(completion_times) / len(completion_times)
                    
                # 计算平均提示使用数
                overall_stats['avg_hints_used'] = sum(c['hints_used'] for c in challenges) / len(challenges)
                
                # 计算成功率
                overall_stats['success_rate'] = len([c for c in challenges if c['status'] == 'completed']) / len(challenges)
                
            performance['overall_stats'] = overall_stats
            return performance
            
        except Exception as e:
            logger.error(f"分析用户表现失败: {str(e)}")
            return None
            
    def _parse_time_diff(self, end_time: str, start_time: str) -> float:
        """计算时间差（秒）"""
        end = datetime.fromisoformat(end_time)
        start = datetime.fromisoformat(start_time)
        return (end - start).total_seconds()
            
    def generate_recommendations(self, user_id: int) -> List[Dict[str, Any]]:
        """生成推荐
        
        Args:
            user_id: 用户ID
            
        Returns:
            推荐列表
        """
        try:
            # 获取用户表现数据
            performance = self.analyze_user_performance(user_id)
            if not performance:
                return []
                
            # 获取用户已完成的题目
            completed = self.db_utils.execute_query("""
                SELECT challenge_id
                FROM user_progress
                WHERE user_id = ? AND completed = 1
            """, (user_id,))
            completed_ids = [c['challenge_id'] for c in completed]
            
            # 获取所有可用题目
            challenges = self.db_utils.execute_query("""
                SELECT *
                FROM challenges
                WHERE id NOT IN ({})
            """.format(','.join('?' * len(completed_ids)) if completed_ids else '0'),
                completed_ids)
                
            recommendations = []
            for challenge in challenges:
                # 计算推荐分数
                score = self._calculate_recommendation_score(challenge, performance)
                if score > 0:
                    recommendations.append({
                        'challenge_id': challenge['id'],
                        'score': score,
                        'reason': self._get_recommendation_reason(challenge, performance)
                    })
                    
            # 按分数排序
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            # 更新推荐
            self.db_utils.update_user_recommendations(user_id, recommendations)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"生成推荐失败: {str(e)}")
            return []
            
    def _calculate_recommendation_score(self, challenge: Dict[str, Any], performance: Dict[str, Any]) -> float:
        """计算推荐分数"""
        score = 0.0
        
        # 1. 难度匹配度 (40%)
        skill_level = performance['skill_levels'].get(challenge['category'], {}).get('level', 0)
        difficulty_diff = abs(challenge['difficulty'] - skill_level)
        score += max(0, 1 - difficulty_diff / 3) * 0.4
        
        # 2. 别匹配度 (30%)
        if challenge['category'] in performance['skill_levels']:
            score += 0.3
            
        # 3. 进度匹配度 (30%)
        if performance['completed_challenges'] > 0:
            progress_score = min(performance['completed_challenges'] / 10, 1)  # 假设完成10题为满分
            score += progress_score * 0.3
            
        return score
        
    def _get_recommendation_reason(self, challenge: Dict[str, Any], performance: Dict[str, Any]) -> str:
        """生成推荐原因"""
        skill_level = performance['skill_levels'].get(challenge['category'], {}).get('level', 0)
        
        if challenge['difficulty'] <= skill_level:
            return "基于你当前的技能水平，这个挑战适合你"
        elif challenge['difficulty'] == skill_level + 1:
            return "这个挑战稍有难度，可以帮助你提升技能"
        else:
            return "这是一个具有挑战性的题目，可以尝试挑战"
            
    def update_challenge_pool(self) -> bool:
        """更新题目池
        
        更新所有题目的难度和其他统计数据
        
        Returns:
            是否更新成功
        """
        try:
            # 获取所有题目
            challenges = self.db_utils.execute_query("SELECT id FROM challenges")
            
            for challenge in challenges:
                # 分析难度
                difficulty = self.analyze_challenge_difficulty(challenge['id'])
                if difficulty is not None:
                    # 将0-1的难度分数转换为1-5的难度等级
                    difficulty_level = int(difficulty * 4) + 1
                    
                    # 更新难度分数
                    self.db_utils.execute_query("""
                        UPDATE challenges
                        SET difficulty = ?,
                            updated_at = ?
                        WHERE id = ?
                    """, (
                        difficulty_level,
                        datetime.now().isoformat(),
                        challenge['id']
                    ))
                    
            return True
            
        except Exception as e:
            logger.error(f"更新题目池失败: {str(e)}")
            return False
