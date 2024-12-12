import psutil
import time
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import get_db
from ..realtime.models import RealtimeMonitor

class SystemMetricsCollector:
    def __init__(self):
        self.db = next(get_db())

    def collect_metrics(self, user_id: int) -> None:
        """收集系统资源使用情况"""
        try:
            # CPU使用率
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # 内存使用率
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            
            # 磁盘使用率
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent
            
            # 网络流量 (MB/s)
            net_io = psutil.net_io_counters()
            time.sleep(1)  # 等待1秒以计算速率
            net_io_after = psutil.net_io_counters()
            
            network_in = (net_io_after.bytes_recv - net_io.bytes_recv) / 1024 / 1024  # MB/s
            network_out = (net_io_after.bytes_sent - net_io.bytes_sent) / 1024 / 1024  # MB/s
            
            # 系统负载
            load_avg = psutil.getloadavg()[0]  # 1分钟负载
            
            # 进程数
            process_count = len(psutil.pids())
            
            # 创建监控记录
            monitor_record = RealtimeMonitor(
                user_id=user_id,
                cpu_usage=cpu_usage,
                memory_usage=memory_usage,
                disk_usage=disk_usage,
                network_in=network_in,
                network_out=network_out,
                system_load=load_avg,
                process_count=process_count,
                node_name='primary',
                timestamp=datetime.now()
            )
            
            self.db.add(monitor_record)
            self.db.commit()
            
        except Exception as e:
            print(f"Error collecting system metrics: {str(e)}")
            self.db.rollback()
        finally:
            self.db.close()

def start_collector(user_id: int, interval: int = 30):
    """启动系统资源监控收集器"""
    collector = SystemMetricsCollector()
    
    while True:
        try:
            collector.collect_metrics(user_id)
            time.sleep(interval)
        except KeyboardInterrupt:
            print("Stopping system metrics collector...")
            break
        except Exception as e:
            print(f"Collector error: {str(e)}")
            time.sleep(interval)

if __name__ == "__main__":
    # 测试收集器
    USER_ID = 1  # 测试用户ID
    start_collector(USER_ID) 