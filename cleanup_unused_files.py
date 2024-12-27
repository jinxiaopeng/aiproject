#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def cleanup_files():
    # 需要删除的文件列表
    files_to_delete = [
        # 测试相关的临时文件
        "test.db",
        "test_docker.py",
        "test_challenge.py",  # 空文件
        "test_auth.py",  # 空文件
        "sql_app.db",
        "learning.db",
        
        # 重复的路由文件
        "frontend/src/router/routes.ts",  # 未使用
        "frontend/src/router/index.tsx",  # 未使用，使用 index.ts
        
        # 重复的挑战/练习相关文件
        "frontend/src/views/practice",  # 整个目录，因为已经合并到 challenge
        "frontend/src/router/modules/practice.ts",  # 已合并到 challenge
        "frontend/src/router/modules/challenges.ts",  # 空文件
        
        # 临时文件
        "query",  # 临时文件
        "tatus",  # 临时文件
        "et --hard 111acbd",  # 临时文件
        
        # 重复的 README 文件
        "readme-optimized-zh.md",  # 空文件
        
        # 下载的安装文件
        "DockerDesktop.exe",  # 安装文件
        "wsl_update_x64.msi",  # 安装文件
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
    cleanup_files() 