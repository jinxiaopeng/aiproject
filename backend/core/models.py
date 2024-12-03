from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联
    user = relationship("User", back_populates="notes")
    lesson = relationship("Lesson", back_populates="notes")
    histories = relationship("NoteHistory", back_populates="note", cascade="all, delete-orphan")

class NoteHistory(Base):
    __tablename__ = "note_histories"

    id = Column(Integer, primary_key=True, index=True)
    note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联
    note = relationship("Note", back_populates="histories")

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    title = Column(Text, nullable=False)
    type = Column(String(20), nullable=False)
    options = Column(JSON, nullable=False)
    correct_answer = Column(JSON, nullable=False)
    explanation = Column(Text)
    score = Column(Integer, nullable=False, default=10)
    order_num = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联
    lesson = relationship("Lesson", back_populates="questions")
    attempt_details = relationship("QuizAttemptDetail", back_populates="question")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    answers = Column(JSON, nullable=False)
    score = Column(Integer, nullable=False)
    passed = Column(Boolean, nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联
    user = relationship("User", back_populates="quiz_attempts")
    lesson = relationship("Lesson", back_populates="quiz_attempts")
    details = relationship("QuizAttemptDetail", back_populates="attempt", cascade="all, delete-orphan")

class QuizAttemptDetail(Base):
    __tablename__ = "quiz_attempt_details"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("quiz_questions.id"), nullable=False)
    user_answer = Column(JSON, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联
    attempt = relationship("QuizAttempt", back_populates="details")
    question = relationship("QuizQuestion", back_populates="attempt_details")

class CourseProgress(Base):
    __tablename__ = "course_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    total_lessons = Column(Integer, nullable=False)
    completed_lessons = Column(Integer, nullable=False, default=0)
    total_duration = Column(Integer, nullable=False)
    learning_time = Column(Integer, nullable=False, default=0)
    last_lesson_id = Column(Integer, ForeignKey("lessons.id"))
    progress = Column(Float, nullable=False, default=0)
    status = Column(String(20), nullable=False, default='not_started')
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联
    user = relationship("User", back_populates="course_progress")
    course = relationship("Course", back_populates="progress")
    last_lesson = relationship("Lesson")
    lesson_progress = relationship("LessonProgress", back_populates="course_progress")

class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    progress = Column(Float, nullable=False, default=0)
    learning_time = Column(Integer, nullable=False, default=0)
    last_position = Column(Integer, default=0)
    status = Column(String(20), nullable=False, default='not_started')
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联
    user = relationship("User", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="progress")
    course = relationship("Course")
    course_progress = relationship("CourseProgress", back_populates="lesson_progress")
    learning_records = relationship("LearningRecord", back_populates="lesson_progress")

class LearningRecord(Base):
    __tablename__ = "learning_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    action = Column(String(20), nullable=False)
    position = Column(Integer)
    duration = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联
    user = relationship("User", back_populates="learning_records")
    course = relationship("Course")
    lesson = relationship("Lesson")
    lesson_progress = relationship("LessonProgress", back_populates="learning_records")

class AchievementType(Base):
    __tablename__ = "achievement_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    icon = Column(String(100))
    points = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联
    user_achievements = relationship("UserAchievement", back_populates="achievement_type")

class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_type_id = Column(Integer, ForeignKey("achievement_types.id"), nullable=False)
    progress = Column(Integer, nullable=False, default=0)
    completed = Column(Boolean, nullable=False, default=False)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联
    user = relationship("User", back_populates="achievements")
    achievement_type = relationship("AchievementType", back_populates="user_achievements")

class PointHistory(Base):
    __tablename__ = "point_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(Text)
    reference_id = Column(Integer)
    reference_type = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关联
    user = relationship("User", back_populates="point_history")

class LevelRule(Base):
    __tablename__ = "level_rules"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, nullable=False, unique=True)
    points_required = Column(Integer, nullable=False)
    title = Column(String(50), nullable=False)
    icon = Column(String(100))
    rewards = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserLevel(Base):
    __tablename__ = "user_levels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    level = Column(Integer, nullable=False, default=1)
    current_points = Column(Integer, nullable=False, default=0)
    next_level_points = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 关联
    user = relationship("User", back_populates="level") 