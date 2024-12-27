from datetime import datetime
import logging
from typing import Dict, List, Optional
import asyncio
from backend.monitor_service.models.threat import ThreatLevel, ThreatEvent
from backend.monitor_service.database import SessionLocal
from backend.monitor_service.collector.system_collector import SystemCollector
from backend.monitor_service.core.notifier import Notifier
from backend.monitor_service.config.notification import SMTP_CONFIG

class ThreatDetector:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._detection_rules = []
        self._collector = SystemCollector()
        self._notifier = Notifier(SMTP_CONFIG)
        self._initialize_rules()

    def _initialize_rules(self):
        """初始化威胁检测规则"""
        # 基础规则集
        self._detection_rules = [
            self._check_network_anomaly,
            self._check_system_resources,
            self._check_process_anomaly
        ]

    async def _check_network_anomaly(self, data: Dict) -> Optional[ThreatEvent]:
        """检测网络异常"""
        try:
            network_data = data.get('network', {})
            # 检查网络错误率
            total_packets = network_data.get('packets_sent', 0) + network_data.get('packets_recv', 0)
            total_errors = network_data.get('errin', 0) + network_data.get('errout', 0)
            
            if total_packets > 0 and (total_errors / total_packets) > 0.01:  # 1%错误率阈值
                return ThreatEvent(
                    level=ThreatLevel.WARNING,
                    type="network_anomaly",
                    description="检测到异常的网络错误率",
                    timestamp=datetime.now(),
                    source_ip=data.get('host', {}).get('ip'),
                    details={
                        'error_rate': total_errors / total_packets,
                        'total_packets': total_packets,
                        'total_errors': total_errors
                    }
                )
        except Exception as e:
            self.logger.error(f"Network anomaly check failed: {str(e)}")
        return None

    async def _check_system_resources(self, data: Dict) -> Optional[ThreatEvent]:
        """检测系统资源异常"""
        try:
            system_data = data.get('system', {})
            cpu_usage = system_data.get('cpu_usage', {}).get('percent', 0)
            memory_usage = system_data.get('memory_usage', {}).get('percent', 0)
            disk_usage = system_data.get('disk_usage', {}).get('percent', 0)

            if cpu_usage > 90 or memory_usage > 90 or disk_usage > 90:
                return ThreatEvent(
                    level=ThreatLevel.MEDIUM,
                    type="resource_exhaustion",
                    description="系统资源使用率异常",
                    timestamp=datetime.now(),
                    source_ip=data.get('host', {}).get('ip'),
                    details={
                        'cpu_usage': cpu_usage,
                        'memory_usage': memory_usage,
                        'disk_usage': disk_usage
                    }
                )
        except Exception as e:
            self.logger.error(f"System resource check failed: {str(e)}")
        return None

    async def _check_process_anomaly(self, data: Dict) -> Optional[ThreatEvent]:
        """检测进程异常"""
        try:
            processes = data.get('processes', {})
            high_cpu_processes = processes.get('high_cpu', [])
            high_memory_processes = processes.get('high_memory', [])

            if len(high_cpu_processes) > 2 or len(high_memory_processes) > 2:
                return ThreatEvent(
                    level=ThreatLevel.WARNING,
                    type="process_anomaly",
                    description="检测到异常进程活动",
                    timestamp=datetime.now(),
                    source_ip=data.get('host', {}).get('ip'),
                    details={
                        'high_cpu_processes': high_cpu_processes,
                        'high_memory_processes': high_memory_processes
                    }
                )
        except Exception as e:
            self.logger.error(f"Process anomaly check failed: {str(e)}")
        return None

    async def start_monitoring(self):
        """启动威胁监控"""
        self._running = True
        self.logger.info("Threat detection service started")
        while self._running:
            try:
                # 获取监控数据
                data = await self._collector.collect_data()
                
                # 运行所有检测规则
                threats = []
                for rule in self._detection_rules:
                    threat = await rule(data)
                    if threat:
                        threats.append(threat)

                # 处理检测到的威胁
                if threats:
                    await self._handle_threats(threats)

                await asyncio.sleep(5)  # 检测间隔
            except Exception as e:
                self.logger.error(f"Monitoring error: {str(e)}")
                await asyncio.sleep(5)

    async def _handle_threats(self, threats: List[ThreatEvent]):
        """处理检测到的威胁"""
        try:
            db = SessionLocal()
            for threat in threats:
                # 保存威胁事件到数据库
                db.add(threat)
                
                # 发送通知
                self._notifier.notify(threat)
                
                # 根据威胁级别采取相应措施
                if threat.level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
                    await self._trigger_emergency_response(threat)
                
            db.commit()
        except Exception as e:
            self.logger.error(f"Failed to handle threats: {str(e)}")
        finally:
            db.close()

    async def _trigger_emergency_response(self, threat: ThreatEvent):
        """触发紧急响应"""
        self.logger.warning(f"Emergency response triggered for threat: {threat.type}")
        # TODO: 实现具体的应急响应措施
        # 1. 发送紧急通知（已通过notifier实现）
        # 2. 采取自动化防御措施
        # 3. 记录详细日志

    def stop_monitoring(self):
        """停止威胁监控"""
        self._running = False
        self.logger.info("Threat detection service stopped") 