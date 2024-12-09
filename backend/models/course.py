from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    cover_url = Column(String(255))
    category = Column(String(50), nullable=False)
    difficulty = Column(String(20), nullable=False)
    instructor_id = Column(Integer, ForeignKey('users.id'))
    student_count = Column(Integer, default=0)  # 学习人数
    rating = Column(Float, default=0)  # 平均评分
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    instructor = relationship("User", back_populates="courses")
    chapters = relationship("Chapter", back_populates="course", cascade="all, delete-orphan", order_by="Chapter.order")
    notes = relationship("CourseNote", back_populates="course", cascade="all, delete-orphan")
    comments = relationship("CourseComment", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("CourseEnrollment", back_populates="course", cascade="all, delete-orphan")

class Chapter(Base):
    __tablename__ = 'chapters'

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    title = Column(String(100), nullable=False)
    description = Column(Text)
    video_url = Column(String(255))
    duration = Column(Integer)  # 单位：分钟
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    course = relationship("Course", back_populates="chapters")
    progress_records = relationship("ChapterProgress", back_populates="chapter", cascade="all, delete-orphan")
    notes = relationship("CourseNote", back_populates="chapter", cascade="all, delete-orphan")

class CourseEnrollment(Base):
    __tablename__ = 'course_enrollments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    progress = Column(Float, default=0)  # 0-100
    completed = Column(Boolean, default=False)
    last_accessed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="course_enrollments")
    course = relationship("Course", back_populates="enrollments")

class ChapterProgress(Base):
    __tablename__ = 'chapter_progress'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    chapter_id = Column(Integer, ForeignKey('chapters.id'))
    progress = Column(Float, default=0)  # 0-100
    completed = Column(Boolean, default=False)
    last_position = Column(Float, default=0)  # 视频播放位置（秒）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="chapter_progress")
    chapter = relationship("Chapter", back_populates="progress_records")

class CourseNote(Base):
    __tablename__ = 'course_notes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    chapter_id = Column(Integer, ForeignKey('chapters.id'))
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="course_notes")
    course = relationship("Course", back_populates="notes")
    chapter = relationship("Chapter", back_populates="notes")

class CourseComment(Base):
    __tablename__ = 'course_comments'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    content = Column(Text, nullable=False)
    rating = Column(Float)  # 1-5
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="course_comments")
    course = relationship("Course", back_populates="comments") 