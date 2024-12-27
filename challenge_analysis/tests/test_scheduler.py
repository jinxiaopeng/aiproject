"""调度器测试模块"""
from datetime import datetime
from ..tests.base import TestBase
from ..core.scheduler import TaskScheduler
from ..data.storage import DatabaseUtils

class TestTaskScheduler(TestBase):
    """任务调度器测试"""
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.db = DatabaseUtils(self.test_db_path)
        self.scheduler = TaskScheduler(self.db)
        
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
        
    def test_schedule_analysis(self):
        """测试调度分析任务"""
        challenge_id = self._create_test_data()
        
        # 调度分析
        success = self.scheduler.schedule_analysis(challenge_id)
        
        # 验证结果
        self.assertTrue(success)
        tasks = self.db.execute_query(
            "SELECT * FROM analysis_tasks WHERE challenge_id = ?",
            (challenge_id,)
        )
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['status'], 'pending')
        
    def test_schedule_sync(self):
        """测试调度同步任务"""
        # 调度同步
        success = self.scheduler.schedule_sync()
        
        # 验证结果
        self.assertTrue(success)
        tasks = self.db.execute_query(
            "SELECT * FROM sync_tasks ORDER BY created_at DESC LIMIT 1"
        )
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['status'], 'pending')
        
    def test_process_tasks(self):
        """测试处理任务"""
        challenge_id = self._create_test_data()
        
        # 创建任务
        self.scheduler.schedule_analysis(challenge_id)
        
        # 处理任务
        success = self.scheduler.process_tasks()
        
        # 验证结果
        self.assertTrue(success)
        tasks = self.db.execute_query(
            "SELECT * FROM analysis_tasks WHERE challenge_id = ?",
            (challenge_id,)
        )
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['status'], 'completed') 