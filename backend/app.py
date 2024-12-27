from flask import Flask, jsonify, request
from flask_cors import CORS
from learning.models import db, VideoProgress, LearningBehavior
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# 配置SQLite数据库
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'learning.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/api/learning/progress', methods=['POST'])
def update_progress():
    """更新学习进度"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)  # 临时使用固定用户ID
        course_id = data['course_id']
        chapter_id = data['chapter_id']
        progress = data['progress']
        current_time = data['current_time']
        duration = data['duration']
        
        # 更新视频进度
        video_progress = VideoProgress.query.filter_by(
            user_id=user_id,
            course_id=course_id,
            chapter_id=chapter_id
        ).first()
        
        if not video_progress:
            video_progress = VideoProgress(
                user_id=user_id,
                course_id=course_id,
                chapter_id=chapter_id
            )
            db.session.add(video_progress)
        
        video_progress.progress = progress
        video_progress.current_time = current_time
        video_progress.duration = duration
        
        # 更新学习行为
        learning_behavior = LearningBehavior.query.filter_by(
            user_id=user_id,
            course_id=course_id,
            end_time=None
        ).first()
        
        if not learning_behavior:
            learning_behavior = LearningBehavior(
                user_id=user_id,
                course_id=course_id,
                start_time=datetime.now()
            )
            db.session.add(learning_behavior)
        
        # 更新学习时长
        current_time = datetime.now()
        if learning_behavior.start_time:
            duration = (current_time - learning_behavior.start_time).seconds
            learning_behavior.duration = duration
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '进度已更新'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/learning/progress', methods=['GET'])
def get_progress():
    """获取学习进度"""
    try:
        user_id = request.args.get('user_id', 1)  # 临时使用固定用户ID
        
        # 获取视频进度
        video_progress = VideoProgress.query.filter_by(user_id=user_id).all()
        video_data = {f"{p.course_id}-{p.chapter_id}": p.progress for p in video_progress}
        
        # 获取学习行为
        learning_behavior = LearningBehavior.query.filter_by(user_id=user_id).all()
        behavior_data = {b.course_id: b.to_dict() for b in learning_behavior}
        
        return jsonify({
            'videoProgress': video_data,
            'learningProgress': behavior_data
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(port=5173, debug=True) 