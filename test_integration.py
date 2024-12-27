import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_auth_and_connection():
    """测试认证和基本连接"""
    # 基础配置
    base_url = os.getenv("BACKEND_URL", "http://localhost:3000")
    
    # 1. 测试登录
    login_data = {
        "username": os.getenv("TEST_USERNAME", "test_user"),
        "password": os.getenv("TEST_PASSWORD", "test_password")
    }
    
    print(f"\n1. Testing Login with {login_data['username']}")
    response = requests.post(f"{base_url}/api/auth/login", json=login_data)
    print("Status Code:", response.status_code)
    
    if response.status_code == 200:
        result = response.json()
        token = result.get("token")
        print("Login successful!")
        print("Token received:", token[:20] + "..." if token else None)
        return token
    else:
        print("Login failed:", response.text)
        return None

def test_challenge_apis(token):
    """测试挑战相关的API"""
    base_url = os.getenv("BACKEND_URL", "http://localhost:3000")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. 获取挑战列表
    print("\n2. Testing Get Challenges")
    response = requests.get(f"{base_url}/api/challenges", headers=headers)
    print("Status Code:", response.status_code)
    
    if response.status_code == 200:
        challenges = response.json()
        print(f"Found {len(challenges)} challenges")
        print("First challenge:", json.dumps(challenges[0], indent=2) if challenges else None)
        
        if challenges:
            challenge_id = challenges[0]["id"]
            
            # 3. 获取单个挑战详情
            print(f"\n3. Testing Get Challenge Detail (ID: {challenge_id})")
            response = requests.get(f"{base_url}/api/challenges/{challenge_id}", headers=headers)
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                detail = response.json()
                print("Challenge title:", detail.get("title"))
                print("Challenge status:", detail.get("status"))
            
            # 4. 开始挑战
            print(f"\n4. Testing Start Challenge (ID: {challenge_id})")
            response = requests.post(f"{base_url}/api/challenges/{challenge_id}/start", headers=headers)
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                result = response.json()
                print("Challenge started:", result.get("challenge", {}).get("title"))
                print("Progress:", result.get("progress", {}).get("status"))
            
            # 5. 提交flag测试
            test_flag = "test_flag"
            print(f"\n5. Testing Submit Flag (ID: {challenge_id})")
            response = requests.post(
                f"{base_url}/api/challenges/{challenge_id}/verify",
                headers=headers,
                json={"flag": test_flag}
            )
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                result = response.json()
                print("Submission successful:", result.get("success"))
                print("Points earned:", result.get("points"))
            else:
                print("Submission failed:", response.text)
            
            # 6. 获取用户统计
            print("\n6. Testing Get User Statistics")
            response = requests.get(f"{base_url}/api/challenges/statistics/me", headers=headers)
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                stats = response.json()
                print("Total points:", stats.get("total_points"))
                print("Completed challenges:", stats.get("completed_challenges"))

def main():
    """主测试流程"""
    print("Starting Integration Tests...")
    token = test_auth_and_connection()
    if token:
        test_challenge_apis(token)
    else:
        print("Tests stopped due to authentication failure")

if __name__ == "__main__":
    main() 