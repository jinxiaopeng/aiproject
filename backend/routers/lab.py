from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, text
from sqlalchemy.orm import Session
import logging

from backend.core.database import get_db
from backend.core.deps import get_current_user
from backend.models.lab import Lab, LabInstance, LabProgress
from backend.models.user import User
from backend.models.flag import Flag
from challenges import ChallengeManager

router = APIRouter(prefix="/practice", tags=["practice"])
logger = logging.getLogger(__name__)
challenge_manager = ChallengeManager()

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

@router.post("/labs/{lab_id}/start")
async def start_lab(
    lab_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """启动靶场实例"""
    try:
        # 获取靶场信息
        lab = db.query(Lab).filter(Lab.id == lab_id).first()
        if not lab:
            raise HTTPException(status_code=404, detail=f"靶场不存在: {lab_id}")

        # 检查是否已有正在运行的实例
        existing_instance = db.query(LabInstance).filter(
            LabInstance.lab_id == lab_id,
            LabInstance.user_id == current_user.id,
            LabInstance.end_time.is_(None)
        ).first()
        
        if existing_instance:
            # 返回已存在的实例信息
            try:
                status = challenge_manager.get_challenge_status(lab_id)
                if status['status'] == 'running':
                    return {
                        "status": "running",
                        "instance_id": existing_instance.id,
                        "url": status['url']
                    }
                else:
                    # 如果进程已经停止，更新实例状态
                    existing_instance.end_time = datetime.now()
                    db.commit()
            except Exception as e:
                logger.error(f"获取靶场状态失败: {str(e)}")
                # 如果获取状态失败，也更新实例状态
                existing_instance.end_time = datetime.now()
                db.commit()

        # 启动靶场
        try:
            result = challenge_manager.start_challenge(lab_id)
        except Exception as e:
            logger.error(f"启动靶场失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"启动靶场失败: {str(e)}")
        
        # 创建新实例
        instance = LabInstance(
            lab_id=lab_id,
            user_id=current_user.id,
            start_time=datetime.now(),
            status='running',
            instance_url=result['url']
        )
        db.add(instance)
        db.commit()
        
        return {
            "status": "started",
            "instance_id": instance.id,
            "url": result['url']
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"启动靶场失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"启动靶场失败: {str(e)}")

@router.post("/labs/{lab_id}/stop")
async def stop_lab(
    lab_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """停止靶场实例"""
    try:
        # 查找正在运行的实例
        instance = db.query(LabInstance).filter(
            LabInstance.lab_id == lab_id,
            LabInstance.user_id == current_user.id,
            LabInstance.end_time.is_(None)
        ).first()
        
        if not instance:
            raise HTTPException(status_code=404, detail="没有找到运行中的实例")

        # 停止靶场
        result = challenge_manager.stop_challenge(lab_id)
        
        # 更新实例状态
        instance.end_time = datetime.now()
        db.commit()
        
        return {
            "status": "stopped",
            "instance_id": instance.id
        }
    except Exception as e:
        logger.error(f"停止靶场失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"停止靶场失败: {str(e)}")

@router.post("/labs/{lab_id}/verify")
async def verify_flag(
    lab_id: str,
    flag: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """验证flag并更新进度"""
    try:
        # 获取靶场信息
        lab = db.query(Lab).filter(Lab.id == lab_id).first()
        if not lab:
            raise HTTPException(status_code=404, detail="靶场不存在")

        # 验证flag
        if flag == lab.flag_hash:  # 修改为flag_hash
            # 更新进度
            progress = db.query(LabProgress).filter(
                LabProgress.lab_id == lab_id,
                LabProgress.user_id == current_user.id
            ).first()
            
            if not progress:
                progress = LabProgress(
                    lab_id=lab_id,
                    user_id=current_user.id,
                    score=lab.points,
                    status='completed',
                    completed_at=datetime.now()
                )
                db.add(progress)
            elif progress.status != 'completed':
                progress.status = 'completed'
                progress.score = lab.points
                progress.completed_at = datetime.now()
            
            db.commit()
            
            return {
                "success": True,
                "message": "恭喜！完成挑战",
                "points": lab.points
            }
        else:
            return {
                "success": False,
                "message": "Flag不正确，请继续尝试"
            }
    except Exception as e:
        logger.error(f"验证flag失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"验证flag失败: {str(e)}")