import logging
import os
from logging.handlers import RotatingFileHandler
from ..config import settings

def get_logger(name: str) -> logging.Logger:
    """
    获取配置好的logger实例
    
    Args:
        name: logger名称，通常使用模块名
        
    Returns:
        配置好的logger实例
    """
    logger = logging.getLogger(name)
    
    # 如果logger已经配置过，直接返回
    if logger.handlers:
        return logger
        
    # 设置日志级别
    logger.setLevel(settings.LOG_LEVEL)
    
    # 创建日志目录
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 文件处理器 - 按大小轮转
    log_file = os.path.join(log_dir, f'{name}.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    
    # 设置格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger