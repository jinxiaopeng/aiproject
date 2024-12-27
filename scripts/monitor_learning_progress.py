import json
import time
from datetime import datetime
import os
import browser_cookie3  # 需要安装: pip install browser-cookie3
import requests

def monitor_learning_progress():
    """监控课程学习进度"""
    print("开始监控课程学习进度...")
    
    try:
        # 获取浏览器cookies
        cookies = browser_cookie3.chrome()  # 或者使用 browser_cookie3.firefox()
        
        # 构建请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        while True:
            try:
                # 发送请求获取localStorage数据
                response = requests.get('http://localhost:5173/api/learning/progress', cookies=cookies, headers=headers)
                data = response.json()
                
                if 'videoProgress' in data and 'learningProgress' in data:
                    video_progress = data['videoProgress']
                    learning_progress = data['learningProgress']
                    
                    print("\n检测到学习数据:")
                    print("-" * 50)
                    
                    # 分析视频进度
                    if video_progress:
                        print("\n视频观看进度:")
                        for key, progress in video_progress.items():
                            course_id, chapter_id = key.split('-')
                            print(f"课程{course_id} 章节{chapter_id}: {progress}%")
                    
                    # 分析学习行为
                    if learning_progress:
                        print("\n学习行为数据:")
                        for course_id, data in learning_progress.items():
                            total_time = data.get('totalTime', 0)
                            last_access = data.get('lastAccess', '')
                            print(f"\n课程{course_id}:")
                            print(f"总学习时长: {total_time/60:.1f}分钟")
                            print(f"最后访问时间: {last_access}")
                            
                            # 显示章节进度
                            chapters = data.get('chapters', {})
                            for chapter_id, chapter_data in chapters.items():
                                progress = chapter_data.get('progress', 0)
                                print(f"章节{chapter_id} 进度: {progress}%")
                    
                    print("\n" + "-" * 50)
                else:
                    print("未检测到学习数据")
                    
            except requests.exceptions.RequestException as e:
                print(f"请求失败: {e}")
            except json.JSONDecodeError as e:
                print(f"数据解析失败: {e}")
            except Exception as e:
                print(f"发生错误: {e}")
            
            # 每5秒检查一次
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n停止监控")
    except Exception as e:
        print(f"程序异常: {e}")

if __name__ == '__main__':
    monitor_learning_progress() 