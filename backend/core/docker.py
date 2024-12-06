import subprocess
import json
from typing import Tuple, Optional
import config
import traceback
import platform
import os
import time
import logging
import asyncio

class DockerManager:
    def __init__(self):
        """初始化Docker管理器"""
        self.logger = logging.getLogger(__name__)
        self.docker_available = False
        try:
            # 测试Docker连接
            result = subprocess.run(['docker', 'info'], capture_output=True, text=True)
            if result.returncode == 0:
                self.logger.info("Docker连接成功")
                self.docker_available = True
                # 确保网络存在
                self._ensure_network()
            else:
                self.logger.warning(f"Docker未运行或未安装: {result.stderr}")
        except Exception as e:
            self.logger.warning(f"Docker服务不可用: {str(e)}")
            self.logger.debug(f"错误详情: {traceback.format_exc()}")

    def _ensure_network(self):
        """确保Docker网络存在"""
        try:
            # 检查网络是否存在
            result = subprocess.run(
                ['docker', 'network', 'ls', '--format', '{{.Name}}'],
                capture_output=True,
                text=True
            )
            
            networks = result.stdout.split('\n')
            if config.CHALLENGE_NETWORK not in networks:
                # 创建网络
                result = subprocess.run(
                    ['docker', 'network', 'create', config.CHALLENGE_NETWORK],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    raise Exception(f"创建网络失败: {result.stderr}")
                print(f"创建Docker网络: {config.CHALLENGE_NETWORK}")
            else:
                print(f"Docker网络已存在: {config.CHALLENGE_NETWORK}")
        except Exception as e:
            print(f"确保Docker网络失败: {str(e)}")
            print(f"错误详情: {traceback.format_exc()}")

    async def create_container(
        self,
        image: str,
        port_mapping: Optional[str] = None,
        max_memory: str = "512m",
        cpu_limit: float = 0.5,
        timeout: int = 300
    ) -> Tuple[str, str]:
        """创建并启动容器，增加资源限制和超时控制"""
        if not self.docker_available:
            raise Exception("Docker服务不可用，请确保Docker Desktop已启动")
        container_id = None
        try:
            
            print(f"开始创建容器: {image}")
            print(f"端口映射: {port_mapping}")

            # 拉取镜像
            try:


                print(f"拉取镜像: {image}")
                result = subprocess.run(['docker', 'pull', image], capture_output=True, text=True)
                if result.returncode == 0:
                    print("镜像拉取成功")
                else:
                    print(f"拉取镜像失败: {result.stderr}")
                    print("尝试使用本地镜像")
            except Exception as e:
                print(f"拉取镜像失败: {str(e)}")
                print("尝试使用本地镜像")

            # 生成容器名称
            container_name = f"challenge_{int(time.time())}"

            # 构建运行命令
            run_cmd = [
                'docker', 'run', '-d',
                '--name', container_name,
                '--network', config.CHALLENGE_NETWORK,
                '--memory', max_memory,
                '--cpus', str(cpu_limit),
                '--health-cmd', 'curl -f http://localhost:8080/ || exit 1',
                '--health-interval', '10s',
                '--health-timeout', '5s',
                '--health-retries', '3',
                '--health-start-period', '30s'
            ]
            
            # 添加端口映射
            if port_mapping:
                host_port, container_port = port_mapping.split(':')  # 格式: 8080:80
                run_cmd.extend(['-p', f'{host_port}:{container_port}'])
            
            # 添加环境变量
            if 'webgoat' in image.lower():
                run_cmd.extend([
                    '-e', 'WEBGOAT_HOST=0.0.0.0',
                    '-e', 'WEBGOAT_PORT=8080',
                    '-e', 'WEBWOLF_HOST=0.0.0.0',
                    '-e', 'WEBWOLF_PORT=9090'
                ])
            
            # 添加镜像名
            run_cmd.append(image)
            
            # 添加超时停止
            run_cmd.extend(['--stop-timeout', str(timeout)])
            
            # 创建并启动容器
            print("开始创建并启动容器")
            print(f"运行命令: {' '.join(run_cmd)}")
            result = subprocess.run(run_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"创建容器失败: {result.stderr}")
            
            container_id = result.stdout.strip()
            print(f"容器创建成功: {container_id}")

            # 等待容器启动
            time.sleep(10)  # 等待10秒让容器完全启动

            # 获取容器信息
            print("获取容器网络信息")
            result = subprocess.run(
                ['docker', 'inspect', container_id],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise Exception(f"获取容器信息失败: {result.stderr}")
            
            container_info = json.loads(result.stdout)[0]
            container_ip = container_info['NetworkSettings']['Networks'][config.CHALLENGE_NETWORK]['IPAddress']
            print(f"容器IP: {container_ip}")

            # 构建访问URL
            if port_mapping:
                if 'webgoat' in image.lower():
                    instance_url = f"http://localhost:{host_port}/WebGoat"
                else:
                    instance_url = f"http://localhost:{host_port}"
            else:
                instance_url = f"http://{container_ip}"
            print(f"实例访问URL: {instance_url}")

            # 等待容器健康检查
            start_time = time.time()
            while time.time() - start_time < 60:  # 60秒超时
                result = subprocess.run(
                    ['docker', 'inspect', '--format', '{{.State.Health.Status}}', container_id],
                    capture_output=True,
                    text=True
                )
                if result.stdout.strip() == 'healthy':
                    self.logger.info(f"容器 {container_id} 健康检查通过")
                    break
                await asyncio.sleep(2)
            else:
                raise Exception("容器健康检查超时")

            return container_id, instance_url

        except Exception as e:
            self.logger.error(f"创建容器失败: {str(e)}")
            self.logger.debug(f"错误详情: {traceback.format_exc()}")
            if container_id:
                await self.stop_container(container_id)
            raise

    async def stop_container(self, container_id: str):
        """停止并删除容器，增加强制删除选项"""
        if not self.docker_available:
            self.logger.warning("Docker服务不可用，跳过容器停止")
            return
        try:
            self.logger.info(f"开始停止容器: {container_id}")
            
            # 停止容器，10秒超时
            result = subprocess.run(
                ['docker', 'stop', '-t', '10', container_id], 
                capture_output=True, 
                text=True
            )
            if result.returncode != 0:
                self.logger.warning(f"正常停止容器失败，尝试强制停止: {result.stderr}")
                result = subprocess.run(['docker', 'kill', container_id], capture_output=True, text=True)
            
            self.logger.info("容器已停止")

            # 删除容器
            self.logger.info("开始删除容器")
            result = subprocess.run(
                ['docker', 'rm', '-f', container_id], 
                capture_output=True, 
                text=True
            )
            if result.returncode != 0:
                raise Exception(f"删除容器失败: {result.stderr}")
            self.logger.info("容器已删除")

        except Exception as e:
            self.logger.error(f"停止容器失败: {str(e)}")
            self.logger.debug(f"错误详情: {traceback.format_exc()}")
            raise

# 创建Docker管理器实例
docker_manager = DockerManager()