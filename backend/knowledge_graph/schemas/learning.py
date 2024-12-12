from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum

class LearningStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REVIEWING = "reviewing"

# 学习记录模型
class LearningRecordBase(BaseModel):
    entity_id: int = Field(..., description="知识点ID")
    status: LearningStatus = Field(default=LearningStatus.NOT_STARTED, description="学习状态")
    progress: float = Field(default=0.0, ge=0.0, le=100.0, description="学习进度")
    notes: Optional[str] = Field(None, description="学习笔记")

class LearningRecordCreate(LearningRecordBase):
    pass

class LearningRecordUpdate(BaseModel):
    status: Optional[LearningStatus] = None
    progress: Optional[float] = Field(None, ge=0.0, le=100.0)
    notes: Optional[str] = None
    score: Optional[float] = Field(None, ge=0.0)

class LearningRecordInDB(LearningRecordBase):
    id: int
    user_id: int
    score: Optional[float] = None
    last_study_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 学习会话模型
class StudySessionBase(BaseModel):
    learning_record_id: int = Field(..., description="学习记录ID")
    start_time: datetime = Field(default_factory=datetime.utcnow)
    progress_delta: float = Field(default=0.0, ge=0.0, description="进度增量")
    notes: Optional[str] = Field(None, description="学习笔记")

class StudySessionCreate(StudySessionBase):
    pass

class StudySessionUpdate(BaseModel):
    end_time: datetime
    duration: int = Field(..., ge=0, description="学习时长（分钟）")
    progress_delta: float = Field(..., ge=0.0, description="进度增量")
    notes: Optional[str] = None

class StudySessionInDB(StudySessionBase):
    id: int
    end_time: Optional[datetime] = None
    duration: Optional[int] = None

    class Config:
        from_attributes = True

# 测试记录模型
class TestRecordBase(BaseModel):
    learning_record_id: int = Field(..., description="学习记录ID")
    score: float = Field(..., ge=0.0, description="测试得分")
    max_score: float = Field(default=100.0, ge=0.0, description="满分值")
    answers: Optional[Dict[str, Any]] = Field(None, description="答题记录")

class TestRecordCreate(TestRecordBase):
    pass

class TestRecordInDB(TestRecordBase):
    id: int
    test_time: datetime

    class Config:
        from_attributes = True

# 学习进度统计模型
class LearningStats(BaseModel):
    total_entities: int = Field(..., description="总知识点数")
    completed_entities: int = Field(..., description="已完成知识点数")
    in_progress_entities: int = Field(..., description="学习中知识点数")
    not_started_entities: int = Field(..., description="未开始知识点数")
    average_progress: float = Field(..., description="平均学习进度")
    average_score: Optional[float] = Field(None, description="平均测试得分")
    total_study_time: int = Field(..., description="总学习时长（分钟）")

# 学习路径模型
class LearningPathNode(BaseModel):
    entity_id: int
    name: str
    status: LearningStatus
    progress: float
    prerequisites: List[int] = []  # 前置知识点ID列表

class LearningPath(BaseModel):
    nodes: List[LearningPathNode]
    recommended_next: List[int] = Field(..., description="推荐的下一个学习知识点ID列表") 