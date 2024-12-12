import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..services.login_monitor import LoginMonitorService
from ..models.monitor import LoginMonitor, LoginEventType
from ..schemas.monitor import LoginMonitorCreate

def create_test_login_event(db: Session, user_id: int, event_type: LoginEventType) -> LoginMonitor:
    """创建测试用的登录事件"""
    event = LoginMonitorCreate(
        user_id=user_id,
        event_type=event_type,
        ip_address="127.0.0.1",
        user_agent="Test Browser",
        location="Test Location"
    )
    service = LoginMonitorService(db)
    return service.create_login_event(event)

def test_create_login_event(db: Session):
    """测试创建登录事件"""
    service = LoginMonitorService(db)
    event = LoginMonitorCreate(
        user_id=1,
        event_type=LoginEventType.SUCCESS,
        ip_address="127.0.0.1",
        user_agent="Test Browser",
        location="Test Location"
    )
    
    db_event = service.create_login_event(event)
    assert db_event.id is not None
    assert db_event.user_id == 1
    assert db_event.event_type == LoginEventType.SUCCESS
    assert db_event.ip_address == "127.0.0.1"

def test_get_login_events(db: Session):
    """测试获取登录事件列表"""
    # 创建测试数据
    create_test_login_event(db, 1, LoginEventType.SUCCESS)
    create_test_login_event(db, 1, LoginEventType.FAILED)
    create_test_login_event(db, 2, LoginEventType.SUCCESS)
    
    service = LoginMonitorService(db)
    
    # 测试获取所有事件
    events = service.get_login_events()
    assert len(events) == 3
    
    # 测试按用户筛选
    events = service.get_login_events(user_id=1)
    assert len(events) == 2
    assert all(e.user_id == 1 for e in events)
    
    # 测试按事件类型筛选
    events = service.get_login_events(event_type=LoginEventType.SUCCESS)
    assert len(events) == 2
    assert all(e.event_type == LoginEventType.SUCCESS for e in events)

def test_get_failed_login_attempts(db: Session):
    """测试获取失败登录尝试次数"""
    service = LoginMonitorService(db)
    
    # 创建测试数据
    create_test_login_event(db, 1, LoginEventType.FAILED)
    create_test_login_event(db, 1, LoginEventType.FAILED)
    create_test_login_event(db, 1, LoginEventType.SUCCESS)
    
    # 测试获取失败次数
    attempts = service.get_failed_login_attempts(user_id=1, minutes=30)
    assert attempts == 2

def test_get_login_statistics(db: Session):
    """测试获取登录统计信息"""
    service = LoginMonitorService(db)
    
    # 创建测试数据
    create_test_login_event(db, 1, LoginEventType.SUCCESS)
    create_test_login_event(db, 1, LoginEventType.SUCCESS)
    create_test_login_event(db, 1, LoginEventType.FAILED)
    
    # 测试获取统计信息
    stats = service.get_login_statistics(user_id=1)
    assert stats["total_events"] == 3
    assert stats["success_events"] == 2
    assert stats["failed_events"] == 1
    assert stats["success_rate"] == pytest.approx(66.67, 0.01)

@pytest.mark.asyncio
async def test_login_monitor_api(async_client, db: Session):
    """测试登录监控API接口"""
    # 创建登录事件
    response = await async_client.post("/login/events", json={
        "user_id": 1,
        "event_type": "SUCCESS",
        "ip_address": "127.0.0.1",
        "user_agent": "Test Browser",
        "location": "Test Location"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    
    # 获取登录事件列表
    response = await async_client.get("/login/events")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    
    # 获取失败登录尝试次数
    response = await async_client.get("/login/failed-attempts/1")
    assert response.status_code == 200
    data = response.json()
    assert "failed_attempts" in data
    
    # 获取登录统计信息
    response = await async_client.get("/login/statistics")
    assert response.status_code == 200
    data = response.json()
    assert "total_events" in data 