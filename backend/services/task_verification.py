"""
任务验证服务
"""

import logging
from typing import Dict, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.challenge import Challenge
from ..models.training_progress import TrainingProgress
from ..models.user import User

logger = logging.getLogger(__name__)

class TaskVerificationService:
    @staticmethod
    def verify_flag(
        db: Session,
        user_id: int,
        challenge_id: int,
        flag: str
    ) -> Dict:
        """验证flag"""
        # 获取靶场信息
        challenge = db.query(Challenge).get(challenge_id)
        if not challenge:
            raise ValueError("Challenge not found")

        # 获取训练进度
        progress = db.query(TrainingProgress).filter(
            and_(
                TrainingProgress.user_id == user_id,
                TrainingProgress.challenge_id == challenge_id
            )
        ).first()

        if not progress:
            raise ValueError("Training not started")

        # 检查flag
        if challenge.flag == flag:
            # 更新进度
            if not progress.completed_at:
                progress.completed_at = datetime.utcnow()
                
                # 更新用户积分
                user = db.query(User).get(user_id)
                if user:
                    user.points = (user.points or 0) + challenge.points
                
                # 更新靶场统计
                challenge.completions = (challenge.completions or 0) + 1
                total_attempts = db.query(TrainingProgress).filter(
                    TrainingProgress.challenge_id == challenge_id
                ).count()
                challenge.pass_rate = (challenge.completions / total_attempts) * 100
                
                db.commit()
            
            return {
                "correct": True,
                "points": challenge.points
            }
        else:
            return {
                "correct": False,
                "message": "Flag incorrect"
            }

    @staticmethod
    def verify_task(
        db: Session,
        user_id: int,
        challenge_id: int,
        step: int,
        task_index: int,
        result: Dict
    ) -> bool:
        """验证任务完成情况"""
        # 获取靶场信息
        challenge = db.query(Challenge).get(challenge_id)
        if not challenge or not challenge.steps:
            raise ValueError("Challenge or steps not found")

        # 验证步骤和任务索引
        if step >= len(challenge.steps):
            raise ValueError("Invalid step")
            
        step_data = challenge.steps[step]
        if not step_data.get('tasks') or task_index >= len(step_data['tasks']):
            raise ValueError("Invalid task")

        # 获取任务验证器
        task = step_data['tasks'][task_index]
        validator = task.get('validator')
        if not validator:
            # 如果没有验证器，默认通过
            return True

        try:
            # 执行验证
            if validator['type'] == 'regex':
                import re
                pattern = re.compile(validator['pattern'])
                return bool(pattern.match(str(result.get('answer', ''))))
                
            elif validator['type'] == 'script':
                # 执行Python验证脚本
                script = validator['script']
                local_vars = {'result': result, 'success': False}
                exec(script, {}, local_vars)
                return local_vars.get('success', False)
                
            else:
                raise ValueError(f"Unsupported validator type: {validator['type']}")
                
        except Exception as e:
            logger.error(f"Error validating task: {str(e)}")
            return False

    @staticmethod
    def get_task_hints(
        db: Session,
        challenge_id: int,
        step: int,
        task_index: int
    ) -> List[str]:
        """获取任务提示"""
        challenge = db.query(Challenge).get(challenge_id)
        if not challenge or not challenge.steps:
            raise ValueError("Challenge or steps not found")

        if step >= len(challenge.steps):
            raise ValueError("Invalid step")
            
        step_data = challenge.steps[step]
        if not step_data.get('tasks') or task_index >= len(step_data['tasks']):
            raise ValueError("Invalid task")

        task = step_data['tasks'][task_index]
        return task.get('hints', []) 