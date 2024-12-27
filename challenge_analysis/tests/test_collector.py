"""数据收集器测试模块"""
from datetime import datetime
from ..tests.base import TestBase
from ..data.collector import DataCollector
from ..data.storage import DatabaseUtils

class TestDataCollector(TestBase):
    """数据收集器测试"""
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.db = DatabaseUtils(self.test_db_path)
        self.collector = DataCollector(self.db)
        
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
        return challenge_id
        
    def test_record_challenge_attempt(self):
        """测试记录挑战尝试"""
        challenge_id = self._create_test_data()
        
        # 记录尝试
        attempt_data = {
            'user_id': 1,
            'challenge_id': challenge_id,
            'status': 'completed',
            'start_time': datetime.now().isoformat(),
            'completion_time': datetime.now().isoformat(),
            'attempts': 2
        }
        success = self.collector.record_challenge_attempt(attempt_data)
        
        # 验证结果
        self.assertTrue(success)
        attempts = self.db.execute_query(
            "SELECT * FROM user_challenges WHERE user_id = ? AND challenge_id = ?",
            (1, challenge_id)
        )
        self.assertEqual(len(attempts), 1)
        self.assertEqual(attempts[0]['status'], 'completed')
        
    def test_collect_user_feedback(self):
        """测试收集用户反馈"""
        challenge_id = self._create_test_data()
        
        # 收集反馈
        feedback_data = {
            'user_id': 1,
            'challenge_id': challenge_id,
            'difficulty_rating': 4,
            'clarity_rating': 5,
            'comments': '这是一个很好的挑战'
        }
        success = self.collector.collect_user_feedback(feedback_data)
        
        # 验证结果
        self.assertTrue(success)
        feedback = self.db.execute_query(
            "SELECT * FROM challenge_feedback WHERE user_id = ? AND challenge_id = ?",
            (1, challenge_id)
        )
        self.assertEqual(len(feedback), 1)
        self.assertEqual(feedback[0]['difficulty_rating'], 4)
        
    def test_sync_challenge_data(self):
        """测试同步挑战数据"""
        # 同步数据
        success = self.collector.sync_challenge_data()
        
        # 验证结果
        self.assertTrue(success)
        sync_log = self.db.execute_query(
            "SELECT * FROM challenges_sync_log ORDER BY sync_time DESC LIMIT 1"
        )
        self.assertEqual(len(sync_log), 1)
        self.assertEqual(sync_log[0]['status'], 'success')
        
    def test_sync_user_progress(self):
        """测试同步用户进度"""
        # 同步进度
        success = self.collector.sync_user_progress()
        
        # 验证结果
        self.assertTrue(success)
        sync_log = self.db.execute_query(
            "SELECT * FROM user_progress_sync_log ORDER BY sync_time DESC LIMIT 1"
        )
        self.assertEqual(len(sync_log), 1)
        self.assertEqual(sync_log[0]['status'], 'success') 