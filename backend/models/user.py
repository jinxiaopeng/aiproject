from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    role = Column(String(20), nullable=False, default="user")
    status = Column(String(20), nullable=False, default="active")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 课程相关的关联
    courses = relationship("Course", back_populates="instructor")
    course_enrollments = relationship("CourseEnrollment", back_populates="user")
    chapter_progress = relationship("ChapterProgress", back_populates="user")
    course_notes = relationship("CourseNote", back_populates="user")
    course_comments = relationship("CourseComment", back_populates="user")

    # 靶场训练相关的关联
    lab_instances = relationship("LabInstance", back_populates="user")
    lab_progress = relationship("LabProgress", back_populates="user")

    def __repr__(self):
        return f"<User {self.username}>"