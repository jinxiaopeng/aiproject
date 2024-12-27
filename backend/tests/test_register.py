import requests
import random
import string
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API基础URL
BASE_URL = "http://localhost:8000/api"

def generate_random_string(length=8):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def test_register():
    """测试注册功能"""
    # 生成随机用户数据
    username = f"test_user_{generate_random_string()}"
    email = f"{username}@test.com"
    password = "Test123456"

    # 注册数据
    register_data = {
        "username": username,
        "email": email,
        "password": password
    }

    try:
        # 发送注册请求
        logger.info(f"Attempting to register user: {username}")
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        
        # 检查响应
        if response.status_code == 200:
            logger.info("Registration successful!")
            logger.info(f"Response: {response.json()}")
            return True
        else:
            logger.error(f"Registration failed with status code: {response.status_code}")
            logger.error(f"Error message: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        return False

def test_duplicate_username():
    """测试重复用户名"""
    # 使用相同的用户名，不同的邮箱
    username = f"test_user_{generate_random_string()}"
    password = "Test123456"

    # 第一次注册
    register_data1 = {
        "username": username,
        "email": f"{username}_1@test.com",
        "password": password
    }

    # 第二次注册（相同用户名）
    register_data2 = {
        "username": username,
        "email": f"{username}_2@test.com",
        "password": password
    }

    try:
        # 第一次注册
        logger.info(f"First registration attempt with username: {username}")
        response1 = requests.post(f"{BASE_URL}/auth/register", json=register_data1)
        
        # 第二次注册
        logger.info(f"Second registration attempt with same username: {username}")
        response2 = requests.post(f"{BASE_URL}/auth/register", json=register_data2)
        
        # 检查响应
        if response1.status_code == 200 and response2.status_code == 400:
            logger.info("Duplicate username test passed!")
            return True
        else:
            logger.error("Duplicate username test failed!")
            logger.error(f"First response: {response1.status_code} - {response1.text}")
            logger.error(f"Second response: {response2.status_code} - {response2.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error during duplicate username test: {str(e)}")
        return False

def test_duplicate_email():
    """测试重复邮箱"""
    # 使用相同的邮箱，不同的用户名
    email = f"test_{generate_random_string()}@test.com"
    password = "Test123456"

    # 第一次注册
    register_data1 = {
        "username": f"test_user1_{generate_random_string()}",
        "email": email,
        "password": password
    }

    # 第二次注册（相同邮箱）
    register_data2 = {
        "username": f"test_user2_{generate_random_string()}",
        "email": email,
        "password": password
    }

    try:
        # 第一次注册
        logger.info(f"First registration attempt with email: {email}")
        response1 = requests.post(f"{BASE_URL}/auth/register", json=register_data1)
        
        # 第二次注册
        logger.info(f"Second registration attempt with same email: {email}")
        response2 = requests.post(f"{BASE_URL}/auth/register", json=register_data2)
        
        # 检查响应
        if response1.status_code == 200 and response2.status_code == 400:
            logger.info("Duplicate email test passed!")
            return True
        else:
            logger.error("Duplicate email test failed!")
            logger.error(f"First response: {response1.status_code} - {response1.text}")
            logger.error(f"Second response: {response2.status_code} - {response2.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error during duplicate email test: {str(e)}")
        return False

def run_all_tests():
    """运行所有测试"""
    logger.info("Starting registration tests...")
    
    # 测试正常注册
    logger.info("\n=== Testing normal registration ===")
    test_register()
    
    # 测试重复用户名
    logger.info("\n=== Testing duplicate username ===")
    test_duplicate_username()
    
    # 测试重复邮箱
    logger.info("\n=== Testing duplicate email ===")
    test_duplicate_email()
    
    logger.info("\nAll tests completed!")

if __name__ == "__main__":
    run_all_tests() 