import os
import requests
from pathlib import Path

def create_directory(path):
    """创建目录（如果不存在）"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"创建目录: {path}")

def download_image(url, save_path):
    """下载图片"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"下载失败 {url}: {str(e)}")
        return False

def download_course_images():
    # 基础路径
    target_base = Path("frontend/public/images")
    
    # 创建必要的目录
    create_directory(target_base / "courses")
    create_directory(target_base / "avatars")
    
    # 课程封面图片 URL（使用更专业的网络安全相关图片）
    course_images = {
        'web-security-basic.jpg': 'https://img.freepik.com/free-vector/cyber-security-concept_23-2148532223.jpg',
        'xss-defense.jpg': 'https://img.freepik.com/free-vector/cyber-attack-concept-illustration_114360-1528.jpg',
        'sql-injection.jpg': 'https://img.freepik.com/free-vector/database-protection-concept-illustration_114360-5926.jpg',
        'system-security.jpg': 'https://img.freepik.com/free-vector/operating-system-abstract-concept-illustration_335657-3875.jpg',
        'network-protocol.jpg': 'https://img.freepik.com/free-vector/network-security-concept-illustration_114360-5625.jpg',
        'cryptography.jpg': 'https://img.freepik.com/free-vector/cryptography-abstract-concept-illustration_335657-3895.jpg',
        'secure-dev.jpg': 'https://img.freepik.com/free-vector/programming-concept-illustration_114360-1351.jpg',
        'mobile-security.jpg': 'https://img.freepik.com/free-vector/mobile-security-concept-illustration_114360-7143.jpg',
        'blockchain.jpg': 'https://img.freepik.com/free-vector/blockchain-technology-concept-illustration_114360-5247.jpg',
        'cloud-security.jpg': 'https://img.freepik.com/free-vector/cloud-computing-security-abstract-concept-illustration_335657-3903.jpg'
    }
    
    # 讲师头像（使用专业人士头像）
    teacher_images = {
        'teacher1.jpg': 'https://img.freepik.com/free-photo/confident-business-man-portrait_144627-1.jpg',
        'teacher2.jpg': 'https://img.freepik.com/free-photo/young-businesswoman-portrait_144627-5.jpg',
        'teacher3.jpg': 'https://img.freepik.com/free-photo/business-man-portrait_144627-3.jpg',
        'teacher4.jpg': 'https://img.freepik.com/free-photo/businesswoman-portrait_144627-7.jpg',
        'teacher5.jpg': 'https://img.freepik.com/free-photo/business-man-portrait_144627-9.jpg',
        'teacher6.jpg': 'https://img.freepik.com/free-photo/young-businessman-portrait_144627-11.jpg',
        'teacher7.jpg': 'https://img.freepik.com/free-photo/businesswoman-portrait_144627-13.jpg',
        'teacher8.jpg': 'https://img.freepik.com/free-photo/business-man-portrait_144627-15.jpg',
        'teacher9.jpg': 'https://img.freepik.com/free-photo/young-businesswoman-portrait_144627-17.jpg',
        'teacher10.jpg': 'https://img.freepik.com/free-photo/business-man-portrait_144627-19.jpg'
    }
    
    print("\n开始下载课程封面图片...")
    for filename, url in course_images.items():
        save_path = target_base / "courses" / filename
        if download_image(url, save_path):
            print(f"已下载课程封面: {filename}")
    
    print("\n开始下载讲师头像...")
    for filename, url in teacher_images.items():
        save_path = target_base / "avatars" / filename
        if download_image(url, save_path):
            print(f"已下载讲师头像: {filename}")

if __name__ == "__main__":
    download_course_images() 