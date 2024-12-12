from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from core.database import get_db
from models.lab import Lab, LabInstance, LabProgress
from core.deps import get_current_user
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/labs", response_model=List[dict])
async def get_labs(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取靶场列表"""
    try:
        query = db.query(Lab).filter(Lab.is_active == True)
        
        if category:
            query = query.filter(Lab.category == category)
        if difficulty:
            query = query.filter(Lab.difficulty == difficulty)
            
        labs = query.all()
        
        # 转换为字典列表
        result = []
        for lab in labs:
            # 获取完成人数
            solved_count = db.query(LabProgress).filter(
                LabProgress.lab_id == lab.id,
                LabProgress.status == 'completed'
            ).count()
            
            # 计算完成率
            total_attempts = db.query(LabProgress).filter(
                LabProgress.lab_id == lab.id
            ).count()
            completion_rate = (solved_count / total_attempts * 100) if total_attempts > 0 else 0
            
            result.append({
                "id": lab.id,
                "title": lab.title,
                "description": lab.description,
                "category": lab.category,
                "difficulty": lab.difficulty,
                "points": lab.points,
                "status": "active",
                "completionRate": round(completion_rate, 2),
                "solvedCount": solved_count
            })
        
        return result
    except Exception as e:
        logger.error(f"获取靶场列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取靶场列表失败")

@router.get("/stats")
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """获取用户训练统计"""
    try:
        # 获取完成的靶场数量
        completed_count = db.query(LabProgress).filter(
            LabProgress.user_id == current_user.id,
            LabProgress.status == 'completed'
        ).count()
        
        # 获取总积分
        total_points = db.query(func.sum(LabProgress.score)).filter(
            LabProgress.user_id == current_user.id
        ).scalar() or 0
        
        # 获取总训练时长
        total_hours = db.query(func.sum(
            func.timestampdiff(
                text('HOUR'),
                LabInstance.start_time,
                LabInstance.end_time
            )
        )).filter(
            LabInstance.user_id == current_user.id,
            LabInstance.end_time.isnot(None)
        ).scalar() or 0
        
        # 获取排名
        rank_subquery = db.query(
            LabProgress.user_id,
            func.sum(LabProgress.score).label('total_score')
        ).group_by(
            LabProgress.user_id
        ).having(
            func.sum(LabProgress.score) > total_points
        ).subquery()
        
        rank = db.query(rank_subquery).count() + 1
        
        return {
            "completedCount": completed_count,
            "totalPoints": total_points,
            "totalHours": total_hours,
            "rank": rank
        }
    except Exception as e:
        logger.error(f"获取用户统计失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取用户统计失败") 