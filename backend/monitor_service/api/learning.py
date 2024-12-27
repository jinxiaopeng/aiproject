from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from ..database import MonitorDB

router = APIRouter(prefix="/learning", tags=["learning"])
db = MonitorDB()

class VideoProgress(BaseModel):
    user_id: int
    course_id: int
    chapter_id: int
    progress: int
    duration: int
    current_time: int

class LearningBehavior(BaseModel):
    user_id: int
    course_id: int
    behavior_type: str
    content_id: int
    duration: Optional[int] = None

class ChallengeProgress(BaseModel):
    user_id: int
    challenge_id: int
    status: str
    attempts: Optional[int] = None
    hints: Optional[int] = None
    score: Optional[int] = None

@router.post("/video/progress")
async def update_video_progress(progress: VideoProgress):
    """更新视频播放进度"""
    try:
        db.record_video_progress(
            user_id=progress.user_id,
            course_id=progress.course_id,
            chapter_id=progress.chapter_id,
            progress=progress.progress,
            duration=progress.duration,
            current_time=progress.current_time
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/behavior")
async def record_learning_behavior(behavior: LearningBehavior):
    """记录学习行为"""
    try:
        db.record_learning_behavior(
            user_id=behavior.user_id,
            course_id=behavior.course_id,
            behavior_type=behavior.behavior_type,
            content_id=behavior.content_id,
            duration=behavior.duration
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/challenge/progress")
async def update_challenge_progress(progress: ChallengeProgress):
    """更新靶场训练进度"""
    try:
        db.update_challenge_progress(
            user_id=progress.user_id,
            challenge_id=progress.challenge_id,
            status=progress.status,
            attempts=progress.attempts,
            hints=progress.hints,
            score=progress.score
        )
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/{user_id}")
async def get_user_stats(user_id: int, days: int = 7):
    """获取用户学习统计数据"""
    try:
        stats = db.get_user_stats(user_id, days)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 