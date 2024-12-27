import os
import shutil
from pathlib import Path

def create_directory(path):
    """创建目录（如果不存在）"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"创建目录: {path}")

def find_and_move_images():
    # 基础路径
    base_path = Path(".")
    target_base = Path("frontend/public/images")
    
    # 创建必要的目录
    create_directory(target_base / "courses")
    create_directory(target_base / "avatars")
    
    # 要搜索的图片类型
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    # 要排除的目录
    exclude_dirs = {'.git', 'node_modules', 'venv', '__pycache__', 'cache', '.pytest_cache'}
    
    # 用于存储找到的图片
    found_images = []
    
    # 遍历所有文件
    for root, dirs, files in os.walk(base_path):
        # 排除不需要的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                file_path = Path(root) / file
                
                # 根据文件名判断图片类型
                if any(keyword in file.lower() for keyword in ['course', 'web', 'security', 'sql', 'xss', 'crypto']):
                    target_dir = target_base / "courses"
                    category = "课程封面"
                elif any(keyword in file.lower() for keyword in ['avatar', 'teacher', 'instructor']):
                    target_dir = target_base / "avatars"
                    category = "讲师头像"
                else:
                    continue
                
                # 记录找到的图片
                found_images.append({
                    'source': file_path,
                    'target': target_dir / file,
                    'category': category
                })
    
    # 打印找到的图片
    if found_images:
        print("\n找到以下相关图片：")
        for img in found_images:
            print(f"\n类型: {img['category']}")
            print(f"源文件: {img['source']}")
            print(f"目标位置: {img['target']}")
        
        # 询问是否移动文件
        response = input("\n是否将这些文件移动到对应目录？(y/n): ")
        if response.lower() == 'y':
            for img in found_images:
                try:
                    shutil.copy2(img['source'], img['target'])
                    print(f"已复制: {img['source']} -> {img['target']}")
                except Exception as e:
                    print(f"复制失败 {img['source']}: {str(e)}")
    else:
        print("未找到相关图片文件")

if __name__ == "__main__":
    find_and_move_images() 