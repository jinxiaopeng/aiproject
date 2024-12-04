from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CourseBase(BaseModel):
    title: str = Field(..., description="课程标题")
    description: str = Field(..., description="课程描述")
    category: str = Field(..., description="课程分类")
    cover_image: Optional[str] = Field(None, description="课程封面图片")
    duration: int = Field(..., description="课程时长(分钟)")
    difficulty: str = Field(..., description="课程难度")
    prerequisites: List[str] = Field(default=[], description="课程前置要求")
    tags: List[str] = Field(default=[], description="课程标签")

class CourseCreate(CourseBase):
    pass

class CourseUpdate(CourseBase):
    pass

class Course(CourseBase):
    id: str = Field(..., description="课程ID")
    instructor_id: str = Field(..., description="讲师ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    status: str = Field(..., description="课程状态")
    enrolled_count: int = Field(default=0, description="报名人数")
    rating: float = Field(default=0.0, description="课程评分")
    
    class Config:
        orm_mode = True

class Chapter(BaseModel):
    id: str = Field(..., description="章节ID")
    title: str = Field(..., description="章节标题")
    description: str = Field(..., description="章节描述")
    content: str = Field(..., description="章节内容")
    order: int = Field(..., description="章节顺序")
    duration: int = Field(..., description="章节时长(分钟)")
    video_url: Optional[str] = Field(None, description="视频URL")
    attachments: List[str] = Field(default=[], description="附件列表")

class CourseProgress(BaseModel):
    course_id: str = Field(..., description="课程ID")
    user_id: str = Field(..., description="用户ID")
    progress: float = Field(..., description="学习进度")
    completed_chapters: List[str] = Field(default=[], description="已完成章节")
    last_study_time: Optional[datetime] = Field(None, description="最后学习时间")
    
    class Config:
        orm_mode = True 