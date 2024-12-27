import requests
import json
from requests.exceptions import RequestException

BASE_URL = 'http://localhost:3017'

def safe_request(method, url, **kwargs):
    """安全的请求包装器"""
    print(f"\n请求: {method} {url}")
    print(f"参数: {json.dumps(kwargs, ensure_ascii=False)}")
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        print(f"状态码: {response.status_code}")
        if response.status_code != 200:
            print(f"错误响应: {response.text}")
            return None
        return response.json()
    except RequestException as e:
        print(f"请求异常: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {str(e)}")
        print(f"响应内容: {response.text}")
        return None

def test_auth():
    """测试认证"""
    print('\n=== 测试认证 ===')
    auth_data = {
        'username': 'admin',
        'password': 'jxp1210'
    }
    result = safe_request('POST', f'{BASE_URL}/auth/login', json=auth_data)
    if result:
        print('认证成功:', json.dumps(result, ensure_ascii=False, indent=2))
        return result.get('token')
    print('认证失败')
    return None

def test_monitor_overview(token=None):
    """测试监控概览"""
    print('\n=== 测试监控概览 ===')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    } if token else {}
    
    result = safe_request('GET', f'{BASE_URL}/monitor/overview', headers=headers)
    if result:
        print('监控概览数据:')
        print(f"CPU使用率: {result['current_stats']['cpu_usage']}%")
        print(f"内存使用率: {result['current_stats']['memory_usage']}%")
        print(f"磁盘使用率: {result['current_stats']['disk_usage']}%")
        print(f"系统状态: {result['system_status']}")
        print('\n告警统计:')
        print(f"总计: {result['alerts_summary']['total']}")
        print(f"严重: {result['alerts_summary']['critical']}")
        print(f"错误: {result['alerts_summary']['error']}")
        print(f"警告: {result['alerts_summary']['warning']}")
        print(f"信息: {result['alerts_summary']['info']}")
    else:
        print('获取监控概览失败')
    return result

def test_monitor_alerts(token=None):
    """测试告警列表"""
    print('\n=== 测试告警列表 ===')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    } if token else {}
    
    result = safe_request('GET', f'{BASE_URL}/monitor/alerts', headers=headers)
    if result:
        print(f'获取到 {len(result)} 条告警:')
        for alert in result[:3]:  # 只显示前3条
            print(f"\n- [{alert['severity']}] {alert['type']}")
            print(f"  消息: {alert['message']}")
            print(f"  状态: {alert['status']}")
            print(f"  时间: {alert['created_at']}")
    else:
        print('获取告警列表失败')
    return result

def test_monitor_settings(token=None):
    """测试监控设置"""
    print('\n=== 测试监控设置 ===')
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    } if token else {}
    
    result = safe_request('GET', f'{BASE_URL}/monitor/settings', headers=headers)
    if result:
        print('阈值设置:')
        print(f"CPU使用率阈值: {result['thresholds']['cpu_usage']}%")
        print(f"内存使用率阈值: {result['thresholds']['memory_usage']}%")
        print(f"磁盘使用率阈值: {result['thresholds']['disk_usage']}%")
        print(f"网络延迟阈值: {result['thresholds']['network_latency']}ms")
        
        print('\n通知设置:')
        print(f"邮件通知: {'启用' if result['notification']['email'] else '禁用'}")
        print(f"Slack通知: {'启用' if result['notification']['slack'] else '禁用'}")
        print(f"Webhook通知: {'启用' if result['notification']['webhook'] else '禁用'}")
        
        print('\n告警规则:')
        for rule in result['alert_rules']:
            print(f"\n- {rule['name']}")
            print(f"  条件: {rule['condition']}")
            print(f"  级别: {rule['severity']}")
            print(f"  状态: {'启用' if rule['enabled'] else '禁用'}")
    else:
        print('获取监控设置失败')
    return result

def run_tests():
    """运行所有测试"""
    print('开始测试监控系统API...\n')
    
    # 1. 测试认证
    token = test_auth()
    
    if token:
        # 2. 测试监控概览
        test_monitor_overview(token)
        
        # 3. 测试告警列表
        test_monitor_alerts(token)
        
        # 4. 测试监控设置
        test_monitor_settings(token)
    else:
        print('\n认证失败，无法继续测试')
    
    print('\n测试完成!')

if __name__ == '__main__':
    run_tests()