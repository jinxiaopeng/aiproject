import requests
import time
import logging
import subprocess
import sys

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_container_status(container_name):
    """检查容器状态"""
    try:
        result = subprocess.run(
            f'docker ps --filter name={container_name} --format "{{{{.Status}}}}"',
            shell=True, capture_output=True, text=True
        )
        return result.returncode == 0 and 'Up' in result.stdout
    except Exception:
        return False

def test_challenge_manager():
    """测试挑战管理器的功能"""
    base_url = 'http://localhost:8000'

    try:
        # 测试启动基础SQL注入挑战
        logger.info("Testing basic SQL injection challenge...")
        response = requests.post(f'{base_url}/api/challenge/start', json={
            'challengeId': 1,
            'containerName': 'sql_injection_basic',
            'port': 8081
        })
        
        if response.status_code == 200 and response.json()['success']:
            logger.info("✓ Basic challenge container started successfully")
            
            # 验证容器是否在运行
            if check_container_status('sql_injection_basic'):
                logger.info("✓ Container is running")
                
                # 测试访问Web服务
                time.sleep(2)  # 等待服务启动
                try:
                    web_response = requests.get('http://localhost:8081')
                    if web_response.status_code == 200:
                        logger.info("✓ Web service is accessible")
                    else:
                        logger.error("✗ Web service is not accessible")
                except requests.exceptions.ConnectionError:
                    logger.error("✗ Could not connect to web service")
            else:
                logger.error("✗ Container is not running")
        else:
            logger.error(f"✗ Failed to start basic challenge: {response.json().get('message', 'Unknown error')}")

        # 测试启动进阶SQL注入挑战
        logger.info("\nTesting advanced SQL injection challenge...")
        response = requests.post(f'{base_url}/api/challenge/start', json={
            'challengeId': 2,
            'containerName': 'sql_injection_advanced',
            'port': 8082
        })
        
        if response.status_code == 200 and response.json()['success']:
            logger.info("✓ Advanced challenge container started successfully")
            
            # 验证容器是否在运行
            if check_container_status('sql_injection_advanced'):
                logger.info("✓ Container is running")
                
                # 测试访问Web服务
                time.sleep(2)  # 等待服务启动
                try:
                    web_response = requests.get('http://localhost:8082')
                    if web_response.status_code == 200:
                        logger.info("✓ Web service is accessible")
                    else:
                        logger.error("✗ Web service is not accessible")
                except requests.exceptions.ConnectionError:
                    logger.error("✗ Could not connect to web service")
            else:
                logger.error("✗ Container is not running")
        else:
            logger.error(f"✗ Failed to start advanced challenge: {response.json().get('message', 'Unknown error')}")

        # 测试停止容器
        logger.info("\nTesting container stop functionality...")
        
        # 停止基础挑战
        response = requests.post(f'{base_url}/api/challenge/stop', json={
            'containerName': 'sql_injection_basic'
        })
        if response.status_code == 200 and response.json()['success']:
            logger.info("✓ Basic challenge container stopped successfully")
            if not check_container_status('sql_injection_basic'):
                logger.info("✓ Container is no longer running")
            else:
                logger.error("✗ Container is still running")
        else:
            logger.error("✗ Failed to stop basic challenge container")

        # 停止进阶挑战
        response = requests.post(f'{base_url}/api/challenge/stop', json={
            'containerName': 'sql_injection_advanced'
        })
        if response.status_code == 200 and response.json()['success']:
            logger.info("✓ Advanced challenge container stopped successfully")
            if not check_container_status('sql_injection_advanced'):
                logger.info("✓ Container is no longer running")
            else:
                logger.error("✗ Container is still running")
        else:
            logger.error("✗ Failed to stop advanced challenge container")

    except requests.exceptions.ConnectionError:
        logger.error("✗ Failed to connect to challenge manager. Is it running?")
        sys.exit(1)
    except Exception as e:
        logger.error(f"✗ Test failed: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    logger.info("Starting challenge system tests...")
    test_challenge_manager() 