from fastapi import APIRouter, Depends, HTTPException, status, Body
from backend.core.deps import get_current_user
from backend.models.user import User
from typing import List, Dict, Any
import random
from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter(prefix="/monitor", tags=["monitor"])

# 告警处理动作模型
class AlertAction(BaseModel):
    type: str
    alertId: str
    comment: str = None
    parameters: Dict[str, Any] = None

# 模拟数据生成
def generate_mock_stats():
    """生成基础统计数据"""
    return {
        "security": {
            "total_alerts": random.randint(50, 200),
            "pending_alerts": random.randint(10, 30),
            "critical_alerts": random.randint(1, 5),
            "recent_attacks": random.randint(5, 15),
            "blocked_ips": random.randint(20, 100),
            "alert_trend": random.randint(-20, 20),
            "attack_types": {
                "sql_injection": random.randint(10, 50),
                "xss": random.randint(5, 30),
                "file_upload": random.randint(3, 20),
                "command_injection": random.randint(1, 10),
                "unauthorized_access": random.randint(10, 40)
            }
        },
        "lab": {
            "total_labs": random.randint(150, 250),
            "active_labs": random.randint(50, 100),
            "error_labs": random.randint(0, 5),
            "resource_usage": random.randint(40, 90),
            "lab_types": {
                "web_security": random.randint(30, 60),
                "system_security": random.randint(20, 40),
                "network_security": random.randint(25, 45),
                "crypto": random.randint(10, 25),
                "reverse": random.randint(15, 35)
            },
            "resources": {
                "cpu_usage": random.randint(40, 90),
                "memory_usage": random.randint(50, 85),
                "storage_usage": random.randint(60, 80),
                "network_usage": random.randint(30, 70)
            }
        },
        "system": {
            "uptime": random.randint(86400, 864000),  # 1-10天的秒数
            "total_users": random.randint(800, 1200),
            "active_sessions": random.randint(50, 200),
            "avg_response_time": random.randint(100, 500),
            "metrics": {
                "cpu_usage": random.randint(40, 90),
                "memory_usage": random.randint(50, 85),
                "disk_usage": random.randint(60, 80)
            },
            "network": {
                "inbound": random.randint(1024 * 1024, 1024 * 1024 * 10),  # 1-10MB/s
                "outbound": random.randint(1024 * 1024, 1024 * 1024 * 5),  # 1-5MB/s
                "connections": random.randint(100, 500),
                "error_rate": round(random.uniform(0.1, 3.0), 2)
            }
        }
    }

