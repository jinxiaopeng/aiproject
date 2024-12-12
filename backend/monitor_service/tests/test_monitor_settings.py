import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径
current_dir = Path(__file__).resolve().parent
monitor_service_dir = current_dir.parent
backend_dir = monitor_service_dir.parent
sys.path.append(str(backend_dir))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from monitor_service.core.auth import create_access_token
from monitor_service.models.monitor import MonitorSettings

# 测试用户数据
TEST_USER = {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
}

@pytest.fixture
def auth_headers():
    """认证头"""
    access_token = create_access_token(TEST_USER)
    return {"Authorization": f"Bearer {access_token}"}

def test_get_monitor_settings(client, db, auth_headers):
    """测试获取监控设置"""
    response = client.get("/api/monitor/settings", headers=auth_headers)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == TEST_USER["id"]
    assert "login_alert" in data
    assert "operation_alert" in data
    assert "security_alert" in data
    assert "notify_methods" in data

def test_update_monitor_settings(client, db, auth_headers):
    """测试更新监控设置"""
    update_data = {
        "login_alert": False,
        "operation_alert": True,
        "security_alert": True,
        "notify_methods": ["email", "web"]
    }
    response = client.put(
        "/api/monitor/settings",
        headers=auth_headers,
        json=update_data
    )
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["login_alert"] == update_data["login_alert"]
    assert data["operation_alert"] == update_data["operation_alert"]
    assert data["security_alert"] == update_data["security_alert"]
    assert data["notify_methods"] == update_data["notify_methods"]

def test_get_settings_creates_default(client, db, auth_headers):
    """测试获取设置时如果不存在会创建默认设置"""
    # 确保没有已存在的设置
    db.query(MonitorSettings).filter(
        MonitorSettings.user_id == TEST_USER["id"]
    ).delete()
    db.commit()

    response = client.get("/api/monitor/settings", headers=auth_headers)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["login_alert"] == True
    assert data["operation_alert"] == False
    assert data["security_alert"] == True
    assert data["notify_methods"] == ["web"] 