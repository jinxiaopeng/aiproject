from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..core.deps import get_db, get_current_user
from ..services.feedback import FeedbackService
from ..schemas.feedback import (
    FeedbackCreate,
    FeedbackUpdate,
    FeedbackInDB,
    FeedbackCommentCreate,
    FeedbackCommentInDB,
    FeedbackVoteCreate,
    FeedbackVoteInDB,
    FeedbackDetail,
    FeedbackStats,
    FeedbackType,
    FeedbackStatus
)
from ..models.user import User

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("", response_model=FeedbackInDB)
def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建反馈"""
    service = FeedbackService(db)
    return service.create_feedback(
        user_id=current_user.id,
        entity_id=feedback.entity_id,
        feedback_type=feedback.feedback_type,
        content=feedback.content,
        rating=feedback.rating
    )

@router.get("/{feedback_id}", response_model=FeedbackDetail)
def get_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取反馈详情"""
    service = FeedbackService(db)
    feedback = service.get_feedback_detail(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

@router.get("/entity/{entity_id}", response_model=List[FeedbackInDB])
def get_entity_feedback(
    entity_id: int,
    feedback_type: Optional[FeedbackType] = None,
    status: Optional[FeedbackStatus] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取实体的反馈列表"""
    service = FeedbackService(db)
    return service.get_entity_feedback(
        entity_id=entity_id,
        feedback_type=feedback_type,
        status=status,
        skip=skip,
        limit=limit
    )

@router.put("/{feedback_id}", response_model=FeedbackInDB)
def update_feedback(
    feedback_id: int,
    feedback: FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新反馈"""
    service = FeedbackService(db)
    # 检查权限
    existing_feedback = service.get_feedback(feedback_id)
    if not existing_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if existing_feedback.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    updated_feedback = service.update_feedback(
        feedback_id=feedback_id,
        feedback_type=feedback.feedback_type,
        content=feedback.content,
        rating=feedback.rating,
        status=feedback.status,
        admin_reply=feedback.admin_reply if current_user.is_admin else None
    )
    if not updated_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return updated_feedback

@router.delete("/{feedback_id}")
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除反馈"""
    service = FeedbackService(db)
    # 检查权限
    feedback = service.get_feedback(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if feedback.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    if service.delete_feedback(feedback_id):
        return {"message": "Feedback deleted successfully"}
    raise HTTPException(status_code=404, detail="Feedback not found")

@router.post("/{feedback_id}/comments", response_model=FeedbackCommentInDB)
def add_comment(
    feedback_id: int,
    comment: FeedbackCommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """添加评论"""
    service = FeedbackService(db)
    # 检查反馈是否存在
    if not service.get_feedback(feedback_id):
        raise HTTPException(status_code=404, detail="Feedback not found")
        
    return service.add_comment(
        feedback_id=feedback_id,
        user_id=current_user.id,
        content=comment.content
    )

@router.get("/{feedback_id}/comments", response_model=List[FeedbackCommentInDB])
def get_comments(
    feedback_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取评论列表"""
    service = FeedbackService(db)
    # 检查反馈是否存在
    if not service.get_feedback(feedback_id):
        raise HTTPException(status_code=404, detail="Feedback not found")
        
    return service.get_comments(
        feedback_id=feedback_id,
        skip=skip,
        limit=limit
    )

@router.post("/{feedback_id}/vote", response_model=FeedbackVoteInDB)
def vote_feedback(
    feedback_id: int,
    vote: FeedbackVoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """投票"""
    service = FeedbackService(db)
    # 检查反馈是否存在
    if not service.get_feedback(feedback_id):
        raise HTTPException(status_code=404, detail="Feedback not found")
        
    return service.vote_feedback(
        feedback_id=feedback_id,
        user_id=current_user.id,
        is_upvote=vote.is_upvote == 1
    )

@router.get("/stats/{entity_id}", response_model=FeedbackStats)
def get_entity_feedback_stats(
    entity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取实体的反馈统计信息"""
    service = FeedbackService(db)
    return service.get_feedback_stats(entity_id) 