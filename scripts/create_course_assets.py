# 创建新文件
import os
import shutil
from pathlib import Path

def create_course_assets():
    # 项目根目录
    root_dir = Path.cwd()
    
    # 创建缺少的目录结构
    directories = [
        'public/images/courses'  # 只需要创建images目录
    ]
    
    for directory in directories:
        dir_path = root_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f'Created directory: {dir_path}')
    
    # 创建示例视频文件 (仅创建空文件作为占位符)
    video_files = [
        'public/videos/chapter1.mp4',
        'public/videos/chapter2.mp4'
    ]
    
    for video_file in video_files:
        file_path = root_dir / video_file
        if not file_path.exists():
            file_path.touch()
            print(f'Created video placeholder: {file_path}')
    
    # 创建示例图片文件 (仅创建空文件作为占位符)
    image_files = [
        'public/images/courses/web-pentest.jpg'
    ]
    
    for image_file in image_files:
        file_path = root_dir / image_file
        if not file_path.exists():
            file_path.touch()
            print(f'Created image placeholder: {file_path}')

if __name__ == '__main__':
    create_course_assets() 