#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def cleanup_challenge_files():
    # 需要删除的重复挑战相关文件列表
    files_to_delete = [
        # 后端重复的路由文件
        "backend/app/routers/challenges.py",  # 空文件，使用 backend/routers/challenge.py 代替
        "backend/routers/challenge_router.py",  # 重复的路由，使用 backend/routers/challenge.py 代替
        "backend/routers/lab.py",  # 重复的路由，已合并到 challenge.py
        "backend/init_challenges.py",  # 空文件
        
        # 前端重复的API文件
        "frontend/src/api/challenges.ts",  # 空文件，使用 challenge.ts 代替
        
        # 前端重复的路由文件
        "frontend/src/router/modules/challenges.ts",  # 空文件
        
        # 测试文件
        "backend/tests/test_challenge_start.py",  # 空文件
        
        # 重复的服务文件
        "backend/services/challenge_service.py",  # 空文件
        
        # 重复的视图组件
        "frontend/src/views/challenges",  # 整个目录，因为已经合并到 challenge 目录
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
    cleanup_challenge_files() 