"""数据库工具测试模块"""
from datetime import datetime
from ..tests.base import TestBase
from ..data.storage import DatabaseUtils

class TestDatabaseUtils(TestBase):
    """数据库工具测试"""
    
    def setUp(self):
        """测试初始化"""
        super().setUp()
        self.db = DatabaseUtils(self.test_db_path)
        
    def test_execute_query(self):
        """测试执行查询"""
        # 插入测试数据
        self.db.execute_query("""
            INSERT INTO challenges (title, category, difficulty, points, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('测试挑战', 'test', 3, 100, datetime.now().isoformat(), datetime.now().isoformat()))
        
        # 查询数据
        results = self.db.execute_query("SELECT * FROM challenges")
        
        # 验证结果
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], '测试挑战')
        self.assertEqual(results[0]['category'], 'test')
        
    def test_execute_many(self):
        """测试批量执行"""
        # 准备测试数据
        challenges = [
            ('挑战1', 'test', 1, 100, datetime.now().isoformat(), datetime.now().isoformat()),
            ('挑战2', 'test', 2, 200, datetime.now().isoformat(), datetime.now().isoformat())
        ]
        
        # 批量插入
        self.db.execute_many("""
            INSERT INTO challenges (title, category, difficulty, points, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, challenges)
        
        # 验证结果
        results = self.db.execute_query("SELECT * FROM challenges ORDER BY title")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], '挑战1')
        self.assertEqual(results[1]['title'], '挑战2')
        
    def test_transaction(self):
        """测试事务处理"""
        try:
            # 开始事务
            self.db.begin_transaction()
            
            # 插入数据
            self.db.execute_query("""
                INSERT INTO challenges (title, category, difficulty, points, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ('事务测试', 'test', 3, 100, datetime.now().isoformat(), datetime.now().isoformat()))
            
            # 故意制造错误
            self.db.execute_query("SELECT * FROM non_existent_table")
            
            # 提交事务
            self.db.commit_transaction()
        except Exception:
            # 回滚事务
            self.db.rollback_transaction()
            
        # 验证数据未被插入
        results = self.db.execute_query("SELECT * FROM challenges WHERE title = ?", ('事务测试',))
        self.assertEqual(len(results), 0) 