import requests
import json
import time
from datetime import datetime, timedelta

def test_send_progress():
    """测试发送学习进度数据"""
    url = 'http://localhost:5173/api/learning/progress'
    
    # 模拟多个章节的学习进度
    chapters = [
        {'course_id': 1, 'chapter_id': 1, 'progress': 100, 'current_time': 150, 'duration': 150},
        {'course_id': 1, 'chapter_id': 2, 'progress': 75, 'current_time': 90, 'duration': 120},
        {'course_id': 1, 'chapter_id': 3, 'progress': 50, 'current_time': 30, 'duration': 60},
        {'course_id': 1, 'chapter_id': 4, 'progress': 25, 'current_time': 15, 'duration': 60}
    ]
    
    # 模拟不同时间点的学习行为
    current_time = datetime.now()
    for i, chapter in enumerate(chapters):
        # 设置不同的时间点
        test_time = current_time - timedelta(hours=i)
        test_data = {
            'course_id': chapter['course_id'],
            'chapter_id': chapter['chapter_id'],
            'progress': chapter['progress'],
            'current_time': chapter['current_time'],
            'duration': chapter['duration'],
            'timestamp': test_time.isoformat()  # 添加时间戳
        }
        
        try:
            # 发送POST请求
            response = requests.post(url, json=test_data)
            print(f'\n发送章节 {chapter["chapter_id"]} 数据:')
            print(json.dumps(test_data, indent=2, ensure_ascii=False))
            print('响应状态:', response.status_code)
            print('响应内容:', response.json())
            
            # 暂停一下，模拟真实的学习间隔
            time.sleep(1)
            
        except Exception as e:
            print(f'发送章节 {chapter["chapter_id"]} 数据失败:', e)
    
    try:
        # 查询所有进度
        response = requests.get(url)
        print('\n查询所有学习数据:')
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except Exception as e:
        print('查询数据失败:', e)

if __name__ == '__main__':
    test_send_progress() 