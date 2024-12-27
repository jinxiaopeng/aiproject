from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class VideoProgress(db.Model):
    __tablename__ = 'video_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    chapter_id = db.Column(db.Integer, nullable=False)
    progress = db.Column(db.Integer, default=0)  # 进度百分比
    duration = db.Column(db.Integer, default=0)  # 视频总时长(秒)
    current_time = db.Column(db.Integer, default=0)  # 当前播放时间(秒)
    last_updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            'course_id': self.course_id,
            'chapter_id': self.chapter_id,
            'progress': self.progress,
            'duration': self.duration,
            'current_time': self.current_time,
            'last_updated': self.last_updated.isoformat()
        }

class LearningBehavior(db.Model):
    __tablename__ = 'learning_behavior'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer, default=0)  # 学习时长(秒)
    
    def to_dict(self):
        return {
            'course_id': self.course_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration
        } 