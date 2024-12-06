from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: Optional[str]
    nickname: Optional[str]
    bio: Optional[str]
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class UpdateProfileRequest(BaseModel):
    nickname: Optional[str]
    bio: Optional[str]

class ActivityResponse(BaseModel):
    id: int
    user_id: int
    type: str
    content: str
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class StatsResponse(BaseModel):
    user_id: int
    study_days: int
    completed_courses: int
    points: int
    total_study_time: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class SkillResponse(BaseModel):
    id: int
    user_id: int
    name: str
    level: int
    progress: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class ChangeEmailRequest(BaseModel):
    email: EmailStr
    code: str 