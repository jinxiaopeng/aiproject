import requests
import json
import time

# 测试配置
BASE_URL = 'http://localhost:3017'
USERNAME = 'admin'  # 管理员用户名
PASSWORD = 'jxp1210'  # 管理员密码

def login():
    """登录并获取token"""
    login_url = f'{BASE_URL}/api/auth/login'
    
    # 构造登录表单数据
    form_data = {
        'username': USERNAME,
        'password': PASSWORD,
        'grant_type': 'password'  # OAuth2 要求
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        # 使用 URLSearchParams 格式发送数据
        data = '&'.join(f'{k}={v}' for k, v in form_data.items())
        response = requests.post(
            login_url, 
            data=data,
            headers=headers
        )
        response.raise_for_status()
        
        data = response.json()
        token = data.get('access_token')  # 使用正确的token字段名
        print('✅ 登录成功')
        print(f'响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}')
        return token
    except Exception as e:
        print(f'❌ 登录失败: {str(e)}')
        if hasattr(e, 'response'):
            print(f'错误响应: {e.response.text}')
        return None

def test_monitor_page(token):
    """测试监控页面访问"""
    headers = {'Authorization': f'Bearer {token}'}
    monitor_url = f'{BASE_URL}/monitor'
    
    try:
        response = requests.get(monitor_url, headers=headers)
        response.raise_for_status()
        print('✅ 监控页面访问成功')
        print(f'响应数据: {response.text[:200]}...')  # 只显示前200个字符
    except Exception as e:
        print(f'❌ 监控页面访问失败: {str(e)}')
        if hasattr(e, 'response'):
            print(f'错误响应: {e.response.text}')

def test_monitor_apis(token):
    """测试监控相关的API接口"""
    headers = {'Authorization': f'Bearer {token}'}
    apis = {
        '监控统计': '/api/monitor/stats',
        '系统指标': '/api/monitor/metrics',
        '告警趋势': '/api/monitor/trends?timeRange=today',
        '实时日志': '/api/monitor/logs?limit=50',
        '告警列表': '/api/monitor/alerts'
    }
    
    for name, path in apis.items():
        try:
            response = requests.get(f'{BASE_URL}{path}', headers=headers)
            response.raise_for_status()
            data = response.json()
            print(f'✅ {name}API测试成功')
            print(f'响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}')
        except Exception as e:
            print(f'❌ {name}API测试失败: {str(e)}')
            if hasattr(e, 'response'):
                print(f'错误响应: {e.response.text}')
        time.sleep(1)  # 避免请求过快

def main():
    print('开始测试监控系统...')
    print(f'测试环境: {BASE_URL}')
    
    # 1. 登录
    token = login()
    if not token:
        print('登录失败,终止测试')
        return
        
    # 2. 测试监控页面访问
    test_monitor_page(token)
    
    # 3. 测试监控API接口
    test_monitor_apis(token)
    
    print('测试完成!')

if __name__ == '__main__':
    main() 