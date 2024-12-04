from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LabBase(BaseModel):
    title: str = Field(..., description="实验标题")
    description: str = Field(..., description="实验描述")
    category: str = Field(..., description="实验分类")
    difficulty: str = Field(..., description="实验难度")
    duration: int = Field(..., description="预计时长(分钟)")
    docker_image: str = Field(..., description="Docker镜像")
    ports: str = Field(..., description="端口映射")
    prerequisites: List[str] = Field(default=[], description="前置要求")
    tags: List[str] = Field(default=[], description="实验标签")

class LabCreate(LabBase):
    pass

class LabUpdate(LabBase):
    pass

class Lab(LabBase):
    id: str = Field(..., description="实验ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    status: str = Field(..., description="实验状态")
    participants_count: int = Field(default=0, description="参与人数")
    completion_rate: float = Field(default=0.0, description="完成率")
    
    class Config:
        orm_mode = True

class LabStep(BaseModel):
    id: str = Field(..., description="步骤ID")
    title: str = Field(..., description="步骤标题")
    description: str = Field(..., description="步骤描述")
    content: str = Field(..., description="步骤内容")
    order: int = Field(..., description="步骤顺序")
    hints: List[str] = Field(default=[], description="提示信息")
    verification: Optional[str] = Field(None, description="验证方法")

class LabReport(BaseModel):
    content: str = Field(..., description="报告内容")
    screenshots: List[str] = Field(default=[], description="截图列表")
    
    class Config:
        orm_mode = True

class LabProgress(BaseModel):
    lab_id: str = Field(..., description="实验ID")
    user_id: str = Field(..., description="用户ID")
    status: str = Field(..., description="实验状态")
    completed_steps: List[str] = Field(default=[], description="已完成步骤")
    started_at: Optional[datetime] = Field(None, description="开始时间")
    completed_at: Optional[datetime] = Field(None, description="完成时间")
    
    class Config:
        orm_mode = True 