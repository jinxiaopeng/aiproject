from typing import Dict, List, Optional
from datetime import datetime
import mysql.connector
import json
import os
from pathlib import Path

from config import DB_CONFIG, UPLOAD_DIR
from core.logger import system_logger

class LabReport:
    """实验报告管理器"""
    
    def __init__(self):
        """初始化报告管理器"""
        self.upload_dir = Path(UPLOAD_DIR) / 'reports'
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        system_logger.info("实验报告管理器初始化成功", "report")
    
    def get_report(self, report_id: int) -> Dict:
        """获取实验报告详情"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 获取报告基本信息
            cursor.execute(
                """
                SELECT 
                    r.*,
                    l.name as lab_name,
                    l.category,
                    l.difficulty,
                    u.username as author
                FROM lab_reports r
                JOIN lab_instances li ON r.instance_id = li.id
                JOIN labs l ON li.lab_id = l.id
                JOIN users u ON li.user_id = u.id
                WHERE r.id = %s
                """,
                (report_id,)
            )
            report = cursor.fetchone()
            
            if not report:
                return {
                    'status': 'error',
                    'message': '报告不存在'
                }
            
            # 获取报告评论
            cursor.execute(
                """
                SELECT 
                    c.*,
                    u.username as commenter
                FROM report_comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.report_id = %s
                ORDER BY c.created_at
                """,
                (report_id,)
            )
            comments = cursor.fetchall()
            
            # 处理附件路径
            attachments = json.loads(report['attachments'])
            for attachment in attachments:
                attachment['url'] = f"/api/reports/attachments/{attachment['filename']}"
            
            return {
                'status': 'success',
                'report': {
                    'id': report['id'],
                    'lab_name': report['lab_name'],
                    'category': report['category'],
                    'difficulty': report['difficulty'],
                    'author': report['author'],
                    'content': report['content'],
                    'findings': report['findings'],
                    'conclusion': report['conclusion'],
                    'attachments': attachments,
                    'score': report['score'],
                    'submitted_at': report['submitted_at'].isoformat(),
                    'comments': [
                        {
                            'id': comment['id'],
                            'content': comment['content'],
                            'commenter': comment['commenter'],
                            'created_at': comment['created_at'].isoformat()
                        }
                        for comment in comments
                    ]
                }
            }
            
        except Exception as e:
            system_logger.error(f"获取实验报告失败: {str(e)}", "report", {
                'report_id': report_id
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def get_user_reports(self, user_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """获取用户的实验报告列表"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 获取总数
            cursor.execute(
                """
                SELECT COUNT(*) as total
                FROM lab_reports r
                JOIN lab_instances li ON r.instance_id = li.id
                WHERE li.user_id = %s
                """,
                (user_id,)
            )
            total = cursor.fetchone()['total']
            
            # 获取分页数据
            cursor.execute(
                """
                SELECT 
                    r.*,
                    l.name as lab_name,
                    l.category,
                    l.difficulty
                FROM lab_reports r
                JOIN lab_instances li ON r.instance_id = li.id
                JOIN labs l ON li.lab_id = l.id
                WHERE li.user_id = %s
                ORDER BY r.submitted_at DESC
                LIMIT %s OFFSET %s
                """,
                (user_id, per_page, (page - 1) * per_page)
            )
            reports = cursor.fetchall()
            
            return {
                'status': 'success',
                'total': total,
                'page': page,
                'per_page': per_page,
                'reports': [
                    {
                        'id': report['id'],
                        'lab_name': report['lab_name'],
                        'category': report['category'],
                        'difficulty': report['difficulty'],
                        'score': report['score'],
                        'submitted_at': report['submitted_at'].isoformat()
                    }
                    for report in reports
                ]
            }
            
        except Exception as e:
            system_logger.error(f"获取用户报告列表失败: {str(e)}", "report", {
                'user_id': user_id
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
    
    async def save_attachment(self, report_id: int, file: Dict) -> Dict:
        """保存报告附件"""
        try:
            # 生成文件名
            filename = f"{report_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file['filename']}"
            file_path = self.upload_dir / filename
            
            # 保存文件
            with open(file_path, 'wb') as f:
                f.write(file['content'])
            
            # 更新数据库
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                """
                SELECT attachments FROM lab_reports
                WHERE id = %s
                """,
                (report_id,)
            )
            report = cursor.fetchone()
            
            if not report:
                return {
                    'status': 'error',
                    'message': '报告不存在'
                }
            
            # 更新附件列表
            attachments = json.loads(report['attachments'])
            attachments.append({
                'filename': filename,
                'original_name': file['filename'],
                'size': len(file['content']),
                'mime_type': file['content_type']
            })
            
            cursor.execute(
                """
                UPDATE lab_reports
                SET attachments = %s
                WHERE id = %s
                """,
                (json.dumps(attachments), report_id)
            )
            conn.commit()
            
            return {
                'status': 'success',
                'message': '附件上传成功',
                'filename': filename
            }
            
        except Exception as e:
            system_logger.error(f"保存报告附件失败: {str(e)}", "report", {
                'report_id': report_id,
                'filename': file['filename']
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def add_comment(self, report_id: int, user_id: int, content: str) -> Dict:
        """添加报告评论"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                """
                INSERT INTO report_comments
                (report_id, user_id, content, created_at)
                VALUES (%s, %s, %s, %s)
                """,
                (report_id, user_id, content, datetime.now())
            )
            conn.commit()
            
            # 获取评论信息
            cursor.execute(
                """
                SELECT 
                    c.*,
                    u.username as commenter
                FROM report_comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.id = LAST_INSERT_ID()
                """
            )
            comment = cursor.fetchone()
            
            return {
                'status': 'success',
                'comment': {
                    'id': comment['id'],
                    'content': comment['content'],
                    'commenter': comment['commenter'],
                    'created_at': comment['created_at'].isoformat()
                }
            }
            
        except Exception as e:
            system_logger.error(f"添加报告评论失败: {str(e)}", "report", {
                'report_id': report_id,
                'user_id': user_id
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def update_score(self, report_id: int, score: int, feedback: str = None) -> Dict:
        """更新报告评分"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                """
                UPDATE lab_reports
                SET score = %s, feedback = %s
                WHERE id = %s
                """,
                (score, feedback, report_id)
            )
            
            # 同时更新实验实例的分数
            cursor.execute(
                """
                UPDATE lab_instances li
                JOIN lab_reports r ON li.id = r.instance_id
                SET li.score = %s
                WHERE r.id = %s
                """,
                (score, report_id)
            )
            
            conn.commit()
            return {
                'status': 'success',
                'message': '评分更新成功'
            }
            
        except Exception as e:
            system_logger.error(f"更新报告评分失败: {str(e)}", "report", {
                'report_id': report_id,
                'score': score
            })
            return {'status': 'error', 'message': str(e)}
        finally:
            cursor.close()
            conn.close()

# 创建报告管理器实例
lab_report = LabReport() 