from typing import Optional, List
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum

class FeedbackType(str, Enum):
    CONTENT = "content"
    DIFFICULTY = "difficulty"
    SUGGESTION = "suggestion"
    BUG = "bug"
    OTHER = "other"

class FeedbackStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    RESOLVED = "resolved"
    REJECTED = "rejected"

# 反馈模型
class FeedbackBase(BaseModel):
    entity_id: int = Field(..., description="知识点ID")
    feedback_type: FeedbackType = Field(..., description="反馈类型")
    content: str = Field(..., min_length=1, max_length=1000, description="反馈内容")
    rating: Optional[int] = Field(None, ge=1, le=5, description="评分(1-5)")

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackUpdate(BaseModel):
    feedback_type: Optional[FeedbackType] = None
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    rating: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[FeedbackStatus] = None
    admin_reply: Optional[str] = Field(None, min_length=1, max_length=1000)

class FeedbackInDB(FeedbackBase):
    id: int
    user_id: int
    status: FeedbackStatus
    admin_reply: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 反馈评论模型
class FeedbackCommentBase(BaseModel):
    feedback_id: int = Field(..., description="反馈ID")
    content: str = Field(..., min_length=1, max_length=500, description="评论内容")

class FeedbackCommentCreate(FeedbackCommentBase):
    pass

class FeedbackCommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)

class FeedbackCommentInDB(FeedbackCommentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# 反馈投票模型
class FeedbackVoteBase(BaseModel):
    feedback_id: int = Field(..., description="反馈ID")
    is_upvote: int = Field(..., ge=-1, le=1, description="投票类型(1: 赞同, -1: 反对)")

class FeedbackVoteCreate(FeedbackVoteBase):
    pass

class FeedbackVoteInDB(FeedbackVoteBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# 反馈详情模型（包含评论和投票）
class FeedbackDetail(FeedbackInDB):
    comments: List[FeedbackCommentInDB] = []
    votes: List[FeedbackVoteInDB] = []
    upvotes: int = Field(0, description="赞同数")
    downvotes: int = Field(0, description="反对数")

# 反馈统计模型
class FeedbackStats(BaseModel):
    total_feedback: int = Field(..., description="总反馈数")
    pending_feedback: int = Field(..., description="待处理反馈数")
    resolved_feedback: int = Field(..., description="已解决反馈数")
    average_rating: Optional[float] = Field(None, description="平均评分")
    feedback_by_type: dict = Field(..., description="各类型反馈数量")
    feedback_by_status: dict = Field(..., description="各状态反馈数量") 