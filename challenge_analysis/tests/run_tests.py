"""运行所有测试"""
import unittest
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from challenge_analysis.data.init_db import init_db

def run_tests():
    """运行所有测试"""
    # 设置测试数据库路径
    test_db_path = os.path.join(os.path.dirname(__file__), 'test.db')
    
    # 初始化测试数据库
    init_db(test_db_path)
    
    # 发现并运行测试
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    run_tests() 