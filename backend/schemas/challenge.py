from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ChallengeCategory(str, Enum):
    WEB = "Web安全"
    CRYPTO = "密码学"
    REVERSE = "逆向工程"
    PWN = "二进制漏洞"
    MISC = "杂项"

class ChallengeDifficulty(str, Enum):
    EASY = "简单"
    MEDIUM = "中等"
    HARD = "困难"

class ChallengeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    category: ChallengeCategory
    difficulty: ChallengeDifficulty
    points: int = Field(..., ge=0)

class ChallengeCreate(ChallengeBase):
    flag: str = Field(..., min_length=1)
    docker_image: Optional[str] = None
    docker_compose: Optional[str] = None
    port_mapping: Optional[str] = None

class ChallengeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    category: Optional[ChallengeCategory] = None
    difficulty: Optional[ChallengeDifficulty] = None
    points: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class ChallengeResponse(ChallengeBase):
    id: int
    created_by: int
    created_at: datetime
    is_approved: bool
    is_active: bool
    is_solved: bool
    solved_count: int

    class Config:
        orm_mode = True

class ChallengeSubmitFlag(BaseModel):
    flag: str = Field(..., min_length=1)

class ChallengeInstanceCreate(BaseModel):
    challenge_id: int

class ChallengeInstanceResponse(BaseModel):
    id: int
    challenge_id: int
    instance_url: str
    created_at: datetime
    expires_at: datetime
    is_active: bool

    class Config:
        orm_mode = True

class ChallengeHintCreate(BaseModel):
    content: str = Field(..., min_length=1)
    cost: int = Field(0, ge=0)

class ChallengeHintResponse(BaseModel):
    id: int
    content: str
    cost: int

    class Config:
        orm_mode = True 