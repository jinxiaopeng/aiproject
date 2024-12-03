class CourseProgressBase(BaseModel):
    total_lessons: int
    completed_lessons: int = 0
    total_duration: int
    learning_time: int = 0
    progress: float = 0
    status: str = "not_started"

class CourseProgressCreate(CourseProgressBase):
    user_id: int
    course_id: int

class CourseProgressUpdate(BaseModel):
    completed_lessons: Optional[int]
    learning_time: Optional[int]
    last_lesson_id: Optional[int]
    progress: Optional[float]
    status: Optional[str]

class CourseProgressResponse(CourseProgressBase):
    id: int
    user_id: int
    course_id: int
    last_lesson_id: Optional[int]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LessonProgressBase(BaseModel):
    progress: float = 0
    learning_time: int = 0
    last_position: int = 0
    status: str = "not_started"

class LessonProgressCreate(LessonProgressBase):
    user_id: int
    lesson_id: int
    course_id: int

class LessonProgressUpdate(BaseModel):
    progress: Optional[float]
    learning_time: Optional[int]
    last_position: Optional[int]
    status: Optional[str]

class LessonProgressResponse(LessonProgressBase):
    id: int
    user_id: int
    lesson_id: int
    course_id: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class LearningRecordCreate(BaseModel):
    action: str
    position: Optional[int]
    duration: int = 0

class AchievementTypeBase(BaseModel):
    name: str
    description: Optional[str]
    icon: Optional[str]
    points: int = 0

class AchievementTypeCreate(AchievementTypeBase):
    pass

class AchievementTypeResponse(AchievementTypeBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserAchievementBase(BaseModel):
    user_id: int
    achievement_type_id: int
    progress: int = 0
    completed: bool = False

class UserAchievementCreate(UserAchievementBase):
    pass

class UserAchievementUpdate(BaseModel):
    progress: Optional[int]
    completed: Optional[bool]

class UserAchievementResponse(UserAchievementBase):
    id: int
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    achievement_type: AchievementTypeResponse

    class Config:
        orm_mode = True

class PointHistoryBase(BaseModel):
    user_id: int
    points: int
    type: str
    description: Optional[str]
    reference_id: Optional[int]
    reference_type: Optional[str]

class PointHistoryCreate(PointHistoryBase):
    pass

class PointHistoryResponse(PointHistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class LevelRuleBase(BaseModel):
    level: int
    points_required: int
    title: str
    icon: Optional[str]
    rewards: Optional[dict]

class LevelRuleCreate(LevelRuleBase):
    pass

class LevelRuleResponse(LevelRuleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserLevelBase(BaseModel):
    user_id: int
    level: int = 1
    current_points: int = 0
    next_level_points: int

class UserLevelCreate(UserLevelBase):
    pass

class UserLevelUpdate(BaseModel):
    level: Optional[int]
    current_points: Optional[int]
    next_level_points: Optional[int]

class UserLevelResponse(UserLevelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 