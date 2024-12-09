from sqlalchemy.orm import configure_mappers
from core.database import Base
from .user import User
from .course import Course, Chapter, CourseEnrollment, ChapterProgress, CourseNote, CourseComment

# 确保所有模型都被导入和映射
configure_mappers()

__all__ = [
    'Base',
    'User',
    'Course',
    'Chapter',
    'CourseEnrollment',
    'ChapterProgress',
    'CourseNote',
    'CourseComment'
] 