import docker
from typing import Dict, List, Optional
from datetime import datetime
import mysql.connector
import json

from config import DB_CONFIG
from core.logger import system_logger
from core.docker import docker_manager

class LabManager:
    """靶场管理器"""
    
    def __init__(self):
        """初始化靶场管理器"""
        self.docker_client = docker.from_env()
        system_logger.info("靶场管理器初始化成功", "lab")
    
    def get_lab_info(self, lab_id: int) -> Optional[Dict]:
        """获取靶场信息"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM labs WHERE id = %s",
                (lab_id,)
            )
            lab = cursor.fetchone()
            
            if not lab:
                return None
            
            return lab
            
        except Exception as e:
            system_logger.error(f"获取靶场信息失败: {str(e)}", "lab", {
                'lab_id': lab_id
            })
            return None
        finally:
            cursor.close()
            conn.close()
    
    async def start_lab(self, lab_id: int, user_id: int) -> Dict:
        """启动靶场"""
        try:
            # 获取靶场信息
            lab_info = self.get_lab_info(lab_id)
            if not lab_info:
                return {"status": "error", "message": "靶场不存在"}
            
            # 检查是否有运行中的实例
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM lab_instances WHERE user_id = %s AND status = 'running'",
                (user_id,)
            )
            running_instance = cursor.fetchone()
            
            if running_instance:
                return {"status": "error", "message": "已有运行中的实例"}
            
            # 创建Docker容器
            container_id, instance_url = await docker_manager.create_container(
                image=lab_info['docker_image'],
                port_mapping=lab_info['internal_port'],
                max_memory="512m",
                cpu_limit=0.5,
                timeout=3600  # 1小时超时
            )
            
            # 记录实例信息
            cursor.execute(
                """
                INSERT INTO lab_instances 
                (lab_id, user_id, container_id, status, port, start_time)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (lab_id, user_id, container_id, 'running', 
                 lab_info['internal_port'], datetime.now())
            )
            conn.commit()
            
            return {
                "status": "success",
                "message": "靶场启动成功",
                "container_id": container_id,
                "instance_url": instance_url
            }
            
        except Exception as e:
            system_logger.error(f"启动靶场失败: {str(e)}", "lab", {
                'lab_id': lab_id,
                'user_id': user_id
            })
            return {"status": "error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    async def stop_lab(self, lab_id: int, user_id: int) -> Dict:
        """停止靶场"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 获取运行中的实例
            cursor.execute(
                """
                SELECT * FROM lab_instances 
                WHERE lab_id = %s AND user_id = %s AND status = 'running'
                """,
                (lab_id, user_id)
            )
            instance = cursor.fetchone()
            
            if not instance:
                return {"status": "error", "message": "没有运行中的实例"}
            
            # 停止Docker容器
            await docker_manager.stop_container(instance['container_id'])
            
            # 更新实例状态
            cursor.execute(
                """
                UPDATE lab_instances 
                SET status = 'stopped', end_time = %s
                WHERE id = %s
                """,
                (datetime.now(), instance['id'])
            )
            conn.commit()
            
            return {"status": "success", "message": "靶场已停止"}
            
        except Exception as e:
            system_logger.error(f"停止靶场失败: {str(e)}", "lab", {
                'lab_id': lab_id,
                'user_id': user_id
            })
            return {"status": "error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def get_lab_status(self, lab_id: int, user_id: int) -> Dict:
        """获取靶场状态"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 获取实例信息
            cursor.execute(
                """
                SELECT * FROM lab_instances 
                WHERE lab_id = %s AND user_id = %s 
                ORDER BY start_time DESC LIMIT 1
                """,
                (lab_id, user_id)
            )
            instance = cursor.fetchone()
            
            if not instance:
                return {
                    "status": "not_started",
                    "message": "未启动实验环境"
                }
            
            # 如果实例正在运行，检查容器状态
            if instance['status'] == 'running':
                try:
                    container = self.docker_client.containers.get(instance['container_id'])
                    container_status = container.status
                    container_stats = container.stats(stream=False)
                    
                    return {
                        "status": "running",
                        "container_id": instance['container_id'],
                        "start_time": instance['start_time'].isoformat(),
                        "container_status": container_status,
                        "container_stats": {
                            "cpu_usage": container_stats['cpu_stats']['cpu_usage']['total_usage'],
                            "memory_usage": container_stats['memory_stats']['usage'],
                            "network_rx": container_stats['networks']['eth0']['rx_bytes'],
                            "network_tx": container_stats['networks']['eth0']['tx_bytes']
                        }
                    }
                except docker.errors.NotFound:
                    # 容器不存在，更新状态为错误
                    cursor.execute(
                        "UPDATE lab_instances SET status = 'error' WHERE id = %s",
                        (instance['id'],)
                    )
                    conn.commit()
                    return {
                        "status": "error",
                        "message": "容器已丢失"
                    }
            
            return {
                "status": instance['status'],
                "start_time": instance['start_time'].isoformat(),
                "end_time": instance['end_time'].isoformat() if instance['end_time'] else None
            }
            
        except Exception as e:
            system_logger.error(f"获取靶场状态失败: {str(e)}", "lab", {
                'lab_id': lab_id,
                'user_id': user_id
            })
            return {"status": "error", "message": str(e)}
        finally:
            cursor.close()
            conn.close()
    
    def cleanup_expired_instances(self):
        """清理过期的实例"""
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor(dictionary=True)
            
            # 获取所有运行超过1小时的实例
            cursor.execute(
                """
                SELECT * FROM lab_instances 
                WHERE status = 'running' 
                AND TIMESTAMPDIFF(HOUR, start_time, NOW()) >= 1
                """
            )
            expired_instances = cursor.fetchall()
            
            for instance in expired_instances:
                try:
                    # 停止容器
                    container = self.docker_client.containers.get(instance['container_id'])
                    container.stop(timeout=10)
                    container.remove(force=True)
                    
                    # 更新实例状态
                    cursor.execute(
                        """
                        UPDATE lab_instances 
                        SET status = 'expired', end_time = NOW()
                        WHERE id = %s
                        """,
                        (instance['id'],)
                    )
                    conn.commit()
                    
                    system_logger.info(f"清理过期实例成功", "lab", {
                        'instance_id': instance['id'],
                        'container_id': instance['container_id']
                    })
                except Exception as e:
                    system_logger.error(f"清理过期实例失败: {str(e)}", "lab", {
                        'instance_id': instance['id'],
                        'container_id': instance['container_id']
                    })
            
        except Exception as e:
            system_logger.error(f"清理过期实例失败: {str(e)}", "lab")
        finally:
            cursor.close()
            conn.close()

# 创建靶场管理器实例
lab_manager = LabManager() 