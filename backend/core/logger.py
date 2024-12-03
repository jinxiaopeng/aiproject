import logging
import json
from datetime import datetime
from typing import Dict, Optional

class SystemLogger:
    def __init__(self):
        # 配置日志格式
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/system.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _log(self, level: str, message: str, component: Optional[str] = None, extra_data: Optional[Dict] = None):
        """记录日志的内部方法"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        
        if component:
            log_data['component'] = component
            
        if extra_data:
            log_data['extra'] = extra_data
            
        log_message = json.dumps(log_data, ensure_ascii=False)
        
        if level == 'DEBUG':
            self.logger.debug(log_message)
        elif level == 'INFO':
            self.logger.info(log_message)
        elif level == 'WARNING':
            self.logger.warning(log_message)
        elif level == 'ERROR':
            self.logger.error(log_message)
        elif level == 'CRITICAL':
            self.logger.critical(log_message)
    
    def debug(self, message: str, component: Optional[str] = None, extra_data: Optional[Dict] = None):
        """记录调试级别日志"""
        self._log('DEBUG', message, component, extra_data)
    
    def info(self, message: str, component: Optional[str] = None, extra_data: Optional[Dict] = None):
        """记录信息级别日志"""
        self._log('INFO', message, component, extra_data)
    
    def warning(self, message: str, component: Optional[str] = None, extra_data: Optional[Dict] = None):
        """记录警告级别日志"""
        self._log('WARNING', message, component, extra_data)
    
    def error(self, message: str, component: Optional[str] = None, extra_data: Optional[Dict] = None):
        """记录错误级别日志"""
        self._log('ERROR', message, component, extra_data)
    
    def critical(self, message: str, component: Optional[str] = None, extra_data: Optional[Dict] = None):
        """记录严重错误级别日志"""
        self._log('CRITICAL', message, component, extra_data)

# 创建全局日志记录器实例
system_logger = SystemLogger() 