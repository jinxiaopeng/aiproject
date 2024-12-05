import docker
import yaml
import tempfile
import os
from typing import Tuple, Optional
from datetime import datetime

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
        self.network_name = "ctf_network"
        self._ensure_network()
    
    def _ensure_network(self):
        """确保CTF网络存在"""
        try:
            self.client.networks.get(self.network_name)
        except docker.errors.NotFound:
            self.client.networks.create(
                self.network_name,
                driver="bridge",
                internal=True  # 内部网络，不允许直接访问外网
            )
    
    async def create_container(
        self,
        image: str,
        compose_config: Optional[str] = None,
        port_mapping: Optional[str] = None
    ) -> Tuple[str, str]:
        """创建并启动容器"""
        try:
            if compose_config:
                # 使用docker-compose配置
                with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
                    f.write(compose_config)
                    compose_file = f.name
                
                try:
                    project = self.client.compose.up(
                        project_name=f"ctf_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                        compose_files=[compose_file]
                    )
                    container_id = project.containers[0].id
                finally:
                    os.unlink(compose_file)
            else:
                # 直接创建单个容器
                ports = {}
                if port_mapping:
                    host_port, container_port = port_mapping.split(':')
                    ports[container_port] = host_port
                
                container = self.client.containers.run(
                    image=image,
                    detach=True,
                    network=self.network_name,
                    ports=ports,
                    environment={
                        "FLAG_SEED": os.urandom(16).hex()  # 为每个实例生成唯一的flag
                    },
                    mem_limit="256m",  # 限制内存使用
                    cpu_period=100000,
                    cpu_quota=50000,  # 限制CPU使用（0.5核）
                    restart_policy={"Name": "on-failure", "MaximumRetryCount": 3}
                )
                container_id = container.id
            
            # 获取容器信息
            container = self.client.containers.get(container_id)
            container_ports = container.ports
            
            # 构建访问URL
            if container_ports:
                # 获取第一个映射端口
                port_info = list(container_ports.values())[0][0]
                instance_url = f"http://localhost:{port_info['HostPort']}"
            else:
                instance_url = None
            
            return container_id, instance_url
            
        except Exception as e:
            raise Exception(f"创建容器失败: {str(e)}")
    
    async def stop_container(self, container_id: str):
        """停止并删除容器"""
        try:
            container = self.client.containers.get(container_id)
            container.stop(timeout=10)
            container.remove(force=True)
        except Exception as e:
            raise Exception(f"停止容器失败: {str(e)}")
    
    async def cleanup_expired_containers(self):
        """清理过期的容器"""
        containers = self.client.containers.list(
            filters={"label": "ctf_challenge=true"}
        )
        
        for container in containers:
            created = container.attrs['Created']
            created_time = datetime.strptime(created.split('.')[0], '%Y-%m-%dT%H:%M:%S')
            
            # 如果容器运行超过2小时，则停止并删除
            if (datetime.utcnow() - created_time).total_seconds() > 7200:
                await self.stop_container(container.id)

# 创建Docker管理器实例
docker_manager = DockerManager() 