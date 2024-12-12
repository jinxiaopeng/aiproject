import asyncio
from typing import Dict, List
import docker
import psutil
from datetime import datetime

from core.logger import system_logger
from config import DB_CONFIG
import mysql.connector

class LabMonitor:
    """实验环境监控器"""
    
    def __init__(self):
        """初始化监控器"""
        self.docker_client = docker.from_env()
        self.monitoring_data = {}
        system_logger.info("实验环境监控器初始化成功", "monitor")
    
    async def start_monitoring(self, instance_id: str):
        """开始监控实例"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM lab_instances WHERE id = %s",
                (instance_id,)
            )
            instance = cursor.fetchone()
            
            if not instance or instance['status'] != 'running':
                return
            
            # 初始化监控数据
            self.monitoring_data[instance_id] = {
                'start_time': datetime.now(),
                'container_id': instance['container_id'],
                'metrics': []
            }
            
            # 开始收集指标
            while True:
                try:
                    container = self.docker_client.containers.get(instance['container_id'])
                    stats = container.stats(stream=False)
                    
                    # 计算CPU使用率
                    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                              stats['precpu_stats']['cpu_usage']['total_usage']
                    system_cpu_delta = stats['cpu_stats']['system_cpu_usage'] - \
                                     stats['precpu_stats']['system_cpu_usage']
                    cpu_usage = (cpu_delta / system_cpu_delta) * 100.0
                    
                    # 计算内存使用率
                    memory_usage = stats['memory_stats']['usage']
                    memory_limit = stats['memory_stats']['limit']
                    memory_percent = (memory_usage / memory_limit) * 100.0
                    
                    # 计算网络使用情况
                    network_rx = stats['networks']['eth0']['rx_bytes']
                    network_tx = stats['networks']['eth0']['tx_bytes']
                    
                    # 记录指标
                    metric = {
                        'timestamp': datetime.now().isoformat(),
                        'cpu_usage': round(cpu_usage, 2),
                        'memory_usage': memory_usage,
                        'memory_percent': round(memory_percent, 2),
                        'network_rx': network_rx,
                        'network_tx': network_tx
                    }
                    
                    self.monitoring_data[instance_id]['metrics'].append(metric)
                    
                    # 只保留最近1小时的数据
                    if len(self.monitoring_data[instance_id]['metrics']) > 3600:
                        self.monitoring_data[instance_id]['metrics'].pop(0)
                    
                    # 检查资源使用是否超限
                    if cpu_usage > 90 or memory_percent > 90:
                        system_logger.warning(f"实例资源使用超限", "monitor", {
                            'instance_id': instance_id,
                            'cpu_usage': cpu_usage,
                            'memory_percent': memory_percent
                        })
                    
                    # 每5秒收集一次数据
                    await asyncio.sleep(5)
                    
                except docker.errors.NotFound:
                    system_logger.error(f"容器不存在", "monitor", {
                        'instance_id': instance_id,
                        'container_id': instance['container_id']
                    })
                    break
                except Exception as e:
                    system_logger.error(f"监控数据收集失败: {str(e)}", "monitor", {
                        'instance_id': instance_id
                    })
                    await asyncio.sleep(5)
                    continue
                
        except Exception as e:
            system_logger.error(f"启动监控失败: {str(e)}", "monitor", {
                'instance_id': instance_id
            })
        finally:
            cursor.close()
            conn.close()
    
    def stop_monitoring(self, instance_id: str):
        """停止监控实例"""
        if instance_id in self.monitoring_data:
            del self.monitoring_data[instance_id]
    
    def get_monitoring_data(self, instance_id: str, duration: int = 3600) -> Dict:
        """获取监控数据
        
        Args:
            instance_id: 实例ID
            duration: 获取最近多少秒的数据，默认1小时
        """
        if instance_id not in self.monitoring_data:
            return {
                'status': 'not_monitoring',
                'message': '未监控该实例'
            }
        
        data = self.monitoring_data[instance_id]
        metrics = data['metrics']
        
        if not metrics:
            return {
                'status': 'no_data',
                'message': '暂无监控数据'
            }
        
        # 计算平均值
        cpu_usage = sum(m['cpu_usage'] for m in metrics) / len(metrics)
        memory_percent = sum(m['memory_percent'] for m in metrics) / len(metrics)
        
        # 获取最新值
        latest = metrics[-1]
        
        return {
            'status': 'success',
            'start_time': data['start_time'].isoformat(),
            'latest': latest,
            'summary': {
                'avg_cpu_usage': round(cpu_usage, 2),
                'avg_memory_percent': round(memory_percent, 2),
                'total_network_rx': latest['network_rx'],
                'total_network_tx': latest['network_tx']
            },
            'metrics': metrics[-duration:]  # 只返回指定时间段的数据
        }
    
    def get_system_metrics(self) -> Dict:
        """获取系统整体指标"""
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # 内存使用情况
            memory = psutil.virtual_memory()
            
            # 磁盘使用情况
            disk = psutil.disk_usage('/')
            
            # 网络IO
            net_io = psutil.net_io_counters()
            
            return {
                'status': 'success',
                'metrics': {
                    'cpu_percent': cpu_percent,
                    'memory': {
                        'total': memory.total,
                        'used': memory.used,
                        'percent': memory.percent
                    },
                    'disk': {
                        'total': disk.total,
                        'used': disk.used,
                        'percent': disk.percent
                    },
                    'network': {
                        'bytes_sent': net_io.bytes_sent,
                        'bytes_recv': net_io.bytes_recv,
                        'packets_sent': net_io.packets_sent,
                        'packets_recv': net_io.packets_recv
                    }
                }
            }
        except Exception as e:
            system_logger.error(f"获取系统指标失败: {str(e)}", "monitor")
            return {
                'status': 'error',
                'message': str(e)
            }

# 创建监控器实例
lab_monitor = LabMonitor() 