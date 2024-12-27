import requests
import json
import logging
import time

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000/api"

def login():
    try:
        data = {
            "username": "admin",
            "password": "jxp1210"
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        logger.debug(f"Login request: {data}")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data=data,
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        logger.debug(f"Login response: {response.json()}")
        return response.json().get("access_token")
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        return None

def get_labs(token):
    try:
        logger.debug("Getting labs list")
        response = requests.get(
            f"{BASE_URL}/practice/labs",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        response.raise_for_status()
        logger.debug(f"Labs list response: {response.json()}")
        return response.json()
    except Exception as e:
        logger.error(f"Get labs failed: {str(e)}")
        return None

def start_lab(token, lab_id):
    try:
        logger.debug(f"Starting lab {lab_id}")
        response = requests.post(
            f"{BASE_URL}/practice/labs/{lab_id}/start",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        response.raise_for_status()
        logger.debug(f"Start lab response: {response.json()}")
        return response.json()
    except Exception as e:
        logger.error(f"Start lab failed: {str(e)}")
        return None

def stop_lab(token, lab_id):
    try:
        logger.debug(f"Stopping lab {lab_id}")
        response = requests.post(
            f"{BASE_URL}/practice/labs/{lab_id}/stop",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        response.raise_for_status()
        logger.debug(f"Stop lab response: {response.json()}")
        return response.json()
    except Exception as e:
        logger.error(f"Stop lab failed: {str(e)}")
        return None

def verify_flag(token, lab_id, flag):
    try:
        logger.debug(f"Verifying flag for lab {lab_id}")
        response = requests.post(
            f"{BASE_URL}/practice/labs/{lab_id}/verify",
            headers={"Authorization": f"Bearer {token}"},
            params={"flag": flag},
            timeout=5
        )
        response.raise_for_status()
        logger.debug(f"Verify flag response: {response.json()}")
        return response.json()
    except Exception as e:
        logger.error(f"Verify flag failed: {str(e)}")
        return None

def test_sql_injection_lab():
    # 1. Login
    token = login()
    if not token:
        logger.error("Login failed!")
        return

    # 2. Get labs list
    labs = get_labs(token)
    if not labs:
        logger.error("Failed to get labs list!")
        return
    
    # 3. Start SQL injection lab
    lab_id = 1  # SQL注入靶场的ID
    logger.info(f"Starting lab with ID: {lab_id}")
    result = start_lab(token, lab_id)
    
    if not result:
        logger.error("Failed to start lab!")
        return
        
    if result.get("url"):
        lab_url = result["url"]
        logger.info(f"Lab is running at: {lab_url}")
        print("Lab started successfully!")

        # 等待一段时间让用户测试
        print("Testing the lab for 10 seconds...")
        time.sleep(10)

        # 测试提交错误的flag
        wrong_flag = "wrong_flag"
        logger.info(f"Testing wrong flag: {wrong_flag}")
        verify_result = verify_flag(token, lab_id, wrong_flag)
        if verify_result:
            print(f"Wrong flag result: {verify_result}")

        # 测试提交正确的flag
        correct_flag = "flag{sql_injection_success}"
        logger.info(f"Testing correct flag: {correct_flag}")
        verify_result = verify_flag(token, lab_id, correct_flag)
        if verify_result:
            print(f"Correct flag result: {verify_result}")

        # 停止靶场
        logger.info(f"Stopping lab {lab_id}")
        stop_result = stop_lab(token, lab_id)
        if stop_result:
            print(f"Lab stopped: {stop_result}")
        else:
            print("Failed to stop lab!")

if __name__ == "__main__":
    test_sql_injection_lab() 