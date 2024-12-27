import requests
import time
from datetime import datetime

def test_video_progress():
    """测试视频进度记录API"""
    print("\n测试视频进度记录API:")
    
    response = requests.post(
        "http://localhost:8001/learning/video/progress",
        json={
            "user_id": 1,
            "course_id": 1,
            "chapter_id": 1,
            "progress": 50,
            "duration": 600,
            "current_time": 300
        }
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")

def test_learning_behavior():
    """测试学习行为记录API"""
    print("\n测试学习行为记录API:")
    
    response = requests.post(
        "http://localhost:8001/learning/behavior",
        json={
            "user_id": 1,
            "course_id": 1,
            "behavior_type": "video_play",
            "content_id": 1,
            "duration": 300
        }
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")

def test_challenge_progress():
    """测试靶场进度记录API"""
    print("\n测试靶场进度记录API:")
    
    response = requests.post(
        "http://localhost:8001/learning/challenge/progress",
        json={
            "user_id": 1,
            "challenge_id": 1,
            "status": "completed",
            "attempts": 3,
            "hints": 1,
            "score": 100
        }
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")

def test_user_stats():
    """测试获取用户统计数据API"""
    print("\n测试获取用户统计数据API:")
    
    response = requests.get(
        "http://localhost:8001/learning/stats/1",
        params={"days": 7}
    )
    print(f"状态码: {response.status_code}")
    print(f"响应: {response.json()}")

if __name__ == "__main__":
    # 运行所有测试
    test_video_progress()
    time.sleep(1)
    test_learning_behavior()
    time.sleep(1)
    test_challenge_progress()
    time.sleep(1)
    test_user_stats() 