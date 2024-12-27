import requests
import json
import time

BASE_URL = 'http://localhost:3017'
AUTH_HEADERS = {
    'Content-Type': 'application/json'
}

def test_auth():
    """测试认证功能"""
    print("测试认证...")
    auth_data = {
        'username': 'admin',
        'password': 'jxp1210'
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login', json=auth_data)
        if response.status_code == 200:
            token = response.json().get('token')
            AUTH_HEADERS['Authorization'] = f'Bearer {token}'
            print("✓ 认证成功")
            return True
        else:
            print(f"✗ 认证失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ 认证请求异常: {str(e)}")
        return False

def test_monitor_overview():
    """测试系统监控概览"""
    print("\n测试系统监控概览...")
    try:
        response = requests.get(f'{BASE_URL}/monitor/overview', headers=AUTH_HEADERS)
        if response.status_code == 200:
            data = response.json()
            print("✓ 获取监控概览成功")
            print(f"CPU使用率: {data['current_stats']['cpu_usage']}%")
            print(f"内存使用率: {data['current_stats']['memory_usage']}%")
            print(f"磁盘使用率: {data['current_stats']['disk_usage']}%")
            return True
        else:
            print(f"✗ 获取监控概览失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ 监控概览请求异常: {str(e)}")
        return False

def test_alerts():
    """测试告警功能"""
    print("\n测试告警功能...")
    try:
        response = requests.get(f'{BASE_URL}/monitor/alerts', headers=AUTH_HEADERS)
        if response.status_code == 200:
            alerts = response.json()
            print("✓ 获取告警列表成功")
            print(f"总告警数: {len(alerts)}")
            if alerts:
                print("\n最新告警:")
                for alert in alerts[:3]:
                    print(f"- [{alert['type']}] {alert['message']} ({alert['status']})")
            return True
        else:
            print(f"✗ 获取告警列表失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ 告警列表请求异常: {str(e)}")
        return False

def test_monitor_settings():
    """测试监控设置"""
    print("\n测试监控设置...")
    try:
        response = requests.get(f'{BASE_URL}/monitor/settings', headers=AUTH_HEADERS)
        if response.status_code == 200:
            settings = response.json()
            print("✓ 获取监控设置成功")
            print(f"CPU告警阈值: {settings['thresholds']['cpu_usage']}%")
            print(f"内存告警阈值: {settings['thresholds']['memory_usage']}%")
            print(f"磁盘告警阈值: {settings['thresholds']['disk_usage']}%")
            return True
        else:
            print(f"✗ 获取监控设置失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"✗ 监控设置请求异常: {str(e)}")
        return False

def main():
    print("开始测试监控系统...\n")
    
    # 测试认证
    if not test_auth():
        print("\n认证失败,终止测试")
        return
    
    # 测试系统监控
    test_monitor_overview()
    
    # 测试告警功能
    test_alerts()
    
    # 测试监控设置
    test_monitor_settings()
    
    print("\n测试完成!")

if __name__ == '__main__':
    main() 