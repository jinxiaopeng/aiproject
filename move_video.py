import os
import shutil

def move_video():
    # 源文件路径
    source_path = os.path.join('public', 'videos', 'chapter1.mp4')
    # 目标目录
    target_dir = os.path.join('frontend', 'public', 'videos')
    # 目标文件路径
    target_path = os.path.join(target_dir, 'chapter1.mp4')

    try:
        # 确保目标目录存在
        os.makedirs(target_dir, exist_ok=True)
        
        # 如果目标文件已存在，先删除
        if os.path.exists(target_path):
            os.remove(target_path)
            
        # 移动文件
        shutil.move(source_path, target_path)
        print(f'Successfully moved video file to {target_path}')
        
    except Exception as e:
        print(f'Error moving file: {str(e)}')

if __name__ == '__main__':
    move_video() 