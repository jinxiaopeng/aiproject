import psutil
import logging
from typing import Dict
import socket
from datetime import datetime

class SystemCollector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._initialize()

    def _initialize(self):
        """初始化收集器"""
        try:
            # 获取本机主机名
            self.hostname = socket.gethostname()
            # 获取本机IP
            self.host_ip = socket.gethostbyname(self.hostname)
            self.logger.info(f"System collector initialized for {self.hostname} ({self.host_ip})")
        except Exception as e:
            self.logger.error(f"Failed to initialize system collector: {str(e)}")
            self.hostname = "unknown"
            self.host_ip = "0.0.0.0"

    async def collect_data(self) -> Dict:
        """收集系统数据"""
        try:
            return {
                'timestamp': datetime.now().isoformat(),
                'host': {
                    'hostname': self.hostname,
                    'ip': self.host_ip
                },
                'system': {
                    'cpu_usage': await self._get_cpu_usage(),
                    'memory_usage': await self._get_memory_usage(),
                    'disk_usage': await self._get_disk_usage()
                },
                'network': await self._get_network_stats(),
                'processes': await self._get_process_info()
            }
        except Exception as e:
            self.logger.error(f"Data collection failed: {str(e)}")
            return {}

    async def _get_cpu_usage(self) -> Dict:
        """获取CPU使用情况"""
        try:
            return {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
                'load_avg': psutil.getloadavg()
            }
        except Exception as e:
            self.logger.error(f"CPU data collection failed: {str(e)}")
            return {}

    async def _get_memory_usage(self) -> Dict:
        """获取内存使用情况"""
        try:
            mem = psutil.virtual_memory()
            return {
                'total': mem.total,
                'available': mem.available,
                'percent': mem.percent,
                'used': mem.used,
                'free': mem.free
            }
        except Exception as e:
            self.logger.error(f"Memory data collection failed: {str(e)}")
            return {}

    async def _get_disk_usage(self) -> Dict:
        """获取磁盘使用情况"""
        try:
            disk = psutil.disk_usage('/')
            return {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            }
        except Exception as e:
            self.logger.error(f"Disk data collection failed: {str(e)}")
            return {}

    async def _get_network_stats(self) -> Dict:
        """获取网络统计信息"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout,
                'dropin': net_io.dropin,
                'dropout': net_io.dropout
            }
        except Exception as e:
            self.logger.error(f"Network data collection failed: {str(e)}")
            return {}

    async def _get_process_info(self) -> Dict:
        """获取进程信息"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    if pinfo['cpu_percent'] > 0 or pinfo['memory_percent'] > 0:
                        processes.append(pinfo)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            return {
                'count': len(processes),
                'high_cpu': [p for p in processes if p['cpu_percent'] > 50],
                'high_memory': [p for p in processes if p['memory_percent'] > 50]
            }
        except Exception as e:
            self.logger.error(f"Process data collection failed: {str(e)}")
            return {} 