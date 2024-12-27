"""
靶场相关的数据模型
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, Optional, List
from datetime import datetime

class Link(BaseModel):
    """链接"""
    title: str = Field(..., description="链接标题")
    url: HttpUrl = Field(..., description="链接地址")

class Prerequisite(BaseModel):
    """前置知识"""
    title: str = Field(..., description="知识点标题")
    description: str = Field(..., description="知识点描述")
    links: Optional[List[Link]] = Field(None, description="相关链接")

class Environment(BaseModel):
    """环境配置"""
    type: str = Field(..., description="环境类型")
    version: Optional[str] = Field(None, description="版本")
    ports: Optional[List[int]] = Field(None, description="端口列表")
    notice: Optional[str] = Field(None, description="环境说明")
    setup: Optional[List[str]] = Field(None, description="环境准备步骤")

class TrainingStep(BaseModel):
    """训练步骤"""
    title: str = Field(..., description="步骤标题")
    description: str = Field(..., description="步骤描述")
    tips: Optional[List[str]] = Field(None, description="提示信息")
    tasks: Optional[List[str]] = Field(None, description="验证任务")
    required: Optional[bool] = Field(True, description="是否必须完成")

class ProcessConfig(BaseModel):
    """进程配置"""
    type: str = Field(..., description="进程类型 (如: python)")
    main_file: str = Field(..., description="主文件路径")
    port: Optional[int] = Field(None, description="服务端口")
    env: Optional[Dict[str, str]] = Field(None, description="环境变量")

class ResourceLimits(BaseModel):
    """资源限制配置"""
    max_memory: str = Field(..., description="最大内存限制 (如: 256M)")
    max_cpu: float = Field(..., ge=0, le=100, description="最大CPU使用率 (0-100)")
    max_processes: int = Field(..., gt=0, description="最大进程数")

class TimeoutConfig(BaseModel):
    """超时配置"""
    total_timeout: int = Field(
        3600,
        ge=300,
        le=86400,
        description="总运行时间限制（秒）"
    )
    idle_timeout: int = Field(
        1800,
        ge=300,
        le=43200,
        description="空闲时间限制（秒）"
    )
    cleanup_interval: int = Field(
        300,
        ge=60,
        le=3600,
        description="清理检查间隔（秒）"
    )

class ChallengeConfig(BaseModel):
    """靶场配置"""
    process_config: Optional[ProcessConfig] = None
    resource_limits: Optional[ResourceLimits] = None
    timeout_config: Optional[TimeoutConfig] = None

class ChallengeStatus(BaseModel):
    """靶场状态"""
    status: str = Field(..., description="运行状态")
    pid: Optional[int] = Field(None, description="进程ID")
    port: Optional[int] = Field(None, description="服务端口")
    cpu_percent: Optional[float] = Field(None, description="CPU使用率")
    memory_percent: Optional[float] = Field(None, description="内存使用率")
    memory_usage: Optional[int] = Field(None, description="内存使用量（字节）")
    io_read_bytes: Optional[int] = Field(None, description="IO读取字节数")
    io_write_bytes: Optional[int] = Field(None, description="IO写入字节数")
    last_update: Optional[datetime] = Field(None, description="最后更新时间")
    remaining_time: Optional[int] = Field(None, description="剩余时间（秒）")

class ChallengeBase(BaseModel):
    """靶场基本信息"""
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., description="靶场描述")
    category: str = Field(..., min_length=1, max_length=50)
    difficulty: str = Field(..., regex='^(easy|medium|hard)$')
    points: int = Field(..., ge=0)
    flag: str = Field(..., min_length=1, max_length=255)
    
    # 训练相关
    objectives: Optional[List[str]] = Field(None, description="学习目标")
    prerequisites: Optional[List[Prerequisite]] = Field(None, description="前置知识")
    environment: Optional[Environment] = Field(None, description="环境信息")
    notices: Optional[List[str]] = Field(None, description="注意事项")
    steps: Optional[List[TrainingStep]] = Field(None, description="训练步骤")
    hints: Optional[List[str]] = Field(None, description="提示信息")
    
    is_active: bool = True

class ChallengeCreate(ChallengeBase):
    """创建靶场请求"""
    process_config: Optional[ProcessConfig] = None
    resource_limits: Optional[ResourceLimits] = None
    timeout_config: Optional[TimeoutConfig] = None

class ChallengeUpdate(BaseModel):
    """更新靶场请求"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    difficulty: Optional[str] = Field(None, regex='^(easy|medium|hard)$')
    points: Optional[int] = Field(None, ge=0)
    flag: Optional[str] = Field(None, min_length=1, max_length=255)
    
    # 训练相关
    objectives: Optional[List[str]] = None
    prerequisites: Optional[List[Prerequisite]] = None
    environment: Optional[Environment] = None
    notices: Optional[List[str]] = None
    steps: Optional[List[TrainingStep]] = None
    hints: Optional[List[str]] = None
    
    is_active: Optional[bool] = None
    process_config: Optional[ProcessConfig] = None
    resource_limits: Optional[ResourceLimits] = None
    timeout_config: Optional[TimeoutConfig] = None

class ChallengeResponse(ChallengeBase):
    """靶场响应"""
    id: int
    process_config: Optional[Dict] = None
    resource_limits: Optional[Dict] = None
    timeout_config: Optional[Dict] = None
    current_status: Optional[str] = None
    last_start_time: Optional[datetime] = None
    completions: Optional[int] = None
    pass_rate: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class FlagSubmitResponse(BaseModel):
    """Flag提交响应"""
    correct: bool = Field(..., description="是否正确")
    points: Optional[int] = Field(None, description="获得的积分")
    message: Optional[str] = Field(None, description="提示信息")

class HintResponse(BaseModel):
    """提示响应"""
    hint: str = Field(..., description="提示内容")
    cost: int = Field(..., description="消耗的积分")