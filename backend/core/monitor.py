import psutil
import time
from datetime import datetime
from typing import Dict, Any
import logging
from prometheus_client import Counter, Gauge, Histogram
from config import DB_CONFIG

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests')
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')
ACTIVE_USERS = Gauge('active_users', 'Number of active users')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')
MEMORY_USAGE = Gauge('memory_usage_percent', 'Memory usage percentage')
DB_CONNECTIONS = Gauge('db_connections', 'Number of database connections')

class SystemMonitor:
    def __init__(self):
        self.start_time = datetime.now()
        
    def get_system_metrics(self) -> Dict[str, Any]:
        """获取系统指标"""
        try:
            metrics = {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'uptime': str(datetime.now() - self.start_time),
                'active_users': ACTIVE_USERS._value.get(),
                'request_count': REQUEST_COUNT._value.get()
            }
            
            # 更新Prometheus指标
            CPU_USAGE.set(metrics['cpu_percent'])
            MEMORY_USAGE.set(metrics['memory_percent'])
            
            return metrics
            
        except Exception as e:
            logger.error(f"获取系统指标失败: {str(e)}")
            return {}
    
    def get_database_metrics(self) -> Dict[str, Any]:
        """获取数据库指标"""
        try:
            # 这里可以添加数据库连接数、查询性能等指标
            metrics = {
                'connections': DB_CONNECTIONS._value.get(),
                'host': DB_CONFIG['host'],
                'database': DB_CONFIG['database']
            }
            return metrics
            
        except Exception as e:
            logger.error(f"获取数据库指标失败: {str(e)}")
            return {}
    
    def get_all_metrics(self) -> Dict[str, Any]:
        """获取所有监控指标"""
        return {
            'system': self.get_system_metrics(),
            'database': self.get_database_metrics(),
            'timestamp': datetime.now().isoformat()
        }

# 创建全局监控实例
system_monitor = SystemMonitor() 