import os
import mysql.connector
from pathlib import Path
from typing import Dict, List, Optional

from core.logger import system_logger

class ConfigValidator:
    """配置验证器"""
    
    def __init__(self):
        self.errors: List[str] = []
    
    def validate_database_config(self, config: Dict) -> bool:
        """验证数据库配置"""
        try:
            # 检查必要的配置项
            required_fields = ['host', 'user', 'password', 'database']
            for field in required_fields:
                if field not in config:
                    self.errors.append(f"数据库配置缺少必要字段: {field}")
                    return False
            
            # 尝试连接数据库
            conn = mysql.connector.connect(**config)
            conn.close()
            return True
            
        except Exception as e:
            self.errors.append(f"数据库配置验证失败: {str(e)}")
            return False
    
    def validate_jwt_config(self, config: Dict) -> bool:
        """验证JWT配置"""
        try:
            # 检查必要的配置项
            required_fields = ['jwt_secret_key', 'jwt_algorithm', 'access_token_expire_minutes']
            for field in required_fields:
                if field not in config:
                    self.errors.append(f"JWT配置缺少必要字段: {field}")
                    return False
            
            # 验证密钥长度
            if len(config['jwt_secret_key']) < 32:
                self.errors.append("JWT密钥长度不足32字符")
                return False
            
            # 验证算法
            valid_algorithms = ['HS256', 'HS384', 'HS512']
            if config['jwt_algorithm'] not in valid_algorithms:
                self.errors.append(f"不支持的JWT算法: {config['jwt_algorithm']}")
                return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"JWT配置验证失败: {str(e)}")
            return False
    
    def validate_app_config(self, config: Dict) -> bool:
        """验证应用配置"""
        try:
            # 检查必要的配置项
            required_fields = ['debug', 'host', 'port', 'workers']
            for field in required_fields:
                if field not in config:
                    self.errors.append(f"应用配置缺少必要字段: {field}")
                    return False
            
            # 验证端口范围
            if not (1024 <= config['port'] <= 65535):
                self.errors.append(f"无效的端口号: {config['port']}")
                return False
            
            # 验证工作进程数
            if config['workers'] < 1:
                self.errors.append(f"工作进程数必须大于0: {config['workers']}")
                return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"应用配置验证失败: {str(e)}")
            return False
    
    def validate_log_config(self, config: Dict) -> bool:
        """验证日志配置"""
        try:
            # 检查必要的配置项
            required_fields = ['level', 'format', 'file']
            for field in required_fields:
                if field not in config:
                    self.errors.append(f"日志配置缺少必要字段: {field}")
                    return False
            
            # 验证日志级别
            valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
            if config['level'].upper() not in valid_levels:
                self.errors.append(f"无效的日志级别: {config['level']}")
                return False
            
            # 验证日志文件路径
            log_path = Path(config['file'])
            log_dir = log_path.parent
            if not log_dir.exists():
                try:
                    log_dir.mkdir(parents=True)
                except Exception as e:
                    self.errors.append(f"无法创建日志目录: {str(e)}")
                    return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"日志配置验证失败: {str(e)}")
            return False
    
    def validate_security_config(self, config: Dict) -> bool:
        """验证安全配置"""
        try:
            # 检查必要的配置项
            required_fields = ['allowed_hosts', 'cors_origins', 'rate_limit']
            for field in required_fields:
                if field not in config:
                    self.errors.append(f"安全配置缺少必要字段: {field}")
                    return False
            
            # 验证速率限制
            if config['rate_limit'] < 1:
                self.errors.append(f"速率限制必须大于0: {config['rate_limit']}")
                return False
            
            return True
            
        except Exception as e:
            self.errors.append(f"安全配置验证失败: {str(e)}")
            return False
    
    def validate_all(self, config: Dict) -> bool:
        """验证所有配置"""
        try:
            self.errors = []  # 清空错误列表
            
            # 验证各个配置部分
            database_valid = self.validate_database_config(config.get('database', {}))
            jwt_valid = self.validate_jwt_config(config.get('jwt', {}))
            app_valid = self.validate_app_config(config.get('app', {}))
            log_valid = self.validate_log_config(config.get('log', {}))
            security_valid = self.validate_security_config(config.get('security', {}))
            
            # 记录验证结果
            if self.errors:
                system_logger.error("配置验证失败", "config", {
                    'errors': self.errors
                })
                return False
            
            system_logger.info("配置验证成功", "config")
            return True
            
        except Exception as e:
            self.errors.append(f"配置验证过程出错: {str(e)}")
            system_logger.error("配置验证过程出错", "config", {
                'error': str(e)
            })
            return False
    
    def get_errors(self) -> List[str]:
        """获取验证错误信息"""
        return self.errors

# 创建配置验证器实例
config_validator = ConfigValidator() 