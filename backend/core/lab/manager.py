import docker
import logging
import os
import json
import time
import psutil
import prometheus_client
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import mysql.connector
from pathlib import Path

from config import CONFIG

# 配置日志
logger = logging.getLogger(__name__)

class LabManager:
    def __init__(self):
        """初始化实验管理器"""
        try:
            self.docker_client = docker.from_env()
            logger.info("Docker客户端初始化成功")
            
            # 初始化指标收集器
            self.metrics = {
                'container_count': prometheus_client.Gauge(
                    'lab_container_count',
                    'Number of running lab containers'
                ),
                'container_memory': prometheus_client.Gauge(
                    'lab_container_memory_bytes',
                    'Memory usage of lab containers'
                ),
                'container_cpu': prometheus_client.Gauge(
                    'lab_container_cpu_percent',
                    'CPU usage of lab containers'
                )
            }
            
        except Exception as e:
            logger.error(f"Docker客户端初始化失败: {str(e)}")
            self.docker_client = None
            self.metrics = None

    def _get_lab_config(self, lab_id: int) -> Optional[Dict]:
        """获取靶场配置"""
        try:
            conn = mysql.connector.connect(**CONFIG["database"])
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("""
                    SELECT * FROM labs 
                    WHERE id = %s AND status = 'active'
                """, (lab_id,))
                return cursor.fetchone()
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            logger.error(f"获取靶场配置失败: {str(e)}")
            return None

    def _update_instance_status(self, instance_id: int, status: str):
        """更新实例状态"""
        try:
            conn = mysql.connector.connect(**CONFIG["database"])
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE lab_instances 
                    SET status = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (status, instance_id))
                conn.commit()
            finally:
                cursor.close()
                conn.close()
        except Exception as e:
            logger.error(f"更新实例状态失败: {str(e)}")

    def start_lab(self, lab_id: int, user_id: int) -> Dict:
        """启动靶场环境"""
        try:
            if not self.docker_client:
                return {"status": "error", "message": "Docker服务不可用"}
                
            # 获取靶场配置
            lab_config = self._get_lab_config(lab_id)
            if not lab_config:
                return {"status": "error", "message": "靶场配置不存在"}
                
            # 检查用户是否已有运行中的实例
            conn = mysql.connector.connect(**CONFIG["database"])
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("""
                    SELECT * FROM lab_instances 
                    WHERE user_id = %s AND status = 'running'
                """, (user_id,))
                if cursor.fetchone():
                    return {"status": "error", "message": "已有运行中的实例"}
                
                # 创建容器
                container_name = f"lab_{lab_id}_{user_id}_{int(time.time())}"
                ports = json.loads(lab_config['ports']) if lab_config.get('ports') else {}
                env = json.loads(lab_config['environment']) if lab_config.get('environment') else {}
                
                container = self.docker_client.containers.run(
                    lab_config['image_name'],
                    name=container_name,
                    detach=True,
                    ports=ports,
                    environment=env,
                    remove=True
                )
                
                # 记录实例信息
                cursor.execute("""
                    INSERT INTO lab_instances 
                    (user_id, lab_id, container_id, status)
                    VALUES (%s, %s, %s, 'running')
                """, (user_id, lab_id, container.id))
                conn.commit()
                
                # 更新指标
                if self.metrics:
                    self.metrics['container_count'].inc()
                
                return {
                    "status": "success",
                    "container_id": container.id,
                    "ports": ports
                }
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"启动靶场失败: {str(e)}")
            return {"status": "error", "message": str(e)}

    def stop_lab(self, lab_id: int, user_id: int) -> Dict:
        """停止靶场环境"""
        try:
            if not self.docker_client:
                return {"status": "error", "message": "Docker服务不可用"}
                
            conn = mysql.connector.connect(**CONFIG["database"])
            cursor = conn.cursor(dictionary=True)
            try:
                # 获取实例信息
                cursor.execute("""
                    SELECT * FROM lab_instances 
                    WHERE user_id = %s AND lab_id = %s AND status = 'running'
                """, (user_id, lab_id))
                instance = cursor.fetchone()
                
                if not instance:
                    return {"status": "error", "message": "未找到运行中的实例"}
                
                # 停止容器
                try:
                    container = self.docker_client.containers.get(instance['container_id'])
                    container.stop()
                except docker.errors.NotFound:
                    pass  # 容器可能已经不存在
                
                # 更新实例状态
                cursor.execute("""
                    UPDATE lab_instances 
                    SET status = 'stopped', updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (instance['id'],))
                conn.commit()
                
                # 更新指标
                if self.metrics:
                    self.metrics['container_count'].dec()
                
                return {"status": "success", "message": "靶场环境已停止"}
                
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"停止靶场失败: {str(e)}")
            return {"status": "error", "message": str(e)}

    def get_lab_status(self, lab_id: int, user_id: int) -> Dict:
        """获取靶场状态"""
        try:
            if not self.docker_client:
                return {"status": "error", "message": "Docker服务不可用"}
                
            conn = mysql.connector.connect(**CONFIG["database"])
            cursor = conn.cursor(dictionary=True)
            try:
                # 获取实例信息
                cursor.execute("""
                    SELECT i.*, l.name as lab_name, l.ports
                    FROM lab_instances i
                    JOIN labs l ON i.lab_id = l.id
                    WHERE i.user_id = %s AND i.lab_id = %s
                    ORDER BY i.created_at DESC
                    LIMIT 1
                """, (user_id, lab_id))
                instance = cursor.fetchone()
                
                if not instance:
                    return {"status": "not_found", "message": "未找到实例记录"}
                
                # 检查容器状态
                try:
                    container = self.docker_client.containers.get(instance['container_id'])
                    container_status = container.status
                    
                    # 获取容器详细信息
                    stats = container.stats(stream=False)
                    memory_usage = stats['memory_stats']['usage']
                    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
                    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
                    cpu_usage = (cpu_delta / system_delta) * 100.0
                    
                    # 更新指标
                    if self.metrics:
                        self.metrics['container_memory'].set(memory_usage)
                        self.metrics['container_cpu'].set(cpu_usage)
                    
                    return {
                        "status": "success",
                        "instance_status": instance['status'],
                        "container_status": container_status,
                        "lab_name": instance['lab_name'],
                        "ports": json.loads(instance['ports']) if instance['ports'] else {},
                        "metrics": {
                            "memory_usage": memory_usage,
                            "cpu_usage": round(cpu_usage, 2)
                        },
                        "created_at": instance['created_at'].isoformat(),
                        "updated_at": instance['updated_at'].isoformat()
                    }
                    
                except docker.errors.NotFound:
                    # 容器不存在，更新实例状态
                    self._update_instance_status(instance['id'], 'error')
                    return {
                        "status": "error",
                        "message": "容器已不存在",
                        "instance_status": "error"
                    }
                    
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"获取靶场状态失败: {str(e)}")
            return {"status": "error", "message": str(e)}

    def cleanup_expired_instances(self):
        """清理过期的实例"""
        try:
            if not self.docker_client:
                logger.warning("Docker服务不可用，跳过清理")
                return
                
            conn = mysql.connector.connect(**CONFIG["database"])
            cursor = conn.cursor(dictionary=True)
            try:
                # 获取过期实例
                expire_time = datetime.now() - timedelta(hours=4)  # 4小时过期
                cursor.execute("""
                    SELECT * FROM lab_instances 
                    WHERE status = 'running' 
                    AND created_at < %s
                """, (expire_time,))
                expired = cursor.fetchall()
                
                for instance in expired:
                    try:
                        # 停止容器
                        container = self.docker_client.containers.get(instance['container_id'])
                        container.stop()
                    except docker.errors.NotFound:
                        pass  # 容器可能已经不存在
                    
                    # 更新实例状态
                    self._update_instance_status(instance['id'], 'stopped')
                
                if expired:
                    logger.info(f"已清理 {len(expired)} 个过期实例")
                    
            finally:
                cursor.close()
                conn.close()
                
        except Exception as e:
            logger.error(f"清理过期实例失败: {str(e)}")

# 创建全局实例
lab_manager = LabManager() 