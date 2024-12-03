from typing import Dict, List, Optional
import os
import mysql.connector
from pydantic import BaseModel, validator
import docker
from pathlib import Path
from .logger import system_logger

class DatabaseConfig(BaseModel):
    host: str
    user: str
    password: str
    database: str
    port: int = 3306
    
    @validator('host')
    def validate_host(cls, v):
        if not v:
            raise ValueError("数据库主机不能为空")
        return v
        
    def test_connection(self) -> bool:
        """测试数据库连接"""
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            conn.close()
            return True
        except Exception as e:
            system_logger.error(f"数据库连接测试失败: {str(e)}", "config")
            return False

class DockerConfig(BaseModel):
    host: Optional[str] = None
    api_version: Optional[str] = None
    
    def test_connection(self) -> bool:
        """测试Docker连接"""
        try:
            client = docker.from_env()
            client.ping()
            return True
        except Exception as e:
            system_logger.error(f"Docker连接测试失败: {str(e)}", "config")
            return False

class SecurityConfig(BaseModel):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    @validator('jwt_secret_key')
    def validate_secret_key(cls, v):
        if not v or len(v) < 32:
            raise ValueError("JWT密钥长度必须至少为32个字符")
        return v

class PathConfig(BaseModel):
    upload_dir: Path
    temp_dir: Path
    log_dir: Path
    
    @validator('*')
    def validate_directory(cls, v):
        path = Path(v)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise ValueError(f"无法创建目录 {v}: {str(e)}")
        return path

class AppConfig(BaseModel):
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    reload: bool = False
    
    @validator('workers')
    def validate_workers(cls, v):
        if v < 1:
            raise ValueError("workers数量必须大于0")
        return v

class ConfigValidator:
    def __init__(self):
        self.errors: List[str] = []
        
    def validate_database_config(self, config: Dict) -> bool:
        """验证数据库配置"""
        try:
            db_config = DatabaseConfig(**config)
            if not db_config.test_connection():
                self.errors.append("数据库连接测试失败")
                return False
            return True
        except Exception as e:
            self.errors.append(f"数据库置验证失败: {str(e)}")
            return False
            
    def validate_docker_config(self, config: Dict) -> bool:
        """验证Docker配置"""
        try:
            docker_config = DockerConfig(**config)
            if not docker_config.test_connection():
                self.errors.append("Docker连接测试失败")
                return False
            return True
        except Exception as e:
            self.errors.append(f"Docker配置验证失败: {str(e)}")
            return False
            
    def validate_security_config(self, config: Dict) -> bool:
        """验证安全配置"""
        try:
            SecurityConfig(**config)
            return True
        except Exception as e:
            self.errors.append(f"安全配置验证失败: {str(e)}")
            return False
            
    def validate_path_config(self, config: Dict) -> bool:
        """验证路径配置"""
        try:
            PathConfig(**config)
            return True
        except Exception as e:
            self.errors.append(f"路径配置验证失败: {str(e)}")
            return False
            
    def validate_app_config(self, config: Dict) -> bool:
        """验证应用配置"""
        try:
            AppConfig(**config)
            return True
        except Exception as e:
            self.errors.append(f"应用配置验证失败: {str(e)}")
            return False
            
    def validate_all(self, config: Dict) -> bool:
        """验证所有配置"""
        self.errors = []
        is_valid = True
        
        # 验证数据库配置
        if not self.validate_database_config(config.get('database', {})):
            is_valid = False
            
        # 验证Docker配置
        if not self.validate_docker_config(config.get('docker', {})):
            is_valid = False
            
        # 验证安全配置
        if not self.validate_security_config(config.get('security', {})):
            is_valid = False
            
        # 验证路径配置
        if not self.validate_path_config(config.get('paths', {})):
            is_valid = False
            
        # 验证应用配置
        if not self.validate_app_config(config.get('app', {})):
            is_valid = False
            
        if not is_valid:
            system_logger.error("配置验证失败", "config", {
                'errors': self.errors
            })
            
        return is_valid
        
    def get_errors(self) -> List[str]:
        """获取验证错误信息"""
        return self.errors

# 创建全局配置验证器实例
config_validator = ConfigValidator() 