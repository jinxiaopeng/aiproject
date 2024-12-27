"""
通知相关的API路由
"""

from fastapi import APIRouter, Depends, WebSocket, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from ..database import get_db
from ..services.notification_service import notification_service
from ..auth import get_current_user
from ..models.user import User

router = APIRouter(prefix="/api/notifications", tags=["notifications"])

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    db: Session = Depends(get_db)
):
    """WebSocket连接端点"""
    try:
        # 验证用户
        user = get_current_user(token, db)
        if not user:
            await websocket.close(code=4001)
            return
            
        # 建立连接
        await notification_service.connect(websocket, user.id)
        
        try:
            while True:
                # 保持连接活跃
                data = await websocket.receive_text()
                if data == "ping":
                    await websocket.send_text("pong")
        except Exception as e:
            pass
        finally:
            # 断开连接
            notification_service.disconnect(websocket, user.id)
            
    except Exception as e:
        await websocket.close(code=4002)

@router.get("/history")
async def get_notification_history(
    limit: int = 50,
    user: User = Depends(get_current_user)
) -> List[Dict]:
    """获取通知历史"""
    return notification_service.get_notification_history(user.id, limit)

@router.delete("/clear")
async def clear_notifications(
    user: User = Depends(get_current_user)
):
    """清空通知历史"""
    if user.id in notification_service.notification_history:
        notification_service.notification_history[user.id] = []
    return {"status": "success"} 