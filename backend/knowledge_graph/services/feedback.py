from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.feedback import (
    Feedback,
    FeedbackComment,
    FeedbackVote,
    FeedbackType,
    FeedbackStatus
)
from ..core.logger import logger

class FeedbackService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_feedback(
        self,
        user_id: int,
        entity_id: int,
        feedback_type: FeedbackType,
        content: str,
        rating: Optional[int] = None
    ) -> Feedback:
        """创建反馈"""
        feedback = Feedback(
            user_id=user_id,
            entity_id=entity_id,
            feedback_type=feedback_type,
            content=content,
            rating=rating
        )
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback
    
    def get_feedback(self, feedback_id: int) -> Optional[Feedback]:
        """获取反馈详情"""
        return self.db.query(Feedback).filter(Feedback.id == feedback_id).first()
    
    def get_entity_feedback(
        self,
        entity_id: int,
        feedback_type: Optional[FeedbackType] = None,
        status: Optional[FeedbackStatus] = None,
        skip: int = 0,
        limit: int = 10
    ) -> List[Feedback]:
        """获取实体的反馈列表"""
        query = self.db.query(Feedback).filter(Feedback.entity_id == entity_id)
        
        if feedback_type:
            query = query.filter(Feedback.feedback_type == feedback_type)
        if status:
            query = query.filter(Feedback.status == status)
            
        return query.order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
    
    def update_feedback(
        self,
        feedback_id: int,
        feedback_type: Optional[FeedbackType] = None,
        content: Optional[str] = None,
        rating: Optional[int] = None,
        status: Optional[FeedbackStatus] = None,
        admin_reply: Optional[str] = None
    ) -> Optional[Feedback]:
        """更新反馈"""
        feedback = self.get_feedback(feedback_id)
        if not feedback:
            return None
            
        if feedback_type:
            feedback.feedback_type = feedback_type
        if content:
            feedback.content = content
        if rating is not None:
            feedback.rating = rating
        if status:
            feedback.status = status
        if admin_reply:
            feedback.admin_reply = admin_reply
            
        self.db.commit()
        self.db.refresh(feedback)
        return feedback
    
    def delete_feedback(self, feedback_id: int) -> bool:
        """删除反馈"""
        feedback = self.get_feedback(feedback_id)
        if not feedback:
            return False
            
        self.db.delete(feedback)
        self.db.commit()
        return True
    
    def add_comment(
        self,
        feedback_id: int,
        user_id: int,
        content: str
    ) -> FeedbackComment:
        """添加评论"""
        comment = FeedbackComment(
            feedback_id=feedback_id,
            user_id=user_id,
            content=content
        )
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment
    
    def get_comments(
        self,
        feedback_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[FeedbackComment]:
        """获取评论列表"""
        return self.db.query(FeedbackComment).filter(
            FeedbackComment.feedback_id == feedback_id
        ).order_by(
            FeedbackComment.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def vote_feedback(
        self,
        feedback_id: int,
        user_id: int,
        is_upvote: bool
    ) -> FeedbackVote:
        """投票"""
        # 检查是否已投票
        vote = self.db.query(FeedbackVote).filter(
            FeedbackVote.feedback_id == feedback_id,
            FeedbackVote.user_id == user_id
        ).first()
        
        if vote:
            # 更新投票
            vote.is_upvote = 1 if is_upvote else -1
        else:
            # 创建新投票
            vote = FeedbackVote(
                feedback_id=feedback_id,
                user_id=user_id,
                is_upvote=1 if is_upvote else -1
            )
            self.db.add(vote)
            
        self.db.commit()
        self.db.refresh(vote)
        return vote
    
    def get_feedback_stats(self, entity_id: Optional[int] = None) -> Dict[str, Any]:
        """获取反馈统计信息"""
        query = self.db.query(Feedback)
        if entity_id:
            query = query.filter(Feedback.entity_id == entity_id)
            
        # 总反馈数
        total_feedback = query.count()
        
        # 各状态反馈数
        feedback_by_status = dict(
            query.with_entities(
                Feedback.status,
                func.count(Feedback.id)
            ).group_by(Feedback.status).all()
        )
        
        # 各类型反馈数
        feedback_by_type = dict(
            query.with_entities(
                Feedback.feedback_type,
                func.count(Feedback.id)
            ).group_by(Feedback.feedback_type).all()
        )
        
        # 平均评分
        average_rating = query.with_entities(
            func.avg(Feedback.rating)
        ).filter(Feedback.rating.isnot(None)).scalar()
        
        return {
            "total_feedback": total_feedback,
            "pending_feedback": feedback_by_status.get(FeedbackStatus.PENDING, 0),
            "resolved_feedback": feedback_by_status.get(FeedbackStatus.RESOLVED, 0),
            "average_rating": float(average_rating) if average_rating else None,
            "feedback_by_type": feedback_by_type,
            "feedback_by_status": feedback_by_status
        }
    
    def get_feedback_detail(self, feedback_id: int) -> Optional[Dict[str, Any]]:
        """获取反馈详情（包含评论和投票）"""
        feedback = self.get_feedback(feedback_id)
        if not feedback:
            return None
            
        # 获取评论
        comments = self.get_comments(feedback_id)
        
        # 获取投票统计
        votes = self.db.query(FeedbackVote).filter(
            FeedbackVote.feedback_id == feedback_id
        ).all()
        
        upvotes = sum(1 for vote in votes if vote.is_upvote == 1)
        downvotes = sum(1 for vote in votes if vote.is_upvote == -1)
        
        return {
            "feedback": feedback,
            "comments": comments,
            "votes": votes,
            "upvotes": upvotes,
            "downvotes": downvotes
        } 