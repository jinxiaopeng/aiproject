from typing import Dict, List, Optional
from datetime import datetime, timedelta
import mysql.connector
import json
import redis

from config import DB_CONFIG, REDIS_CONFIG
from core.logger import system_logger

class LabRanking:
    """实验排行榜管理器"""
    
    def __init__(self):
        """初始化排行榜管理器"""
        self.redis = redis.Redis(**REDIS_CONFIG)
        system_logger.info("实验排行榜管理器初始化成功", "ranking")
    
    def update_user_score(self, user_id: int, lab_id: int, score: int):
        """更新用户分数"""
        try:
            # 更新总分
            self.redis.zincrby('lab:total_score', score, user_id)
            
            # 更新实验分类分数
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT category FROM labs WHERE id = %s",
                (lab_id,)
            )
            lab = cursor.fetchone()
            
            if lab:
                self.redis.zincrby(f'lab:category_score:{lab["category"]}', score, user_id)
            
            # 更新月度分数
            month_key = f'lab:monthly_score:{datetime.now().strftime("%Y%m")}'
            self.redis.zincrby(month_key, score, user_id)
            
            # 设置月度分数的过期时间（3个月后）
            self.redis.expire(month_key, 90 * 24 * 3600)
            
        except Exception as e:
            system_logger.error(f"更新用户分数失败: {str(e)}", "ranking", {
                'user_id': user_id,
                'lab_id': lab_id,
                'score': score
            })
    
    def get_total_ranking(self, start: int = 0, limit: int = 10) -> Dict:
        """获取总分排行榜"""
        try:
            # 获取排名数据
            ranking_data = self.redis.zrevrange(
                'lab:total_score',
                start,
                start + limit - 1,
                withscores=True
            )
            
            # 获取用户信息
            user_ids = [int(uid) for uid, _ in ranking_data]
            if not user_ids:
                return {
                    'status': 'success',
                    'total': 0,
                    'ranking': []
                }
            
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 获取用户信息
            placeholders = ','.join(['%s'] * len(user_ids))
            cursor.execute(
                f"""
                SELECT id, username, avatar
                FROM users
                WHERE id IN ({placeholders})
                """,
                user_ids
            )
            users = {user['id']: user for user in cursor.fetchall()}
            
            # 构建排名列表
            ranking = []
            for rank, (user_id, score) in enumerate(ranking_data, start=start+1):
                user = users.get(int(user_id), {})
                ranking.append({
                    'rank': rank,
                    'user_id': int(user_id),
                    'username': user.get('username', 'Unknown'),
                    'avatar': user.get('avatar', ''),
                    'score': int(score)
                })
            
            return {
                'status': 'success',
                'total': self.redis.zcard('lab:total_score'),
                'ranking': ranking
            }
            
        except Exception as e:
            system_logger.error(f"获取总分排行榜失败: {str(e)}", "ranking")
            return {'status': 'error', 'message': str(e)}
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()
    
    def get_category_ranking(self, category: str, start: int = 0, limit: int = 10) -> Dict:
        """获取分类排行榜"""
        try:
            # 获取排名数据
            ranking_data = self.redis.zrevrange(
                f'lab:category_score:{category}',
                start,
                start + limit - 1,
                withscores=True
            )
            
            # 获取用户信息
            user_ids = [int(uid) for uid, _ in ranking_data]
            if not user_ids:
                return {
                    'status': 'success',
                    'category': category,
                    'total': 0,
                    'ranking': []
                }
            
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 获取用户信息
            placeholders = ','.join(['%s'] * len(user_ids))
            cursor.execute(
                f"""
                SELECT id, username, avatar
                FROM users
                WHERE id IN ({placeholders})
                """,
                user_ids
            )
            users = {user['id']: user for user in cursor.fetchall()}
            
            # 构建排名列表
            ranking = []
            for rank, (user_id, score) in enumerate(ranking_data, start=start+1):
                user = users.get(int(user_id), {})
                ranking.append({
                    'rank': rank,
                    'user_id': int(user_id),
                    'username': user.get('username', 'Unknown'),
                    'avatar': user.get('avatar', ''),
                    'score': int(score)
                })
            
            return {
                'status': 'success',
                'category': category,
                'total': self.redis.zcard(f'lab:category_score:{category}'),
                'ranking': ranking
            }
            
        except Exception as e:
            system_logger.error(f"获取分类排行榜失败: {str(e)}", "ranking", {
                'category': category
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()
    
    def get_monthly_ranking(self, year_month: str = None, start: int = 0, limit: int = 10) -> Dict:
        """获取月度排行榜"""
        try:
            if not year_month:
                year_month = datetime.now().strftime("%Y%m")
            
            # 获取排名数据
            ranking_data = self.redis.zrevrange(
                f'lab:monthly_score:{year_month}',
                start,
                start + limit - 1,
                withscores=True
            )
            
            # 获取用户信息
            user_ids = [int(uid) for uid, _ in ranking_data]
            if not user_ids:
                return {
                    'status': 'success',
                    'year_month': year_month,
                    'total': 0,
                    'ranking': []
                }
            
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 获取用户信息
            placeholders = ','.join(['%s'] * len(user_ids))
            cursor.execute(
                f"""
                SELECT id, username, avatar
                FROM users
                WHERE id IN ({placeholders})
                """,
                user_ids
            )
            users = {user['id']: user for user in cursor.fetchall()}
            
            # 构建排名列表
            ranking = []
            for rank, (user_id, score) in enumerate(ranking_data, start=start+1):
                user = users.get(int(user_id), {})
                ranking.append({
                    'rank': rank,
                    'user_id': int(user_id),
                    'username': user.get('username', 'Unknown'),
                    'avatar': user.get('avatar', ''),
                    'score': int(score)
                })
            
            return {
                'status': 'success',
                'year_month': year_month,
                'total': self.redis.zcard(f'lab:monthly_score:{year_month}'),
                'ranking': ranking
            }
            
        except Exception as e:
            system_logger.error(f"获取月度排行榜失败: {str(e)}", "ranking", {
                'year_month': year_month
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()
    
    def get_user_ranking(self, user_id: int) -> Dict:
        """获取用户的排名信息"""
        try:
            result = {
                'status': 'success',
                'rankings': {}
            }
            
            # 获取总分排名
            total_score = self.redis.zscore('lab:total_score', user_id)
            if total_score is not None:
                total_rank = self.redis.zrevrank('lab:total_score', user_id)
                result['rankings']['total'] = {
                    'score': int(total_score),
                    'rank': int(total_rank) + 1 if total_rank is not None else None
                }
            
            # 获取分类排名
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT DISTINCT category FROM labs")
            categories = [row['category'] for row in cursor.fetchall()]
            
            for category in categories:
                score = self.redis.zscore(f'lab:category_score:{category}', user_id)
                if score is not None:
                    rank = self.redis.zrevrank(f'lab:category_score:{category}', user_id)
                    result['rankings'][category] = {
                        'score': int(score),
                        'rank': int(rank) + 1 if rank is not None else None
                    }
            
            # 获取月度排名
            year_month = datetime.now().strftime("%Y%m")
            monthly_score = self.redis.zscore(f'lab:monthly_score:{year_month}', user_id)
            if monthly_score is not None:
                monthly_rank = self.redis.zrevrank(f'lab:monthly_score:{year_month}', user_id)
                result['rankings']['monthly'] = {
                    'year_month': year_month,
                    'score': int(monthly_score),
                    'rank': int(monthly_rank) + 1 if monthly_rank is not None else None
                }
            
            return result
            
        except Exception as e:
            system_logger.error(f"获取用户排名失败: {str(e)}", "ranking", {
                'user_id': user_id
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            if 'conn' in locals():
                cursor.close()
                conn.close()
    
    def sync_rankings(self):
        """同步排行榜数据（从数据库同步到Redis）"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 清空现有排行榜数据
            for key in self.redis.keys('lab:*_score:*'):
                self.redis.delete(key)
            
            # 获取所有完成的实验实例
            cursor.execute(
                """
                SELECT 
                    li.user_id,
                    l.category,
                    li.score,
                    li.end_time
                FROM lab_instances li
                JOIN labs l ON li.lab_id = l.id
                WHERE li.status = 'completed' AND li.score > 0
                """
            )
            instances = cursor.fetchall()
            
            # 更新排行榜数据
            for instance in instances:
                # 更新总分
                self.redis.zincrby('lab:total_score', instance['score'], instance['user_id'])
                
                # 更新分类分数
                self.redis.zincrby(
                    f'lab:category_score:{instance["category"]}',
                    instance['score'],
                    instance['user_id']
                )
                
                # 更新月度分数
                year_month = instance['end_time'].strftime("%Y%m")
                if (datetime.now() - instance['end_time']) < timedelta(days=90):
                    self.redis.zincrby(
                        f'lab:monthly_score:{year_month}',
                        instance['score'],
                        instance['user_id']
                    )
            
            return {'status': 'success', 'message': '排行榜数据同步成功'}
            
        except Exception as e:
            system_logger.error(f"同步排行榜数据失败: {str(e)}", "ranking")
            return {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()

# 创建排行榜管理器实例
lab_ranking = LabRanking() 