import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..realtime.models import RealtimeMonitor
from ..realtime.schemas import RealtimeMonitorCreate
from ..realtime import services

# 测试数据
TEST_USER = {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
}

@pytest.fixture
def test_monitor_data():
    """测试监控数据"""
    return {
        "user_id": TEST_USER["id"],
        "cpu_usage": 45.5,
        "memory_usage": 60.2,
        "disk_usage": 75.8,
        "network_in": 2.5,
        "network_out": 1.8,
        "system_load": 1.5,
        "process_count": 120,
        "node_name": "test-node",
        "notes": "测试数据"
    }

def test_create_monitor_record(db: Session, test_monitor_data):
    """测试创建监控记录"""
    monitor = RealtimeMonitorCreate(**test_monitor_data)
    record = services.create_monitor_record(db, monitor)
    
    assert record.id is not None
    assert record.user_id == test_monitor_data["user_id"]
    assert record.cpu_usage == test_monitor_data["cpu_usage"]
    assert record.memory_usage == test_monitor_data["memory_usage"]
    assert record.timestamp is not None

def test_get_latest_records(db: Session, test_monitor_data):
    """测试获取最新监控记录"""
    # 创建多条测试数据
    for i in range(5):
        monitor = RealtimeMonitorCreate(**test_monitor_data)
        services.create_monitor_record(db, monitor)
    
    records = services.get_latest_records(db, TEST_USER["id"], limit=3)
    assert len(records) == 3
    assert all(r.user_id == TEST_USER["id"] for r in records)
    assert records[0].timestamp >= records[1].timestamp

def test_get_stats(db: Session, test_monitor_data):
    """测试获取监控统计数据"""
    # 创建测试数据
    for i in range(3):
        data = test_monitor_data.copy()
        data["cpu_usage"] = 40 + i * 10  # 40, 50, 60
        monitor = RealtimeMonitorCreate(**data)
        services.create_monitor_record(db, monitor)
    
    stats = services.get_stats(db, TEST_USER["id"], hours=24)
    assert stats.avg_cpu_usage == 50.0  # (40 + 50 + 60) / 3
    assert stats.max_cpu_usage == 60.0
    assert stats.total_records == 3

def test_cleanup_old_records(db: Session, test_monitor_data):
    """测试清理旧记录"""
    # 创建一些旧数据
    old_time = datetime.now() - timedelta(days=31)
    for i in range(3):
        monitor = RealtimeMonitor(**test_monitor_data)
        monitor.timestamp = old_time
        db.add(monitor)
    
    # 创建一些新数据
    for i in range(2):
        monitor = RealtimeMonitorCreate(**test_monitor_data)
        services.create_monitor_record(db, monitor)
    
    db.commit()
    
    # 清理30天前的数据
    deleted = services.cleanup_old_records(db, days=30)
    assert deleted == 3
    
    # 验证只剩下新数据
    remaining = db.query(RealtimeMonitor).count()
    assert remaining == 2 