from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CourseBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    cover_url: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=50)
    difficulty: str = Field(..., min_length=1, max_length=20)
    instructor_id: int

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[str] = None

class ChapterBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    video_url: Optional[str] = None
    duration: Optional[int] = Field(None, ge=0)  # 单位：分钟
    order: int = Field(..., ge=0)

class ChapterCreate(ChapterBase):
    course_id: int

class ChapterUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    video_url: Optional[str] = None
    duration: Optional[int] = None
    order: Optional[int] = None

class ChapterProgressUpdate(BaseModel):
    progress: float = Field(..., ge=0, le=100)
    last_position: float = Field(..., ge=0)
    completed: bool = False

class VideoInfo(BaseModel):
    video_url: str
    duration: int
    title: str

class UserBase(BaseModel):
    id: int
    username: str
    avatar: Optional[str] = None

    class Config:
        orm_mode = True

class ChapterResponse(ChapterBase):
    id: int
    course_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    progress: Optional[float] = None
    completed: Optional[bool] = None
    last_position: Optional[float] = None

    class Config:
        orm_mode = True

class CourseNoteBase(BaseModel):
    content: str = Field(..., min_length=1)
    chapter_id: Optional[int] = None

class CourseNoteCreate(CourseNoteBase):
    pass

class CourseNoteUpdate(BaseModel):
    content: str = Field(..., min_length=1)

class CourseCommentBase(BaseModel):
    content: str = Field(..., min_length=1)
    rating: Optional[float] = Field(None, ge=1, le=5)

class CourseCommentCreate(CourseCommentBase):
    pass

class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    chapters: List[ChapterResponse]
    progress: Optional[float] = None
    student_count: int = 0
    rating: float = 0

    class Config:
        orm_mode = True

class CourseNoteResponse(CourseNoteBase):
    id: int
    user_id: int
    course_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: UserBase

    class Config:
        orm_mode = True

class CourseCommentResponse(CourseCommentBase):
    id: int
    user_id: int
    course_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: UserBase

    class Config:
        orm_mode = True

class PaginatedCourseResponse(BaseModel):
    items: List[CourseResponse]
    total: int
    page: int
    limit: int

    class Config:
        orm_mode = True 