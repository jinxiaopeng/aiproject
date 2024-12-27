#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def cleanup_test_files():
    # 需要删除的测试相关文件列表
    files_to_delete = [
        # 根目录测试文件
        "test_api.py",  # 临时测试文件
        "test_docker.py",  # 临时测试文件
        "test_challenge.py",  # 空文件
        "test_auth.py",  # 空文件
        "test_sql_injection.py",  # 测试文件
        "test_monitor_system.py",  # 测试文件
        "test_monitor.py",  # 测试文件
        "test_integration.py",  # 测试文件
        "test_upload.py",  # 测试文件
        "create_test_files.py",  # 测试文件创建脚本
        "test_progress.py",  # 测试文件
        
        # 后端测试文件
        "backend/tests/test_challenge_start.py",  # 空文件
        "backend/tests/test_local_model.py",  # 未使用的测试文件
        "backend/tests/test_notification.py",  # 测试文件
        "backend/tests/test_register.py",  # 测试文件
        "backend/tests/test_monitor.py",  # 测试文件
        "backend/tests/test_alert_rules.py",  # 测试文件
        "backend/tests/test_alert_evaluator.py",  # 测试文件
        "backend/tests/test_learning_monitor.py",  # 测试文件
        "backend/tests/test_course_learning.py",  # 测试文件
        "backend/test_monitor.py",  # 测试文件
        "backend/test_upload.py",  # 测试文件
        "backend/test_progress.py",  # 测试文件
        "backend/monitor_service/tests",  # 监控服务测试目录
        "backend/monitor_service/run_tests.py",  # 监控服务测试运行脚本
        "backend/monitor_service/core/test_config.py",  # 监控服务测试配置
        
        # 前端测试文件
        "frontend/src/components/feedback/__tests__/feedback.spec.ts",  # 未使用的测试文件
        
        # 测试数据库文件
        "test.db",  # 测试数据库
        "sql_app.db",  # 测试数据库
        "learning.db",  # 测试数据库
        
        # 测试目录
        "test_files",  # 测试文件目录
        "test_challenge",  # 测试挑战目录
        "tests",  # 测试目录
        "challenge_analysis/tests",  # 挑战分析测试目录
        "challenges/web_security/test_challenge",  # Web安全测试挑战目录
        "challenges/web_security/test_challenge.py",  # Web安全测试文件
        
        # 测试数据文件
        "backend/user_progress.json",  # 测试用户进度文件
        "backend/practice_scores.json",  # 测试练习分数文件
        "backend/scripts/init_course_data.py",  # 测试课程数据初始化脚本
    ]
    
    # 获取项目根目录
    root_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # 删除文件
    for file_path in files_to_delete:
        full_path = root_dir / file_path
        if full_path.exists():
            try:
                if full_path.is_dir():
                    shutil.rmtree(full_path)
                    print(f"已删除目录: {file_path}")
                else:
                    full_path.unlink()
                    print(f"已删除文件: {file_path}")
            except Exception as e:
                print(f"删除 {file_path} 时出错: {str(e)}")
        else:
            print(f"文件不存在: {file_path}")

if __name__ == "__main__":
    cleanup_test_files() 