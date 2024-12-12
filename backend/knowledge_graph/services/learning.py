from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models.learning import LearningRecord, StudySession, TestRecord, LearningStatus
from ..models.relationships import Entity, EntityRelationship
from ..core.logger import logger

class LearningService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_learning_record(self, user_id: int, entity_id: int) -> Optional[LearningRecord]:
        """获取学习记录"""
        return self.db.query(LearningRecord).filter(
            LearningRecord.user_id == user_id,
            LearningRecord.entity_id == entity_id
        ).first()
    
    def create_learning_record(self, user_id: int, entity_id: int) -> LearningRecord:
        """创建学习记录"""
        record = LearningRecord(
            user_id=user_id,
            entity_id=entity_id
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
    
    def update_learning_progress(
        self,
        user_id: int,
        entity_id: int,
        progress: float,
        notes: Optional[str] = None
    ) -> LearningRecord:
        """更新学习进度"""
        record = self.get_learning_record(user_id, entity_id)
        if not record:
            record = self.create_learning_record(user_id, entity_id)
        
        # 更新进度
        record.progress = min(100.0, max(0.0, progress))
        record.last_study_at = datetime.utcnow()
        
        # 更新状态
        if record.progress >= 100:
            record.status = LearningStatus.COMPLETED
        elif record.progress > 0:
            record.status = LearningStatus.IN_PROGRESS
            
        if notes:
            record.notes = notes
            
        self.db.commit()
        self.db.refresh(record)
        return record
    
    def start_study_session(
        self,
        user_id: int,
        entity_id: int,
        notes: Optional[str] = None
    ) -> StudySession:
        """开始学习会话"""
        record = self.get_learning_record(user_id, entity_id)
        if not record:
            record = self.create_learning_record(user_id, entity_id)
            
        session = StudySession(
            learning_record_id=record.id,
            notes=notes
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def end_study_session(
        self,
        session_id: int,
        progress_delta: float,
        notes: Optional[str] = None
    ) -> StudySession:
        """结束学习会话"""
        session = self.db.query(StudySession).get(session_id)
        if not session:
            raise ValueError("学习会话不存在")
            
        session.end_time = datetime.utcnow()
        session.progress_delta = progress_delta
        if notes:
            session.notes = notes
            
        # 计算会话时长（分钟）
        duration = int((session.end_time - session.start_time).total_seconds() / 60)
        session.duration = duration
        
        # 更新学习记录
        record = session.learning_record
        self.update_learning_progress(
            record.user_id,
            record.entity_id,
            record.progress + progress_delta,
            notes
        )
        
        self.db.commit()
        self.db.refresh(session)
        return session
    
    def submit_test_result(
        self,
        user_id: int,
        entity_id: int,
        score: float,
        max_score: float = 100.0,
        answers: Optional[Dict[str, Any]] = None
    ) -> TestRecord:
        """提交测试结果"""
        record = self.get_learning_record(user_id, entity_id)
        if not record:
            record = self.create_learning_record(user_id, entity_id)
            
        test_record = TestRecord(
            learning_record_id=record.id,
            score=score,
            max_score=max_score,
            answers=answers
        )
        self.db.add(test_record)
        
        # 更新学习记录的得分
        record.score = score
        if score >= max_score * 0.8:  # 80%及格线
            record.status = LearningStatus.COMPLETED
            record.progress = 100.0
            
        self.db.commit()
        self.db.refresh(test_record)
        return test_record
    
    def get_learning_stats(self, user_id: int) -> Dict[str, Any]:
        """获取学习统计信息"""
        # 查询所有实体数量
        total_entities = self.db.query(Entity).count()
        
        # 查询用户的学习记录
        records = self.db.query(LearningRecord).filter(
            LearningRecord.user_id == user_id
        ).all()
        
        # 统计各状态的数量
        status_counts = {
            LearningStatus.COMPLETED: 0,
            LearningStatus.IN_PROGRESS: 0,
            LearningStatus.NOT_STARTED: 0,
            LearningStatus.REVIEWING: 0
        }
        total_progress = 0.0
        total_score = 0.0
        score_count = 0
        
        for record in records:
            status_counts[record.status] += 1
            total_progress += record.progress
            if record.score is not None:
                total_score += record.score
                score_count += 1
                
        # 计算总学习时长
        total_duration = self.db.query(func.sum(StudySession.duration)).join(
            LearningRecord
        ).filter(
            LearningRecord.user_id == user_id
        ).scalar() or 0
        
        return {
            "total_entities": total_entities,
            "completed_entities": status_counts[LearningStatus.COMPLETED],
            "in_progress_entities": status_counts[LearningStatus.IN_PROGRESS],
            "not_started_entities": total_entities - len(records),
            "average_progress": total_progress / len(records) if records else 0.0,
            "average_score": total_score / score_count if score_count > 0 else None,
            "total_study_time": total_duration
        }
    
    def get_learning_path(self, user_id: int, entity_id: int) -> Dict[str, Any]:
        """获取学习路径"""
        # 获取实体的前置知识
        prerequisites = self.db.query(EntityRelationship).filter(
            EntityRelationship.target_id == entity_id,
            EntityRelationship.relationship_type == "prerequisite"
        ).all()
        
        # 构建学习路径
        path_nodes = []
        for prereq in prerequisites:
            # 获取前置知识的学习记录
            record = self.get_learning_record(user_id, prereq.source_id)
            entity = self.db.query(Entity).get(prereq.source_id)
            
            if record:
                path_nodes.append({
                    "entity_id": entity.id,
                    "name": entity.name,
                    "status": record.status,
                    "progress": record.progress,
                    "prerequisites": []  # 可以递归获取更深层的前置知识
                })
            else:
                path_nodes.append({
                    "entity_id": entity.id,
                    "name": entity.name,
                    "status": LearningStatus.NOT_STARTED,
                    "progress": 0.0,
                    "prerequisites": []
                })
        
        # 获取推荐的下一个学习知识点
        recommended = []
        for node in path_nodes:
            if node["status"] != LearningStatus.COMPLETED:
                recommended.append(node["entity_id"])
                
        return {
            "nodes": path_nodes,
            "recommended_next": recommended
        } 