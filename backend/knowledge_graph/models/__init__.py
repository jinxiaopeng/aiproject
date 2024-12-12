"""Knowledge Graph Models"""

from sqlalchemy.ext.declarative import declarative_base

# 创建基类
Base = declarative_base()

from .knowledge import (
    Entity,
    AttackType,
    Vulnerability,
    LearningRecord,
    Feedback,
    EntityStatus,
    AttackStatus,
    VulnerabilityStatus,
    VulnerabilitySeverity,
    LearningStatus
)

from .user import User, UserRole, UserStatus

__all__ = [
    'Base',
    'Entity',
    'AttackType',
    'Vulnerability',
    'LearningRecord',
    'Feedback',
    'EntityStatus',
    'AttackStatus',
    'VulnerabilityStatus',
    'VulnerabilitySeverity',
    'LearningStatus',
    'User',
    'UserRole',
    'UserStatus'
] 