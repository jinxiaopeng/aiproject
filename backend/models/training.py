"""
靶场训练模型
"""

from sqlalchemy import Column, String, Integer, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, Dict

from .base import Base

class Training(Base):
    __tablename__ = 'trainings'
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    challenge_id = Column(String(36), ForeignKey('challenges.id'), nullable=False)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime)
    status = Column(Enum('in_progress', 'completed', 'failed', name='training_status'), 
                   nullable=False, default='in_progress')
    progress = Column(JSON, nullable=False, default=dict)
    score = Column(Integer, default=0)
    
    # 关联
    user = relationship("User", back_populates="trainings")
    challenge = relationship("Challenge", back_populates="trainings")
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'challenge_id': self.challenge_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'status': self.status,
            'progress': self.progress,
            'score': self.score
        }
    
    def update_progress(self, progress_data: Dict):
        """更新训练进度"""
        self.progress.update(progress_data)
        if self._check_completion():
            self.complete_training()
    
    def complete_training(self):
        """完成训练"""
        self.status = 'completed'
        self.end_time = datetime.utcnow()
    
    def fail_training(self):
        """训练失败"""
        self.status = 'failed'
        self.end_time = datetime.utcnow()
    
    def _check_completion(self) -> bool:
        """检查是否完成训练"""
        required_steps = self.challenge.training_config.get('required_steps', [])
        completed_steps = self.progress.get('completed_steps', [])
        return all(step in completed_steps for step in required_steps)

class TrainingStep(Base):
    __tablename__ = 'training_steps'
    
    id = Column(String(36), primary_key=True)
    training_id = Column(String(36), ForeignKey('trainings.id'), nullable=False)
    step_number = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    completed = Column(DateTime)
    result = Column(JSON)
    
    # 关联
    training = relationship("Training", back_populates="steps")
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'id': self.id,
            'training_id': self.training_id,
            'step_number': self.step_number,
            'name': self.name,
            'description': self.description,
            'completed': self.completed.isoformat() if self.completed else None,
            'result': self.result
        }
    
    def complete_step(self, result: Dict):
        """完成训练步骤"""
        self.completed = datetime.utcnow()
        self.result = result 