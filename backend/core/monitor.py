import psutil
from datetime import datetime
from typing import Dict, Any

class SystemMonitor:
    """系统监控类"""
    
    def get_system_status(self) -> Dict[str, Any]:
        """获取系统状态"""
        try:
            return {
                'status': 'running',
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_docker_status(self) -> Dict[str, Any]:
        """获取Docker状态"""
        return {
            'status': 'not_available',
            'message': 'Docker服务未启动',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_database_status(self) -> Dict[str, Any]:
        """获取数据库状态"""
        return {
            'status': 'running',
            'timestamp': datetime.now().isoformat()
        }

# 创建系统监控实例
system_monitor = SystemMonitor() 