import os
import sys
import shutil
from pathlib import Path

def setup_project():
    """设置项目目录结构"""
    try:
        # 获取项目根目录
        project_root = Path(__file__).parent

        # 创建必要的目录
        directories = [
            'collector',
            'analyzer',
            'config',
            'data',
            'logs',
            'tools',
            'tests'
        ]

        # 创建目录
        for directory in directories:
            dir_path = project_root / directory
            dir_path.mkdir(exist_ok=True)
            # 在每个目录中创建 __init__.py 文件
            init_file = dir_path / '__init__.py'
            init_file.touch()

        print("项目目录结构已创建完成！")
        
        # 显示目录结构
        print("\n目录结构：")
        for path in sorted(project_root.rglob('*')):
            depth = len(path.relative_to(project_root).parts)
            if path.is_file():
                print('    ' * (depth - 1) + '├── ' + path.name)
            else:
                print('    ' * (depth - 1) + '└── ' + path.name + '/')

    except Exception as e:
        print(f"设置项目目录时出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    setup_project() 