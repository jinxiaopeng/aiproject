import asyncio
import logging
from datetime import datetime
from typing import Dict, List
import json
import os

from .collector.network_collector import NetworkCollector
from .analyzer.threat_analyzer import ThreatAnalyzer

class MonitorService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        self.network_collector = NetworkCollector()
        self.threat_analyzer = ThreatAnalyzer()
        self.is_running = False
        self.monitoring_interval = 30  # 监控间隔（秒）
        
    def _setup_logging(self):
        """设置日志记录"""
        try:
            # 确保日志目录存在
            log_dir = os.path.join(os.path.dirname(__file__), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            # 设置日志格式
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
            # 文件处理器
            log_file = os.path.join(log_dir, 'monitor.log')
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            
            # 控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.INFO)
            
            # 配置根日志记录器
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.INFO)
            root_logger.addHandler(file_handler)
            root_logger.addHandler(console_handler)
            
            self.logger.info("Logging setup completed")
        except Exception as e:
            print(f"Failed to setup logging: {str(e)}")
            raise

    async def start(self):
        """启动监控服务"""
        try:
            self.logger.info("Starting monitor service...")
            self.is_running = True
            
            # 启动数据包捕获
            asyncio.create_task(self._start_packet_capture())
            
            # 主监控循环
            while self.is_running:
                try:
                    # 收集网络数据
                    network_data = await self.network_collector.collect_network_data()
                    
                    # 分析威胁
                    threats = self.threat_analyzer.analyze_network_data(network_data)
                    
                    # 处理检测到的威胁
                    if threats:
                        await self._handle_threats(threats)
                    
                    # 获取并保存威胁摘要
                    summary = self.threat_analyzer.get_threat_summary()
                    await self._save_threat_summary(summary)
                    
                    # 等待下一个监控周期
                    await asyncio.sleep(self.monitoring_interval)
                except Exception as e:
                    self.logger.error(f"Error in monitoring loop: {str(e)}")
                    await asyncio.sleep(5)  # 发生错误时短暂暂停
            
            self.logger.info("Monitor service stopped")
        except Exception as e:
            self.logger.error(f"Failed to start monitor service: {str(e)}")
            raise

    async def stop(self):
        """停止监控服务"""
        try:
            self.logger.info("Stopping monitor service...")
            self.is_running = False
        except Exception as e:
            self.logger.error(f"Failed to stop monitor service: {str(e)}")
            raise

    async def _start_packet_capture(self):
        """启动数据包捕获"""
        try:
            # 在单独的线程中运行数据包捕获
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.network_collector.start_packet_capture)
        except Exception as e:
            self.logger.error(f"Failed to start packet capture: {str(e)}")

    async def _handle_threats(self, threats: List[Dict]):
        """处理检测到的威胁"""
        try:
            for threat in threats:
                # 记录威胁
                self.logger.warning(f"Threat detected: {json.dumps(threat, indent=2)}")
                
                # 保存威胁记录
                await self._save_threat(threat)
                
                # 根据威胁级别采取相应措施
                if threat['level'] == 'high':
                    await self._handle_high_threat(threat)
                elif threat['level'] == 'medium':
                    await self._handle_medium_threat(threat)
                elif threat['level'] == 'low':
                    await self._handle_low_threat(threat)
        except Exception as e:
            self.logger.error(f"Failed to handle threats: {str(e)}")

    async def _save_threat(self, threat: Dict):
        """保存威胁记录"""
        try:
            # 确保目录存在
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            # 保存到文件
            threats_file = os.path.join(data_dir, 'threats.json')
            
            # 读取现有威胁
            threats = []
            if os.path.exists(threats_file):
                try:
                    with open(threats_file, 'r') as f:
                        threats = json.load(f)
                except json.JSONDecodeError:
                    self.logger.warning("Failed to load existing threats file")
            
            # 添加新威胁
            threats.append(threat)
            
            # 只保留最近1000条记录
            if len(threats) > 1000:
                threats = threats[-1000:]
            
            # 保存更新后的威胁列表
            with open(threats_file, 'w') as f:
                json.dump(threats, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save threat: {str(e)}")

    async def _save_threat_summary(self, summary: Dict):
        """保存威胁摘要"""
        try:
            # 确保目录存在
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            # 保存到文件
            summary_file = os.path.join(data_dir, 'threat_summary.json')
            with open(summary_file, 'w') as f:
                json.dump(summary, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save threat summary: {str(e)}")

    async def _handle_high_threat(self, threat: Dict):
        """处理高级威胁"""
        try:
            self.logger.error(f"HIGH LEVEL THREAT DETECTED: {json.dumps(threat, indent=2)}")
            
            # 这里可以添加更多处理逻辑，比如：
            # - 发送紧急通知
            # - 采取自动防御措施
            # - 记录详细的威胁信息
            # - 触发其他安全措施
        except Exception as e:
            self.logger.error(f"Failed to handle high threat: {str(e)}")

    async def _handle_medium_threat(self, threat: Dict):
        """处理中级威胁"""
        try:
            self.logger.warning(f"Medium level threat detected: {json.dumps(threat, indent=2)}")
            
            # 这里可以添加更多处理逻辑，比如：
            # - 记录详细信息
            # - 进行进一步分析
            # - 准备可能的响应措施
        except Exception as e:
            self.logger.error(f"Failed to handle medium threat: {str(e)}")

    async def _handle_low_threat(self, threat: Dict):
        """处理低级威胁"""
        try:
            self.logger.info(f"Low level threat detected: {json.dumps(threat, indent=2)}")
            
            # 这里可以添加更多处理逻辑，比如：
            # - 记录基本信息
            # - 更新威胁统计
        except Exception as e:
            self.logger.error(f"Failed to handle low threat: {str(e)}")

    def get_status(self) -> Dict:
        """获取服务状态"""
        try:
            return {
                'is_running': self.is_running,
                'monitoring_interval': self.monitoring_interval,
                'last_update': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Failed to get status: {str(e)}")
            return {} 