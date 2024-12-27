import requests
import json
import time
import subprocess
from typing import Optional, Dict, Any

class TestEnvironment:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.session = requests.Session()
        self.challenge_dir = "challenges/web_security/sql_injection"
    
    def run_docker_command(self, command: str) -> Dict[str, Any]:
        """运行docker命令"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.challenge_dir,
                capture_output=True,
                text=True
            )
            print(f"命令: {command}")
            print(f"输出: {result.stdout}")
            if result.stderr:
                print(f"错误: {result.stderr}")
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            print(f"执行命令失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def start_container(self, challenge_type: str = "sql_injection_basic") -> Dict[str, Any]:
        """启动容器"""
        print("\n=== 启动容器 ===")
        return self.run_docker_command("docker-compose up -d")
    
    def stop_container(self, container_id: str = "") -> Dict[str, Any]:
        """停止容器"""
        print("\n=== 停止容器 ===")
        return self.run_docker_command("docker-compose down")
    
    def get_container_status(self, container_id: str = "") -> Dict[str, Any]:
        """获取容器状态"""
        print("\n=== 容器状态 ===")
        # 使用docker ps检查所有容器
        result = self.run_docker_command("docker ps -a")
        # 使用docker-compose ps检查compose管理的容器
        compose_result = self.run_docker_command("docker-compose ps")
        # 检查端口占用
        port_result = self.run_docker_command("netstat -ano | findstr :8081")
        return {
            "docker_ps": result,
            "compose_ps": compose_result,
            "port_check": port_result
        }

def main():
    # 创建测试环境
    env = TestEnvironment()
    
    try:
        # 1. 检查初始状态
        print("\n=== 检查初始状态 ===")
        env.get_container_status()
        
        # 2. 启动容器
        print("\n=== 测试启动容器 ===")
        result = env.start_container()
        if not result["success"]:
            raise Exception("启动容器失败")
        
        # 等待容器启动
        print("\n等待容器启动...")
        time.sleep(10)
        
        # 3. 检查容器状态
        print("\n=== 检查容器状态 ===")
        env.get_container_status()
        
        # 4. 测试Web应用
        print("\n=== 测试Web应用 ===")
        try:
            response = requests.get("http://localhost:8081")
            print(f"Web应用响应状态码: {response.status_code}")
            print(f"Web应用响应内容: {response.text[:200]}...")  # 只显示前200个字符
        except Exception as e:
            print(f"访问Web应用失败: {str(e)}")
        
        # 5. 停止容器
        print("\n=== 停止容器 ===")
        env.stop_container()
        
        # 等待容器停止
        print("\n等待容器停止...")
        time.sleep(5)
        
        # 6. 检查最终状态
        print("\n=== 最终状态检查 ===")
        env.get_container_status()
        
        # 7. 再次尝试访问Web应用（应该失败）
        print("\n=== 验证Web应用已停止 ===")
        try:
            response = requests.get("http://localhost:8081")
            print(f"警告：Web应用仍然可访问，状态码: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("正常：Web应用已无法访问")
        except Exception as e:
            print(f"其他错误: {str(e)}")
        
    except Exception as e:
        print(f"\n测试过程中出现错误: {str(e)}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main() 