def generate_mock_alerts():
    """生成模拟的告警数据"""
    alert_types = ["login", "injection", "xss", "file_access", "privilege"]
    alert_levels = ["low", "medium", "high", "critical"]
    alert_status = ["pending", "processing", "resolved"]
    alerts = []
    
    for _ in range(random.randint(5, 15)):
        alert_type = random.choice(alert_types)
        level = random.choice(alert_levels)
        status = random.choice(alert_status)
        timestamp = datetime.now() - timedelta(minutes=random.randint(1, 60))
        
        alerts.append({
            "id": str(random.randint(1000, 9999)),
            "type": alert_type,
            "level": level,
            "source": f"{alert_type}_detector",
            "timestamp": timestamp.isoformat(),
            "details": {
                "ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "user": f"user_{random.randint(1, 1000)}",
                "action": "unauthorized_access" if alert_type == "login" else "malicious_payload",
                "payload": "SELECT * FROM users" if alert_type == "injection" else "<script>alert(1)</script>",
                "location": "/api/user/login" if alert_type == "login" else f"/api/{alert_type}",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            "status": status
        })
    
    return sorted(alerts, key=lambda x: x["timestamp"], reverse=True)

def generate_mock_metrics():
    """生成模拟的系统指标数据"""
    return {
        "cpu_usage": round(random.uniform(40, 70), 1),
        "memory_usage": round(random.uniform(60, 80), 1),
        "disk_usage": round(random.uniform(70, 80), 1),
        "network": {
            "incoming": round(random.uniform(100, 500), 1),
            "outgoing": round(random.uniform(50, 300), 1)
        },
        "response_time": round(random.uniform(100, 300), 1),
        "error_rate": round(random.uniform(0, 2), 2),
        "active_users": random.randint(50, 150),
        "active_labs": random.randint(30, 80),
        "timestamp": datetime.now().isoformat()
    }

def generate_mock_trends(hours: int):
    """生成模拟的告警趋势数据"""
    trends = []
    for i in range(hours):
        timestamp = datetime.now() - timedelta(hours=i)
        trends.append({
            "timestamp": timestamp.isoformat(),
            "security_alerts": random.randint(0, 10),
            "lab_alerts": random.randint(0, 5),
            "system_alerts": random.randint(0, 3)
        })
    return sorted(trends, key=lambda x: x["timestamp"])

def generate_mock_logs(limit: int):
    """生成模拟的实时日志数据"""
    log_types = ["security", "lab", "system"]
    log_levels = ["info", "warning", "error", "critical"]
    logs = []
    
    for i in range(limit):
        log_type = random.choice(log_types)
        log_level = random.choice(log_levels)
        timestamp = datetime.now() - timedelta(minutes=i)
        
        logs.append({
            "id": random.randint(1000, 9999),
            "type": log_type,
            "level": log_level,
            "message": f"{log_level.upper()}: {log_type} event occurred",
            "timestamp": timestamp.isoformat(),
            "details": {
                "source": f"{log_type}_service",
                "ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "user": f"user_{random.randint(1, 1000)}"
            }
        })
    
    return sorted(logs, key=lambda x: x["timestamp"], reverse=True)

@router.get("/stats")
async def get_monitor_stats(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """获取监控统计数据"""
    return generate_mock_stats()

@router.get("/alerts")
async def get_monitor_alerts(
    current_user: User = Depends(get_current_user),
    severity: str = None,
    status: str = None,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """获取监控告警列表"""
    alerts = generate_mock_alerts()
    
    if severity:
        alerts = [a for a in alerts if a["level"] == severity]
    if status:
        alerts = [a for a in alerts if a["status"] == status]
    
    return alerts[:limit]

@router.post("/alerts/handle")
async def handle_alert(
    action: AlertAction,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """处理告警"""
    # 在实际应用中，这里应该处理真实的告警
    # 现在我们只是模拟处理
    actions = {
        "block_ip": "已封禁IP",
        "reset_password": "已重置密码",
        "disable_user": "已禁用用户",
        "mark_resolved": "已标记为已解决",
        "notify_admin": "已通知管理员",
        "add_blacklist": "已加入黑名单",
        "clear_cache": "已清理缓存",
        "revoke_permission": "已撤销权限",
        "reset_privilege": "已重置权限"
    }
    
    if action.type not in actions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的操作类型"
        )
    
    return {
        "success": True,
        "message": actions[action.type],
        "action": action.dict()
    }

@router.get("/metrics")
async def get_system_metrics(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """获取系统指标数据"""
    return generate_mock_metrics()

@router.get("/trends")
async def get_alert_trends(
    current_user: User = Depends(get_current_user),
    time_range: str = "today"
) -> List[Dict[str, Any]]:
    """获取告警趋势数据"""
    hours = 24  # 默认今天
    if time_range == "week":
        hours = 24 * 7
    elif time_range == "month":
        hours = 24 * 30
    
    return generate_mock_trends(hours)

@router.get("/logs")
async def get_realtime_logs(
    current_user: User = Depends(get_current_user),
    limit: int = 50,
    log_type: str = None,
    level: str = None
) -> List[Dict[str, Any]]:
    """获取实时日志数据"""
    logs = generate_mock_logs(limit)
    
    if log_type:
        logs = [log for log in logs if log["type"] == log_type]
    if level:
        logs = [log for log in logs if log["level"] == level]
    
    return logs[:limit]

@router.get("/settings")
async def get_monitor_settings(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """获取监控设置"""
    return {
        "thresholds": {
            "cpu_usage": 80,
            "memory_usage": 90,
            "disk_usage": 85,
            "network_latency": 200
        },
        "notification": {
            "email": True,
            "slack": False,
            "webhook": False
        },
        "alert_rules": [
            {
                "id": 1,
                "name": "High CPU Usage",
                "condition": "cpu_usage > 80",
                "severity": "critical",
                "enabled": True
            },
            {
                "id": 2,
                "name": "High Memory Usage",
                "condition": "memory_usage > 90",
                "severity": "error",
                "enabled": True
            }
        ]
    }

@router.post("/settings")
async def update_monitor_settings(
    settings: Dict[str, Any],
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """更新监控设置"""
    # 在实际应用中，这里应该保存到数据库
    return {
        "message": "Settings updated successfully",
        "settings": settings
    }

@router.post("/quick-actions/{action}")
async def execute_quick_action(
    action: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """执行快速操作"""
    valid_actions = {
        "refresh_all": "已刷新所有数据",
        "clear_alerts": "已清理历史告警",
        "test_connection": "连接测试完成",
        "export_logs": "日志导出完成",
        "reset_warning": "已重置所有警告",
        "system_check": "系统检查完成"
    }
    
    if action not in valid_actions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不支持的操作类型"
        )
    
    return {
        "success": True,
        "message": valid_actions[action],
        "action": action
    }