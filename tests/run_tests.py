import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入测试模块
from test_course_learning import TestCourseLearning

if __name__ == '__main__':
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCourseLearning)
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite) 