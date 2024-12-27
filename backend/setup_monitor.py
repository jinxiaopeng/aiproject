import os
import shutil
from pathlib import Path

def setup_monitor_service():
    """
    设置监控系统的目录结构并移动文件到正确的位置
    """
    # 获取backend目录的绝对路径
    backend_dir = Path(os.path.dirname(os.path.abspath(__file__)))
    
    # 创建monitor_service目录结构
    monitor_dirs = [
        'monitor_service',
        'monitor_service/config',
        'monitor_service/data',
        'monitor_service/logs',
        'monitor_service/tests',
        'monitor_service/utils'
    ]
    
    for dir_path in monitor_dirs:
        full_path = backend_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {full_path}")
    
    # 定义需要移动的文件
    files_to_move = {
        # 源文件 : 目标位置
        'init_db.py': 'monitor_service/init_db.py',
        'database.py': 'monitor_service/database.py',
        'README.md': 'monitor_service/README.md'
    }
    
    # 移动文件
    for src, dst in files_to_move.items():
        src_path = backend_dir / src
        dst_path = backend_dir / dst
        
        if dst_path.exists():
            print(f"文件已存在: {dst_path}")
            continue
            
        try:
            if src_path.exists():
                shutil.copy2(src_path, dst_path)
                print(f"移动文件: {src_path} -> {dst_path}")
                # 移动成功后删除源文件
                os.remove(src_path)
                print(f"删除源文件: {src_path}")
            else:
                print(f"源文件不存在: {src_path}")
        except Exception as e:
            print(f"移动文件时出错 {src}: {str(e)}")
    
    # 创建空的__init__.py文件
    init_files = [
        'monitor_service/__init__.py',
        'monitor_service/config/__init__.py',
        'monitor_service/tests/__init__.py',
        'monitor_service/utils/__init__.py'
    ]
    
    for init_file in init_files:
        init_path = backend_dir / init_file
        if not init_path.exists():
            init_path.touch()
            print(f"创建文件: {init_path}")
    
    print("\n监控系统目录设置完成!")
    print("\n目录结构:")
    print("monitor_service/")
    print("├── config/")
    print("├── data/")
    print("├── logs/")
    print("├── tests/")
    print("├── utils/")
    print("├── __init__.py")
    print("├── database.py")
    print("├── init_db.py")
    print("└── README.md")

if __name__ == '__main__':
    setup_monitor_service() 