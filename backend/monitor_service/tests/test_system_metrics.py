import pytest
from unittest.mock import patch, MagicMock
from monitor_service.collector.system_metrics import SystemMetricsCollector
from monitor_service.realtime.models import RealtimeMonitor
from datetime import datetime
from monitor_service.tests.conftest import User

@pytest.fixture
def test_user(db_session):
    """创建测试用户"""
    user = User(
        username="test_user",
        email="test@example.com",
        hashed_password="test_password"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def mock_psutil():
    with patch('psutil.cpu_percent') as mock_cpu, \
         patch('psutil.virtual_memory') as mock_memory, \
         patch('psutil.disk_usage') as mock_disk, \
         patch('psutil.net_io_counters') as mock_net, \
         patch('psutil.getloadavg') as mock_load, \
         patch('psutil.pids') as mock_pids:
        
        # 模拟CPU使用率
        mock_cpu.return_value = 45.2
        
        # 模拟内存使用情况
        mock_memory_info = MagicMock()
        mock_memory_info.percent = 62.5
        mock_memory.return_value = mock_memory_info
        
        # 模拟磁盘使用情况
        mock_disk_info = MagicMock()
        mock_disk_info.percent = 78.3
        mock_disk.return_value = mock_disk_info
        
        # 模拟网络IO
        mock_net_info = MagicMock()
        mock_net_info.bytes_recv = 1000000
        mock_net_info.bytes_sent = 500000
        mock_net.return_value = mock_net_info
        
        # 模拟系统负载
        mock_load.return_value = (1.5, 1.2, 1.0)
        
        # 模拟进程数
        mock_pids.return_value = list(range(100))
        
        yield {
            'cpu': mock_cpu,
            'memory': mock_memory,
            'disk': mock_disk,
            'net': mock_net,
            'load': mock_load,
            'pids': mock_pids
        }

def test_collect_metrics(mock_psutil, db_session, test_user):
    """测试系统资源数据采集"""
    user_id = test_user.id
    with patch('monitor_service.collector.system_metrics.get_db', return_value=iter([db_session])), \
         patch('time.sleep'):  # 避免实际等待
        collector = SystemMetricsCollector()
        collector.collect_metrics(user_id=user_id)
    
    # 验证数据是否被正确保存
    saved_record = db_session.query(RealtimeMonitor).filter_by(user_id=user_id).first()
    assert saved_record is not None
    assert saved_record.user_id == user_id
    assert saved_record.cpu_usage == 45.2
    assert saved_record.memory_usage == 62.5
    assert saved_record.disk_usage == 78.3
    assert saved_record.system_load == 1.5
    assert saved_record.process_count == 100
    assert saved_record.node_name == 'primary'

def test_collect_metrics_error_handling(mock_psutil, db_session, test_user):
    """测试错误处理"""
    # 模拟数据库错误
    db_session.commit = MagicMock(side_effect=Exception("Database error"))
    db_session.rollback = MagicMock()
    
    with patch('monitor_service.collector.system_metrics.get_db', return_value=iter([db_session])), \
         patch('time.sleep'):  # 避免实际等待
        collector = SystemMetricsCollector()
        collector.collect_metrics(user_id=test_user.id)
    
    # 验证是否正确处理了错误
    assert db_session.rollback.called