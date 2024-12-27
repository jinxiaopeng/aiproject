"""
通知服务
负责处理系统通知、告警等
"""

import logging
from typing import Dict, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.websocket_connections: Dict[int, List[WebSocket]] = {}  # user_id -> websockets
        self.notification_history: Dict[int, List[Dict]] = {}  # user_id -> notifications
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """建立WebSocket连接"""
        await websocket.accept()
        if user_id not in self.websocket_connections:
            self.websocket_connections[user_id] = []
        self.websocket_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected to notification service")
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """断开WebSocket连接"""
        if user_id in self.websocket_connections:
            self.websocket_connections[user_id].remove(websocket)
            if not self.websocket_connections[user_id]:
                del self.websocket_connections[user_id]
        logger.info(f"User {user_id} disconnected from notification service")
    
    async def send_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        type: str = "info",
        challenge_id: Optional[int] = None
    ):
        """发送通知"""
        notification = {
            "title": title,
            "message": message,
            "type": type,
            "challenge_id": challenge_id,
            "timestamp": datetime.now().isoformat()
        }
        
        # 保存通知历史
        if user_id not in self.notification_history:
            self.notification_history[user_id] = []
        self.notification_history[user_id].append(notification)
        
        # 限制历史记录数量
        if len(self.notification_history[user_id]) > 100:
            self.notification_history[user_id] = self.notification_history[user_id][-100:]
        
        # 发送WebSocket消息
        if user_id in self.websocket_connections:
            for websocket in self.websocket_connections[user_id]:
                try:
                    await websocket.send_json(notification)
                except Exception as e:
                    logger.error(f"Error sending notification to user {user_id}: {str(e)}")
                    await self.disconnect(websocket, user_id)
    
    async def send_timeout_warning(
        self,
        user_id: int,
        challenge_id: int,
        remaining_time: int,
        timeout_type: str
    ):
        """发送超时警告"""
        title = "靶场超时警告"
        if timeout_type == "total":
            message = f"靶场将在 {remaining_time} 秒后因总时间超时而停止"
        else:
            message = f"靶场将在 {remaining_time} 秒后因空闲超时而停止"
            
        await self.send_notification(
            user_id,
            title,
            message,
            "warning",
            challenge_id
        )
    
    async def send_timeout_notification(
        self,
        user_id: int,
        challenge_id: int,
        timeout_type: str
    ):
        """发送超时通知"""
        title = "靶场已超时停止"
        if timeout_type == "total":
            message = "靶场已因达到最大运行时间而停止"
        else:
            message = "靶场已因空闲时间过长而停止"
            
        await self.send_notification(
            user_id,
            title,
            message,
            "error",
            challenge_id
        )
    
    async def send_resource_warning(
        self,
        user_id: int,
        challenge_id: int,
        resource_type: str,
        current_value: float,
        limit_value: float
    ):
        """发送资源告警"""
        title = "资源使用告警"
        if resource_type == "cpu":
            message = f"CPU使用率达到 {current_value:.1f}%，接近限制 {limit_value}%"
        elif resource_type == "memory":
            message = f"内存使用率达到 {current_value:.1f}%，接近限制 {limit_value}%"
            
        await self.send_notification(
            user_id,
            title,
            message,
            "warning",
            challenge_id
        )
    
    def get_notification_history(self, user_id: int, limit: int = 50) -> List[Dict]:
        """获取通知历史"""
        if user_id not in self.notification_history:
            return []
        return self.notification_history[user_id][-limit:]

# 创建全局通知服务实例
notification_service = NotificationService() 