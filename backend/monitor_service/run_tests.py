import pytest
import sys
from pathlib import Path

def run_tests():
    """运行所有测试"""
    # 获取测试目录路径
    test_dir = Path(__file__).parent / "tests"
    
    # 运行测试
    args = [
        str(test_dir),
        "-v",  # 详细输出
        "--tb=short",  # 简短的错误回溯
        "-s",  # 显示print输出
        "--cov=.",  # 代码覆盖率报告
        "--cov-report=term-missing",  # 显示未覆盖的代码行
    ]
    
    # 运行测试并获取结果
    result = pytest.main(args)
    
    # 根据测试结果设置退出码
    sys.exit(result)

if __name__ == "__main__":
    run_tests() 