"""
环境管理模块 - 处理靶场环境的基本设置
"""

import os
import shutil
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class EnvironmentManager:
    def __init__(self, base_dir: str = "challenges"):
        self.base_dir = base_dir
        self.work_dir = os.path.join(base_dir, "workspace")
        os.makedirs(self.work_dir, exist_ok=True)

    def setup_challenge(self, challenge_id: int) -> str:
        """设置靶场环境"""
        try:
            # 创建工作目录
            challenge_dir = os.path.join(self.work_dir, str(challenge_id))
            if os.path.exists(challenge_dir):
                shutil.rmtree(challenge_dir)
            os.makedirs(challenge_dir)

            # 复制靶场文件
            source_dir = os.path.join(self.base_dir, str(challenge_id))
            if not os.path.exists(source_dir):
                raise ValueError(f"Challenge {challenge_id} not found")

            shutil.copytree(source_dir, challenge_dir, dirs_exist_ok=True)
            
            return challenge_dir

        except Exception as e:
            logger.error(f"Error setting up challenge {challenge_id}: {str(e)}")
            raise

    def cleanup_challenge(self, challenge_id: int):
        """清理靶场环境"""
        try:
            challenge_dir = os.path.join(self.work_dir, str(challenge_id))
            if os.path.exists(challenge_dir):
                shutil.rmtree(challenge_dir)

        except Exception as e:
            logger.error(f"Error cleaning up challenge {challenge_id}: {str(e)}")
            raise

    def get_challenge_dir(self, challenge_id: int) -> Optional[str]:
        """获取靶场工作目录"""
        challenge_dir = os.path.join(self.work_dir, str(challenge_id))
        return challenge_dir if os.path.exists(challenge_dir) else None

    def prepare_env_vars(self, challenge_id: int, config: Dict) -> Dict:
        """准备环境变量"""
        env = os.environ.copy()
        
        # 添加基本环境变量
        env.update({
            'CHALLENGE_ID': str(challenge_id),
            'CHALLENGE_DIR': self.get_challenge_dir(challenge_id) or '',
            'PYTHONPATH': self.get_challenge_dir(challenge_id) or ''
        })

        # 添加配置中的环境变量
        if 'env' in config:
            env.update(config['env'])

        return env 