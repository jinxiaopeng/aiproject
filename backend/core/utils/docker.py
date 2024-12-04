import docker
from typing import Optional
from ..config import settings

client = docker.from_env()

async def create_lab_container(image: str, ports: Optional[dict] = None) -> str:
    """
    创建实验环境容器
    
    Args:
        image: Docker镜像名称
        ports: 端口映射配置
        
    Returns:
        str: 容器ID
    """
    try:
        # 拉取镜像
        client.images.pull(image)
        
        # 创建容器
        container = client.containers.run(
            image=image,
            detach=True,
            ports=ports,
            environment={
                "PLATFORM_NAME": settings.PLATFORM_NAME,
                "ENVIRONMENT": settings.ENVIRONMENT
            },
            restart_policy={"Name": "unless-stopped"},
            network_mode="bridge"
        )
        
        return container.id
    except Exception as e:
        raise Exception(f"创建容器失败: {str(e)}")

async def stop_lab_container(container_id: str):
    """
    停止并删除实验环境容器
    
    Args:
        container_id: 容器ID
    """
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
    except Exception as e:
        raise Exception(f"停止容器失败: {str(e)}")

async def get_container_status(container_id: str) -> str:
    """
    获取容器状态
    
    Args:
        container_id: 容器ID
        
    Returns:
        str: 容器状态
    """
    try:
        container = client.containers.get(container_id)
        return container.status
    except Exception:
        return "not_found"

async def get_container_logs(container_id: str, tail: int = 100) -> str:
    """
    获取容器日志
    
    Args:
        container_id: 容器ID
        tail: 返回最后几行日志
        
    Returns:
        str: 容器日志
    """
    try:
        container = client.containers.get(container_id)
        return container.logs(tail=tail).decode('utf-8')
    except Exception as e:
        raise Exception(f"获取容器日志失败: {str(e)}")

async def execute_command(container_id: str, command: str) -> tuple:
    """
    在容器中执行命令
    
    Args:
        container_id: 容器ID
        command: 要执行的命令
        
    Returns:
        tuple: (exit_code, output)
    """
    try:
        container = client.containers.get(container_id)
        exit_code, output = container.exec_run(command)
        return exit_code, output.decode('utf-8')
    except Exception as e:
        raise Exception(f"执行命令失败: {str(e)}")

async def cleanup_containers():
    """清理所有实验容器"""
    try:
        containers = client.containers.list(
            filters={"label": f"platform={settings.PLATFORM_NAME}"}
        )
        for container in containers:
            container.stop()
            container.remove()
    except Exception as e:
        raise Exception(f"清理容器失败: {str(e)}") 