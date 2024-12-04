import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from config import LOG_CONFIG

# 确保日志目录存在
log_dir = Path(LOG_CONFIG['file']).parent
log_dir.mkdir(parents=True, exist_ok=True)

# 配置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 创建文件处理器
file_handler = logging.FileHandler(LOG_CONFIG['file'], encoding='utf-8')
file_handler.setFormatter(formatter)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 创建日志记录器
logger = logging.getLogger('system')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class SystemLogger:
    """系统日志记录器"""
    
    def __init__(self):
        self.logger = logger
    
    def _format_message(self, message: str, category: str, details: Optional[Dict[str, Any]] = None) -> str:
        """格式化日志消息"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'category': category,
            'message': message
        }
        if details:
            log_entry['details'] = details
        return json.dumps(log_entry, ensure_ascii=False)
    
    def debug(self, message: str, category: str = 'system', details: Optional[Dict[str, Any]] = None):
        """记录调试信息"""
        self.logger.debug(self._format_message(message, category, details))
    
    def info(self, message: str, category: str = 'system', details: Optional[Dict[str, Any]] = None):
        """记录一般信息"""
        self.logger.info(self._format_message(message, category, details))
    
    def warning(self, message: str, category: str = 'system', details: Optional[Dict[str, Any]] = None):
        """记录警告信息"""
        self.logger.warning(self._format_message(message, category, details))
    
    def error(self, message: str, category: str = 'system', details: Optional[Dict[str, Any]] = None):
        """记录错误信息"""
        self.logger.error(self._format_message(message, category, details))
    
    def critical(self, message: str, category: str = 'system', details: Optional[Dict[str, Any]] = None):
        """记录严重错误信息"""
        self.logger.critical(self._format_message(message, category, details))

# 创建系统日志记录器实例
system_logger = SystemLogger() 