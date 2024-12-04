from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models import Course, Chapter, Lesson, LearningProgress, User
from ..schemas import CourseCreate, CourseUpdate

class CourseService:
    def __init__(self, db: Session):
        self.db = db

    def get_courses(
        self,
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Course]:
        """获取课程列表"""
        query = self.db.query(Course)

        if category:
            query = query.filter(Course.category == category)
        if difficulty:
            query = query.filter(Course.level == difficulty)
        if search:
            query = query.filter(
                or_(
                    Course.title.ilike(f"%{search}%"),
                    Course.description.ilike(f"%{search}%")
                )
            )

        return query.all()

    def get_course_detail(self, course_id: int) -> Optional[Course]:
        """获取课程详情"""
        return self.db.query(Course).filter(Course.id == course_id).first()

    def create_course(self, course_data: CourseCreate, created_by: int) -> Course:
        """创建新课程"""
        course = Course(
            title=course_data.title,
            description=course_data.description,
            cover_image=course_data.cover_image,
            level=course_data.level,
            category=course_data.category,
            duration=course_data.duration,
            created_by=created_by,
            status=course_data.status
        )
        self.db.add(course)
        self.db.commit()
        self.db.refresh(course)
        return course

    def update_course(self, course_id: int, course_data: CourseUpdate) -> Course:
        """更新课程信息"""
        course = self.get_course_detail(course_id)
        for field, value in course_data.dict(exclude_unset=True).items():
            setattr(course, field, value)
        self.db.commit()
        self.db.refresh(course)
        return course

    def delete_course(self, course_id: int) -> None:
        """删除课程"""
        course = self.get_course_detail(course_id)
        self.db.delete(course)
        self.db.commit()

    def get_course_chapters(self, course_id: int) -> List[Chapter]:
        """获取课程章节列表"""
        return (
            self.db.query(Chapter)
            .filter(Chapter.course_id == course_id)
            .order_by(Chapter.order_num)
            .all()
        )

    def get_lesson_detail(self, course_id: int, lesson_id: int) -> Optional[Lesson]:
        """获取课时详情"""
        return (
            self.db.query(Lesson)
            .filter(
                Lesson.course_id == course_id,
                Lesson.id == lesson_id
            )
            .first()
        )

    def update_learning_progress(
        self,
        user_id: int,
        course_id: int,
        lesson_id: int,
        progress: float
    ) -> LearningProgress:
        """更新学习进度"""
        learning_progress = (
            self.db.query(LearningProgress)
            .filter(
                LearningProgress.user_id == user_id,
                LearningProgress.course_id == course_id
            )
            .first()
        )

        if not learning_progress:
            learning_progress = LearningProgress(
                user_id=user_id,
                course_id=course_id,
                last_lesson_id=lesson_id,
                progress=progress
            )
            self.db.add(learning_progress)
        else:
            learning_progress.last_lesson_id = lesson_id
            learning_progress.progress = progress

        self.db.commit()
        self.db.refresh(learning_progress)
        return learning_progress

    def get_recommended_courses(self, user_id: int) -> List[Course]:
        """获取推荐课程"""
        # 获取用户已完成的课程
        completed_courses = (
            self.db.query(LearningProgress.course_id)
            .filter(
                LearningProgress.user_id == user_id,
                LearningProgress.progress == 100
            )
            .all()
        )
        completed_course_ids = [c.course_id for c in completed_courses]

        # 获取用户的技能水平
        user = self.db.query(User).filter(User.id == user_id).first()
        user_level = "beginner"
        if user and user.profile and user.profile.skill_level:
            # 根据用户画像确定推荐难度
            skill_levels = user.profile.skill_level
            avg_level = sum(skill_levels.values()) / len(skill_levels)
            if avg_level > 7:
                user_level = "advanced"
            elif avg_level > 4:
                user_level = "intermediate"

        # 推荐同等或稍高难度的未完成课程
        recommended_courses = (
            self.db.query(Course)
            .filter(
                Course.id.notin_(completed_course_ids),
                Course.status == "published"
            )
            .order_by(Course.created_at.desc())
            .limit(10)
            .all()
        )

        return recommended_courses 