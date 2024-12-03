from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
import mysql.connector
import schedule
import time
import threading
from pathlib import Path
import sys

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.append(str(backend_dir))

from config import DB_CONFIG
from core.monitor import system_monitor

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self._setup_jobs()
        
    def _setup_jobs(self):
        """设置定时任务"""
        # 每分钟记录系统指标
        self.scheduler.add_job(
            self._log_system_metrics,
            trigger=CronTrigger(minute='*'),
            id='system_metrics',
            name='Record system metrics'
        )
        
        # 每小时清理过期会话
        self.scheduler.add_job(
            self._cleanup_sessions,
            trigger=CronTrigger(hour='*'),
            id='session_cleanup',
            name='Clean up expired sessions'
        )
        
        # 每天凌晨2点清理过期的靶场容器
        self.scheduler.add_job(
            self._cleanup_lab_containers,
            trigger=CronTrigger(hour=2),
            id='container_cleanup',
            name='Clean up expired lab containers'
        )
        
        # 每周日凌晨3点进行数据库维护
        self.scheduler.add_job(
            self._database_maintenance,
            trigger=CronTrigger(day_of_week='sun', hour=3),
            id='db_maintenance',
            name='Database maintenance'
        )
        
    def start(self):
        """启动调度器"""
        try:
            self.scheduler.start()
            logger.info("Task scheduler started successfully")
        except Exception as e:
            logger.error(f"Failed to start task scheduler: {str(e)}")
            
    def shutdown(self):
        """关闭调度器"""
        try:
            self.scheduler.shutdown()
            logger.info("Task scheduler shut down successfully")
        except Exception as e:
            logger.error(f"Failed to shut down task scheduler: {str(e)}")
            
    def _log_system_metrics(self):
        """记录系统指标"""
        try:
            # 获取系统状态
            system_status = system_monitor.get_system_status()
            docker_status = system_monitor.get_docker_status()
            
            # 获取活跃用户数
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT COUNT(DISTINCT user_id) as active_users
                    FROM user_sessions
                    WHERE last_activity >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
                """)
                active_users = cursor.fetchone()[0]
                
                # 记录指标
                cursor.execute("""
                    INSERT INTO system_metrics (
                        cpu_percent, memory_percent, disk_percent,
                        docker_containers_running, docker_containers_total,
                        active_users, timestamp
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    system_status['cpu_percent'],
                    system_status['memory']['percent'],
                    system_status['disk']['percent'],
                    docker_status['status_count'].get('running', 0),
                    docker_status['status_count'].get('total', 0),
                    active_users,
                    datetime.now()
                ))
                conn.commit()
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"Failed to log system metrics: {str(e)}")
            
    def _cleanup_sessions(self):
        """清理过期会话"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            try:
                # 删除超过24小时未活动的会话
                cursor.execute("""
                    DELETE FROM user_sessions
                    WHERE last_activity < DATE_SUB(NOW(), INTERVAL 24 HOUR)
                """)
                conn.commit()
                logger.info(f"Cleaned up {cursor.rowcount} expired sessions")
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"Failed to clean up sessions: {str(e)}")
            
    def _cleanup_lab_containers(self):
        """清理过期的靶场容器"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            try:
                # 获取所有运行超过12小时的靶场记录
                cursor.execute("""
                    SELECT * FROM lab_usage
                    WHERE status = 'running'
                    AND start_time < DATE_SUB(NOW(), INTERVAL 12 HOUR)
                """)
                expired_labs = cursor.fetchall()
                
                for lab in expired_labs:
                    try:
                        # 停止容器
                        system_monitor.docker_client.containers.get(lab['container_id']).stop()
                        
                        # 更新状态
                        cursor.execute("""
                            UPDATE lab_usage
                            SET status = 'completed', end_time = NOW()
                            WHERE id = %s
                        """, (lab['id'],))
                        
                    except Exception as e:
                        logger.error(f"Failed to stop container {lab['container_id']}: {str(e)}")
                        
                conn.commit()
                logger.info(f"Cleaned up {len(expired_labs)} expired lab containers")
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"Failed to clean up lab containers: {str(e)}")
            
    def _database_maintenance(self):
        """数据库维护"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            try:
                # 优化表
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"OPTIMIZE TABLE {table_name}")
                    
                # 清理旧的系统指标数据
                cursor.execute("""
                    DELETE FROM system_metrics
                    WHERE timestamp < DATE_SUB(NOW(), INTERVAL 30 DAY)
                """)
                
                # 清理旧的系统事件日志
                cursor.execute("""
                    DELETE FROM system_events
                    WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY)
                """)
                
                conn.commit()
                logger.info("Database maintenance completed successfully")
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"Failed to perform database maintenance: {str(e)}")

# 创建全局调度器实例
task_scheduler = TaskScheduler() 