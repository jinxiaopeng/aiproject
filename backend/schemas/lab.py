from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

# Lab模式
class LabBase(BaseModel):
    title: str
    description: str
    category: str
    difficulty: str
    points: int
    docker_image: str
    port_mapping: str
    hints: Optional[List[str]] = None
    resource_limits: Optional[Dict[str, Any]] = None

class LabCreate(LabBase):
    flag: str

class LabUpdate(LabBase):
    flag: Optional[str] = None
    is_active: Optional[bool] = None

class LabResponse(LabBase):
    id: int
    flag: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# LabInstance模式
class LabInstanceBase(BaseModel):
    lab_id: int
    user_id: int
    container_id: str
    instance_url: Optional[str] = None
    status: str

class LabInstanceCreate(LabInstanceBase):
    pass

class LabInstanceUpdate(BaseModel):
    status: Optional[str] = None
    end_time: Optional[datetime] = None

class LabInstanceResponse(LabInstanceBase):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None

    class Config:
        orm_mode = True

# LabProgress模式
class LabProgressBase(BaseModel):
    lab_id: int
    user_id: int
    status: str
    score: int = 0
    attempts: int = 0

class LabProgressCreate(LabProgressBase):
    pass

class LabProgressUpdate(BaseModel):
    status: Optional[str] = None
    score: Optional[int] = None
    attempts: Optional[int] = None
    completed_at: Optional[datetime] = None

class LabProgressResponse(LabProgressBase):
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 统计数据模式
class UserStats(BaseModel):
    completedCount: int
    totalPoints: int
    totalHours: int
    rank: int

class SkillRadarData(BaseModel):
    categories: List[str]
    scores: List[float]

class ProgressTrendData(BaseModel):
    dates: List[str]
    counts: List[int]

# Flag提交模式
class FlagSubmission(BaseModel):
    flag: str

class FlagResponse(BaseModel):
    correct: bool
    message: str 