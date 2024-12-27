"""分析器测试模块"""
from datetime import datetime
from ..tests.base import TestBase
from ..core.analyzer import ChallengeAnalyzer
from ..data.storage import DatabaseUtils

class TestChallengeAnalyzer(TestBase):
    """挑战分析器测试"""
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.db = DatabaseUtils(self.test_db_path)
        self.analyzer = ChallengeAnalyzer(self.db)
        
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
        
    def test_analyze_challenge_difficulty(self):
        """测试分析挑战难度"""
        challenge_id = self._create_test_data()
        
        # 分析难度
        difficulty_score = self.analyzer.analyze_challenge_difficulty(challenge_id)
        
        # 验证结果
        self.assertIsNotNone(difficulty_score)
        self.assertTrue(0 <= difficulty_score <= 5)
        
    def test_analyze_user_performance(self):
        """测试分析用户表现"""
        challenge_id = self._create_test_data()
        
        # 分析用户表现
        performance = self.analyzer.analyze_user_performance(1)
        
        # 验证结果
        self.assertIsNotNone(performance)
        self.assertIn('completed_count', performance)
        self.assertIn('avg_attempts', performance)
        self.assertEqual(performance['completed_count'], 1)
        
    def test_generate_challenge_report(self):
        """测试生成挑战报告"""
        challenge_id = self._create_test_data()
        
        # 生成报告
        report = self.analyzer.generate_challenge_report(challenge_id)
        
        # 验证结果
        self.assertIsNotNone(report)
        self.assertIn('difficulty_score', report)
        self.assertIn('completion_rate', report)
        self.assertIn('avg_attempts', report)
        self.assertIn('feedback_summary', report) 