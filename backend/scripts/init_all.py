"""
统一的靶场数据库初始化入口脚本
"""

import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from backend.scripts.init_challenge_dbs import init_challenge_dbs

logger = logging.getLogger(__name__)

def init_all():
    """初始化所有靶场数据库"""
    try:
        # 1. 创建靶场数据库和用户
        logger.info("Creating challenge databases and users...")
        init_challenge_dbs()
        
        # 2. 初始化各个靶场数据库
        challenges_dir = project_root / "challenges"
        
        # SQL注入靶场
        logger.info("Initializing SQL injection challenge database...")
        sql_injection_dir = challenges_dir / "web_security/sql_injection"
        if sql_injection_dir.exists():
            os.chdir(sql_injection_dir)
            os.system("python init_db.py")
        
        # XSS靶场
        logger.info("Initializing XSS challenge database...")
        xss_dir = challenges_dir / "web_security/xss"
        if xss_dir.exists():
            os.chdir(xss_dir)
            os.system("python init_db.py")
        
        # 文件上传靶场
        logger.info("Initializing File upload challenge database...")
        file_upload_dir = challenges_dir / "web_security/file_upload"
        if file_upload_dir.exists():
            os.chdir(file_upload_dir)
            os.system("python init_db.py")
        
        logger.info("All challenge databases initialized successfully!")
        
    except Exception as e:
        logger.error(f"Error initializing databases: {str(e)}")
        raise

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    init_all() 