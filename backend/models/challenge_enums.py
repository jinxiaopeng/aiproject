"""
靶场相关的枚举类型
"""

from enum import Enum

class ChallengeCategory(str, Enum):
    """靶场类别"""
    WEB = "web"
    PWN = "pwn"
    REVERSE = "reverse"
    CRYPTO = "crypto"
    MISC = "misc"

class ChallengeDifficulty(str, Enum):
    """靶场难度"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard" 