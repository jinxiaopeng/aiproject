"""
资源监控模块
负责监控进程的资源使用情况
"""

import psutil
import logging
from typing import Dict, Optional
from datetime import datetime

from ..services.notification_service import notification_service
from ..models.challenge import Challenge

logger = logging.getLogger(__name__)

class ResourceMonitor:
    def __init__(self):
        self.processes: Dict[str, int] = {}  # challenge_id -> pid
        self.stats: Dict[str, Dict] = {}     # challenge_id -> stats
        
        # 告警阈值（百分比）
        self.warning_thresholds = {
            'cpu': 80.0,     # CPU使用率超过80%告警
            'memory': 80.0   # 内存使用率超过80%告警
        }
        
        # 告警冷却时间（秒）
        self.warning_cooldown = 300  # 5分钟内不重复告警
        
        # 记录上次告警时间
        self.last_warnings: Dict[str, Dict[str, datetime]] = {}
    
    def register_process(self, challenge_id: str, pid: int):
        """注册进程到监控系统"""
        self.processes[challenge_id] = pid
        self.stats[challenge_id] = {
            'last_update': datetime.now(),
            'cpu_percent': 0,
            'memory_percent': 0,
            'memory_info': None,
            'io_counters': None
        }
        self.last_warnings[challenge_id] = {}
        logger.info(f"Registered process {pid} for challenge {challenge_id}")
    
    def unregister_process(self, challenge_id: str):
        """从监控系统中移除进程"""
        self.processes.pop(challenge_id, None)
        self.stats.pop(challenge_id, None)
        self.last_warnings.pop(challenge_id, None)
    
    async def get_process_stats(self, challenge_id: str) -> Optional[Dict]:
        """获取进程的资源使用统计"""
        pid = self.processes.get(challenge_id)
        if not pid:
            return None
            
        try:
            process = psutil.Process(pid)
            
            # 更新统计信息
            stats = {
                'cpu_percent': process.cpu_percent(),
                'memory_percent': process.memory_percent(),
                'memory_info': process.memory_info()._asdict(),
                'io_counters': process.io_counters()._asdict() if hasattr(process, 'io_counters') else None,
                'last_update': datetime.now()
            }
            
            self.stats[challenge_id].update(stats)
            
            # 检查资源告警
            await self._check_resource_warnings(challenge_id, stats)
            
            return self.stats[challenge_id]
            
        except psutil.NoSuchProcess:
            logger.warning(f"Process {pid} for challenge {challenge_id} no longer exists")
            self.unregister_process(challenge_id)
            return None
        except Exception as e:
            logger.error(f"Error getting stats for process {pid}: {str(e)}")
            return None
    
    def is_process_running(self, challenge_id: str) -> bool:
        """检查进程是否仍在运行"""
        pid = self.processes.get(challenge_id)
        if not pid:
            return False
            
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except psutil.NoSuchProcess:
            return False
    
    def get_resource_usage(self, challenge_id: str) -> Dict:
        """获取资源使用情况的详细信息"""
        stats = self.stats.get(challenge_id)
        if not stats:
            return {
                'status': 'stopped',
                'cpu_percent': 0,
                'memory_percent': 0,
                'memory_usage': 0,
                'io_read_bytes': 0,
                'io_write_bytes': 0
            }
        
        return {
            'status': 'running',
            'cpu_percent': stats['cpu_percent'],
            'memory_percent': stats['memory_percent'],
            'memory_usage': stats['memory_info']['rss'] if stats['memory_info'] else 0,
            'io_read_bytes': stats['io_counters']['read_bytes'] if stats['io_counters'] else 0,
            'io_write_bytes': stats['io_counters']['write_bytes'] if stats['io_counters'] else 0,
            'last_update': stats['last_update'].isoformat()
        }
    
    async def _check_resource_warnings(self, challenge_id: str, stats: Dict):
        """检查资源使用是否需要告警"""
        try:
            current_time = datetime.now()
            last_warnings = self.last_warnings.get(challenge_id, {})
            
            # 检查CPU使用率
            if stats['cpu_percent'] >= self.warning_thresholds['cpu']:
                last_cpu_warning = last_warnings.get('cpu')
                if not last_cpu_warning or (current_time - last_cpu_warning).total_seconds() > self.warning_cooldown:
                    await self._send_resource_warning(challenge_id, 'cpu', stats['cpu_percent'])
                    last_warnings['cpu'] = current_time
            
            # 检查内存使用率
            if stats['memory_percent'] >= self.warning_thresholds['memory']:
                last_memory_warning = last_warnings.get('memory')
                if not last_memory_warning or (current_time - last_memory_warning).total_seconds() > self.warning_cooldown:
                    await self._send_resource_warning(challenge_id, 'memory', stats['memory_percent'])
                    last_warnings['memory'] = current_time
            
            self.last_warnings[challenge_id] = last_warnings
            
        except Exception as e:
            logger.error(f"Error checking resource warnings: {str(e)}")
    
    async def _send_resource_warning(self, challenge_id: str, resource_type: str, current_value: float):
        """发送资源告警"""
        try:
            challenge = Challenge.get_by_id(int(challenge_id))
            if challenge and challenge.created_by:
                await notification_service.send_resource_warning(
                    challenge.created_by,
                    int(challenge_id),
                    resource_type,
                    current_value,
                    self.warning_thresholds[resource_type]
                )
        except Exception as e:
            logger.error(f"Error sending resource warning: {str(e)}")