"""存储管理测试模块"""
from datetime import datetime
from ..tests.base import TestBase
from ..data.storage import DatabaseUtils

class TestDatabaseUtils(TestBase):
    """数据库工具测试"""
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.db = DatabaseUtils(self.test_db_path)
        
    def _create_test_data(self):
        """创建测试数据"""
        # 创建挑战
        challenge_data = {
            'title': '测试挑战',
            'description': '这是一个测试挑战',
            'category': 'test',
            'difficulty': 3,
            'points': 100,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        challenge_id = self.db.insert('challenges', challenge_data)
        
        # 创建用户挑战记录
        user_challenge_data = {
            'user_id': 1,
            'challenge_id': challenge_id,
            'status': 'completed',
            'start_time': datetime.now().isoformat(),
            'completion_time': datetime.now().isoformat(),
            'attempts': 2,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        self.db.insert('user_challenges', user_challenge_data)
        
        # 创建挑战反馈
        feedback_data = {
            'user_id': 1,
            'challenge_id': challenge_id,
            'difficulty_rating': 4,
            'clarity_rating': 5,
            'comments': '这是一个很好的挑战',
            'created_at': datetime.now().isoformat()
        }
        self.db.insert('challenge_feedback', feedback_data)
        
        return challenge_id
        
    def test_get_challenge_stats(self):
        """测试获取挑战统计"""
        challenge_id = self._create_test_data()
        
        # 获取统计
        stats = self.db.get_challenge_stats(challenge_id)
        
        # 验证结果
        self.assertIsNotNone(stats)
        self.assertIn('avg_difficulty_rating', stats)
        self.assertIn('avg_clarity_rating', stats)
        self.assertEqual(stats['avg_difficulty_rating'], 4)
        self.assertEqual(stats['avg_clarity_rating'], 5)
        
    def test_get_user_progress(self):
        """测试获取用户进度"""
        challenge_id = self._create_test_data()
        
        # 获取进度
        progress = self.db.get_user_progress(1)
        
        # 验证结果
        self.assertIsNotNone(progress)
        self.assertIn('completed_count', progress)
        self.assertIn('avg_attempts', progress)
        self.assertEqual(progress['completed_count'], 1)
        self.assertEqual(progress['avg_attempts'], 2)
        
    def test_get_challenge_feedback(self):
        """测试获取挑战反馈"""
        challenge_id = self._create_test_data()
        
        # 获取反馈
        feedback = self.db.get_challenge_feedback(challenge_id)
        
        # 验证结果
        self.assertIsNotNone(feedback)
        self.assertEqual(len(feedback), 1)
        self.assertEqual(feedback[0]['difficulty_rating'], 4)
        self.assertEqual(feedback[0]['clarity_rating'], 5)
        self.assertEqual(feedback[0]['comments'], '这是一个很好的挑战') 