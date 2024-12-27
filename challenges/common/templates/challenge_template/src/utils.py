"""
靶场工具函数模板
"""

import os
import logging
from datetime import datetime

def setup_logging():
    """配置日志"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    
    # 创建文件处理器
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(
        log_dir, 
        f'challenge_{datetime.now().strftime("%Y%m%d")}.log'
    )
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def validate_flag(submitted_flag, correct_flag):
    """验证flag"""
    return submitted_flag.strip() == correct_flag.strip()

def get_challenge_status(start_time, timeout):
    """获取靶场状态"""
    if not start_time:
        return "not_started"
    
    elapsed = (datetime.utcnow() - start_time).total_seconds()
    if elapsed > timeout:
        return "timeout"
    
    return "in_progress" 