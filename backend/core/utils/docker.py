import docker
from docker.errors import DockerException
import logging
from typing import Optional, Dict, Any
from ..config.lab_db import DOCKER_CONFIG, LAB_CONFIG

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建Docker客户端
try:
    client = docker.from_env()
    logger.info("Docker client initialized successfully")
except DockerException as e:
    logger.error(f"Failed to initialize Docker client: {str(e)}")
    raise

def create_lab_container(
    image: str,
    environment: Optional[Dict[str, Any]] = None,
    memory_limit: str = LAB_CONFIG['default_memory_limit'],
    cpu_limit: float = LAB_CONFIG['default_cpu_limit']
) -> str:
    """
    创建并启动一个实验容器
    
    Args:
        image: Docker镜像名称
        environment: 环境变量
        memory_limit: 内存限制
        cpu_limit: CPU限制
        
    Returns:
        container_id: 容器ID
    """
    try:
        # 确保镜像存在
        try:
            client.images.get(image)
            logger.info(f"Image {image} found locally")
        except docker.errors.ImageNotFound:
            logger.info(f"Pulling image {image}")
            client.images.pull(image)
        
        # 创建容器
        container = client.containers.run(
            image=image,
            detach=True,
            environment=environment or {},
            network=LAB_CONFIG['network_name'],
            mem_limit=memory_limit,
            nano_cpus=int(cpu_limit * 1e9),  # Convert CPU limit to nano CPUs
            restart_policy={"Name": "unless-stopped"},
            security_opt=['seccomp=unconfined'],  # 允许一些安全相关的系统调用
            cap_add=['NET_ADMIN'],  # 允许网络配置
            privileged=True  # 注意：在生产环境中要谨慎使用
        )
        
        logger.info(f"Container {container.id} created successfully")
        return container.id
        
    except DockerException as e:
        logger.error(f"Failed to create container: {str(e)}")
        raise

def stop_lab_container(container_id: str) -> None:
    """
    停止并删除实验容器
    
    Args:
        container_id: 容器ID
    """
    try:
        container = client.containers.get(container_id)
        
        # 停止容器
        logger.info(f"Stopping container {container_id}")
        container.stop(timeout=10)
        
        # 删除容器
        logger.info(f"Removing container {container_id}")
        container.remove(force=True)
        
    except docker.errors.NotFound:
        logger.warning(f"Container {container_id} not found")
    except DockerException as e:
        logger.error(f"Failed to stop container {container_id}: {str(e)}")
        raise

def get_container_status(container_id: str) -> Dict[str, Any]:
    """
    获取容器状态信息
    
    Args:
        container_id: 容器ID
        
    Returns:
        dict: 包含容器状态信息的字典
    """
    try:
        container = client.containers.get(container_id)
        return {
            'id': container.id,
            'status': container.status,
            'created': container.attrs['Created'],
            'started': container.attrs['State']['StartedAt'],
            'network': container.attrs['NetworkSettings'],
            'memory_usage': container.stats(stream=False)['memory_stats']['usage'],
            'cpu_usage': container.stats(stream=False)['cpu_stats']['cpu_usage']['total_usage']
        }
    except docker.errors.NotFound:
        logger.warning(f"Container {container_id} not found")
        return {'status': 'not_found'}
    except DockerException as e:
        logger.error(f"Failed to get container status: {str(e)}")
        raise

def cleanup_expired_containers() -> None:
    """
    清理过期的容器
    """
    try:
        containers = client.containers.list(
            filters={'label': 'lab_container=true'}
        )
        
        for container in containers:
            # 检查容器是否过期
            created_time = container.attrs['Created']
            # TODO: 实现过期检查逻辑
            
            if True:  # 如果容器过期
                logger.info(f"Cleaning up expired container {container.id}")
                stop_lab_container(container.id)
                
    except DockerException as e:
        logger.error(f"Failed to cleanup containers: {str(e)}")
        raise

def ensure_lab_network() -> None:
    """
    确保实验网络存在
    """
    try:
        networks = client.networks.list(names=[LAB_CONFIG['network_name']])
        if not networks:
            logger.info(f"Creating network {LAB_CONFIG['network_name']}")
            client.networks.create(
                LAB_CONFIG['network_name'],
                driver="bridge",
                internal=True  # 内部网络，不能访问外网
            )
    except DockerException as e:
        logger.error(f"Failed to ensure lab network: {str(e)}")
        raise 