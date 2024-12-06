from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ChallengeCategory(str, Enum):
    WEB = "WEB"
    CRYPTO = "CRYPTO"
    REVERSE = "REVERSE"
    PWN = "PWN"
    MISC = "MISC"

class ChallengeDifficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"

class ChallengeBase(BaseModel):
    title: str
    description: str
    category: ChallengeCategory
    difficulty: ChallengeDifficulty
    points: int
    docker_image: Optional[str] = None
    port_mapping: Optional[str] = None

class ChallengeCreate(ChallengeBase):
    flag: str

class ChallengeResponse(ChallengeBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    solved_count: Optional[int] = None
    is_solved: Optional[bool] = None

    class Config:
        from_attributes = True

class ChallengeSubmitFlag(BaseModel):
    flag: str

class ChallengeInstanceResponse(BaseModel):
    id: int
    challenge_id: int
    instance_url: str
    created_at: datetime
    expires_at: datetime
    is_active: bool

    class Config:
        from_attributes = True 