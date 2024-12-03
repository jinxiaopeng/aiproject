from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import (
    AchievementType,
    UserAchievement,
    PointHistory,
    LevelRule,
    UserLevel,
    CourseProgress,
    LessonProgress
)

class RewardService:
    def __init__(self, db: Session):
        self.db = db

    def get_achievement_types(self) -> List[AchievementType]:
        """获取所有成就类型"""
        return self.db.query(AchievementType).all()

    def get_user_achievements(self, user_id: int) -> List[UserAchievement]:
        """获取用户的所有成就"""
        return self.db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id
        ).all()

    def check_achievements(self, user_id: int) -> List[UserAchievement]:
        """检查并更新用户成就"""
        achievements = []

        # 检查第一门课程完成成就
        first_course = self.db.query(AchievementType).filter(
            AchievementType.name == 'first_course'
        ).first()
        if first_course:
            completed_courses = self.db.query(CourseProgress).filter(
                CourseProgress.user_id == user_id,
                CourseProgress.status == 'completed'
            ).count()
            if completed_courses > 0:
                achievement = self._update_achievement(user_id, first_course.id, 1, True)
                if achievement:
                    achievements.append(achievement)

        # 检查课程大师成就
        course_master = self.db.query(AchievementType).filter(
            AchievementType.name == 'course_master'
        ).first()
        if course_master:
            completed_courses = self.db.query(CourseProgress).filter(
                CourseProgress.user_id == user_id,
                CourseProgress.status == 'completed'
            ).count()
            achievement = self._update_achievement(
                user_id, 
                course_master.id, 
                completed_courses,
                completed_courses >= 10
            )
            if achievement:
                achievements.append(achievement)

        # 检查快速学习者成就
        quick_learner = self.db.query(AchievementType).filter(
            AchievementType.name == 'quick_learner'
        ).first()
        if quick_learner:
            # 获取最近7天的学习记录
            consecutive_days = self._get_consecutive_learning_days(user_id)
            achievement = self._update_achievement(
                user_id,
                quick_learner.id,
                consecutive_days,
                consecutive_days >= 7
            )
            if achievement:
                achievements.append(achievement)

        # 检查知识探索者成就
        knowledge_seeker = self.db.query(AchievementType).filter(
            AchievementType.name == 'knowledge_seeker'
        ).first()
        if knowledge_seeker:
            total_learning_time = self._get_total_learning_time(user_id)
            achievement = self._update_achievement(
                user_id,
                knowledge_seeker.id,
                total_learning_time,
                total_learning_time >= 6000  # 100小时 = 6000分钟
            )
            if achievement:
                achievements.append(achievement)

        return achievements

    def _update_achievement(
        self,
        user_id: int,
        achievement_type_id: int,
        progress: int,
        completed: bool
    ) -> Optional[UserAchievement]:
        """更新用户成就进度"""
        achievement = self.db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_type_id == achievement_type_id
        ).first()

        if not achievement:
            achievement = UserAchievement(
                user_id=user_id,
                achievement_type_id=achievement_type_id,
                progress=progress,
                completed=completed,
                completed_at=datetime.now() if completed else None
            )
            self.db.add(achievement)
        else:
            if not achievement.completed:
                achievement.progress = progress
                if completed and not achievement.completed:
                    achievement.completed = True
                    achievement.completed_at = datetime.now()
                    # 添加积分奖励
                    self._add_points(
                        user_id,
                        achievement.achievement_type.points,
                        'achievement',
                        f'完成成就：{achievement.achievement_type.name}',
                        achievement.id,
                        'achievement'
                    )

        self.db.commit()
        self.db.refresh(achievement)
        return achievement if achievement.completed else None

    def _get_consecutive_learning_days(self, user_id: int) -> int:
        """获取连续学习天数"""
        # TODO: 实现连续学习天数统计
        return 0

    def _get_total_learning_time(self, user_id: int) -> int:
        """获取总学习时长（分钟）"""
        total_time = self.db.query(func.sum(LessonProgress.learning_time)).filter(
            LessonProgress.user_id == user_id
        ).scalar()
        return total_time or 0

    def _add_points(
        self,
        user_id: int,
        points: int,
        type: str,
        description: str,
        reference_id: Optional[int] = None,
        reference_type: Optional[str] = None
    ) -> None:
        """添加积分记录并更新用户等级"""
        # 添加积分历史记录
        point_history = PointHistory(
            user_id=user_id,
            points=points,
            type=type,
            description=description,
            reference_id=reference_id,
            reference_type=reference_type
        )
        self.db.add(point_history)

        # 更新用户等级
        user_level = self.db.query(UserLevel).filter(
            UserLevel.user_id == user_id
        ).first()

        if not user_level:
            # 获取第一个等级规则
            first_level = self.db.query(LevelRule).filter(
                LevelRule.level == 1
            ).first()
            next_level = self.db.query(LevelRule).filter(
                LevelRule.level == 2
            ).first()

            user_level = UserLevel(
                user_id=user_id,
                level=1,
                current_points=points,
                next_level_points=next_level.points_required if next_level else 999999
            )
            self.db.add(user_level)
        else:
            user_level.current_points += points
            # 检查是否可以升级
            while True:
                next_level = self.db.query(LevelRule).filter(
                    LevelRule.level == user_level.level + 1
                ).first()

                if not next_level or user_level.current_points < next_level.points_required:
                    break

                user_level.level += 1
                user_level.next_level_points = (
                    self.db.query(LevelRule.points_required)
                    .filter(LevelRule.level == user_level.level + 1)
                    .scalar() or 999999
                )

        self.db.commit()

    def get_user_level(self, user_id: int) -> Optional[UserLevel]:
        """获取用户等级信息"""
        return self.db.query(UserLevel).filter(
            UserLevel.user_id == user_id
        ).first()

    def get_level_rules(self) -> List[LevelRule]:
        """获取所有等级规则"""
        return self.db.query(LevelRule).order_by(LevelRule.level).all()

    def get_point_history(self, user_id: int, limit: int = 10) -> List[PointHistory]:
        """获取用户积分历史"""
        return self.db.query(PointHistory).filter(
            PointHistory.user_id == user_id
        ).order_by(PointHistory.created_at.desc()).limit(limit).all() 