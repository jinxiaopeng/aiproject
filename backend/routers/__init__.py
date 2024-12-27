# This file is intentionally empty to make the directory a Python package

from .auth import router as auth_router
from .lab import router as lab_router
from .user import router as user_router
from .knowledge import router as knowledge_router

__all__ = ["auth_router", "lab_router", "user_router", "knowledge_router"]
