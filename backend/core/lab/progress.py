from typing import Dict, List, Optional
from datetime import datetime
import mysql.connector
import json

from config import DB_CONFIG
from core.logger import system_logger

class LabProgress:
    """实验进度追踪器"""
    
    def __init__(self):
        """初始化进度追踪器"""
        system_logger.info("实验进度追踪器初始化成功", "progress")
    
    def get_user_progress(self, user_id: int) -> Dict:
        """获取用户的整体实验进度"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 获取用户完成的实验数量
            cursor.execute(
                """
                SELECT 
                    COUNT(DISTINCT lab_id) as completed_labs,
                    SUM(TIMESTAMPDIFF(MINUTE, start_time, end_time)) as total_time
                FROM lab_instances 
                WHERE user_id = %s AND status = 'completed'
                """,
                (user_id,)
            )
            progress = cursor.fetchone()
            
            # 获取用户的技能分布
            cursor.execute(
                """
                SELECT l.category, COUNT(*) as count
                FROM lab_instances li
                JOIN labs l ON li.lab_id = l.id
                WHERE li.user_id = %s AND li.status = 'completed'
                GROUP BY l.category
                """,
                (user_id,)
            )
            skills = cursor.fetchall()
            
            # 获取最近完成的实验
            cursor.execute(
                """
                SELECT 
                    l.name, l.category, l.difficulty,
                    li.start_time, li.end_time,
                    li.score, li.completion_rate
                FROM lab_instances li
                JOIN labs l ON li.lab_id = l.id
                WHERE li.user_id = %s AND li.status = 'completed'
                ORDER BY li.end_time DESC
                LIMIT 5
                """,
                (user_id,)
            )
            recent_labs = cursor.fetchall()
            
            return {
                'status': 'success',
                'progress': {
                    'completed_labs': progress['completed_labs'] or 0,
                    'total_time': progress['total_time'] or 0,
                    'skills': {
                        skill['category']: skill['count']
                        for skill in skills
                    }
                },
                'recent_labs': recent_labs
            }
            
        except Exception as e:
            system_logger.error(f"获取用户进度失败: {str(e)}", "progress", {
                'user_id': user_id
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def get_lab_progress(self, lab_id: int, user_id: int) -> Dict:
        """获取用户在特定实验中的进度"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 获取实验实例信息
            cursor.execute(
                """
                SELECT * FROM lab_instances 
                WHERE lab_id = %s AND user_id = %s
                ORDER BY start_time DESC LIMIT 1
                """,
                (lab_id, user_id)
            )
            instance = cursor.fetchone()
            
            if not instance:
                return {
                    'status': 'not_started',
                    'message': '未开始该实验'
                }
            
            # 获取实验步骤完成情况
            cursor.execute(
                """
                SELECT * FROM lab_steps
                WHERE instance_id = %s
                ORDER BY step_number
                """,
                (instance['id'],)
            )
            steps = cursor.fetchall()
            
            # 计算完成率
            total_steps = len(steps)
            completed_steps = sum(1 for step in steps if step['status'] == 'completed')
            completion_rate = (completed_steps / total_steps * 100) if total_steps > 0 else 0
            
            return {
                'status': 'success',
                'instance': {
                    'id': instance['id'],
                    'status': instance['status'],
                    'start_time': instance['start_time'].isoformat(),
                    'end_time': instance['end_time'].isoformat() if instance['end_time'] else None,
                    'score': instance['score'],
                    'completion_rate': completion_rate
                },
                'steps': [
                    {
                        'number': step['step_number'],
                        'title': step['title'],
                        'status': step['status'],
                        'completed_at': step['completed_at'].isoformat() if step['completed_at'] else None
                    }
                    for step in steps
                ]
            }
            
        except Exception as e:
            system_logger.error(f"获取实验进度失败: {str(e)}", "progress", {
                'lab_id': lab_id,
                'user_id': user_id
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def update_step_progress(self, instance_id: int, step_number: int, status: str) -> Dict:
        """更新实验步骤进度"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 更新步骤状态
            cursor.execute(
                """
                UPDATE lab_steps 
                SET status = %s, completed_at = %s
                WHERE instance_id = %s AND step_number = %s
                """,
                (status, datetime.now() if status == 'completed' else None,
                 instance_id, step_number)
            )
            
            # 检查是否所有步骤都完成了
            cursor.execute(
                """
                SELECT COUNT(*) as total, 
                       SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed
                FROM lab_steps
                WHERE instance_id = %s
                """,
                (instance_id,)
            )
            result = cursor.fetchone()
            
            # 如果所有步骤都完成了，更新实例状态
            if result['total'] == result['completed']:
                cursor.execute(
                    """
                    UPDATE lab_instances 
                    SET status = 'completed', 
                        end_time = %s,
                        completion_rate = 100
                    WHERE id = %s
                    """,
                    (datetime.now(), instance_id)
                )
            else:
                # 更新完成率
                completion_rate = (result['completed'] / result['total'] * 100)
                cursor.execute(
                    """
                    UPDATE lab_instances 
                    SET completion_rate = %s
                    WHERE id = %s
                    """,
                    (completion_rate, instance_id)
                )
            
            conn.commit()
            return {'status': 'success', 'message': '进度更新成功'}
            
        except Exception as e:
            system_logger.error(f"更新步骤进度失败: {str(e)}", "progress", {
                'instance_id': instance_id,
                'step_number': step_number
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def submit_lab_report(self, instance_id: int, report_data: Dict) -> Dict:
        """提交实验报告"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 检查是否已提交过报告
            cursor.execute(
                "SELECT * FROM lab_reports WHERE instance_id = %s",
                (instance_id,)
            )
            existing_report = cursor.fetchone()
            
            if existing_report:
                return {
                    'status': 'error',
                    'message': '已提交过实验报告'
                }
            
            # 保存报告
            cursor.execute(
                """
                INSERT INTO lab_reports 
                (instance_id, content, findings, conclusion, attachments, submitted_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (instance_id, report_data['content'], report_data['findings'],
                 report_data['conclusion'], json.dumps(report_data['attachments']),
                 datetime.now())
            )
            
            # 更新实验实例状态
            cursor.execute(
                """
                UPDATE lab_instances 
                SET status = 'completed', 
                    end_time = %s,
                    score = %s
                WHERE id = %s
                """,
                (datetime.now(), report_data.get('score', 0), instance_id)
            )
            
            conn.commit()
            return {'status': 'success', 'message': '实验报告提交成功'}
            
        except Exception as e:
            system_logger.error(f"提交实验报告失败: {str(e)}", "progress", {
                'instance_id': instance_id
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()

# 创建进度追踪器实例
lab_progress = LabProgress() 