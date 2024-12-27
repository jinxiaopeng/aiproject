"""
靶场数据模型模板
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Flag(db.Model):
    """Flag模型"""
    id = db.Column(db.Integer, primary_key=True)
    flag_key = db.Column(db.String(50), unique=True, nullable=False)
    flag_value = db.Column(db.String(100), nullable=False)
    hint = db.Column(db.Text)

def init_db():
    """初始化数据库"""
    db.create_all()
    
    # 检查是否需要插入初始数据
    if User.query.count() == 0:
        # 插入示例用户
        admin = User(
            username='admin',
            password='admin123',
            email='admin@test.com'
        )
        db.session.add(admin)
        
        # 插入示例flag
        flag = Flag(
            flag_key='test_flag',
            flag_value='flag{test_flag}',
            hint='这是一个测试flag'
        )
        db.session.add(flag)
        
        db.session.commit() 