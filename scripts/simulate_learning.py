import json
import time
from datetime import datetime

def simulate_learning():
    """模拟学习过程"""
    # 初始化数据
    course_id = 1
    video_progress = {}
    learning_progress = {}
    
    # 模拟3个章节的学习
    chapters = [
        {"id": 1, "duration": 300},  # 5分钟
        {"id": 2, "duration": 600},  # 10分钟
        {"id": 3, "duration": 450}   # 7.5分钟
    ]
    
    total_study_time = 0
    
    try:
        for chapter in chapters:
            print(f"\n开始学习章节 {chapter['id']}...")
            current_time = 0
            
            while current_time < chapter["duration"]:
                # 每次增加30秒
                current_time += 30
                if current_time > chapter["duration"]:
                    current_time = chapter["duration"]
                
                # 计算进度
                progress = int((current_time / chapter["duration"]) * 100)
                
                # 更新视频进度
                video_progress[f"{course_id}-{chapter['id']}"] = progress
                
                # 更新学习行为数据
                if course_id not in learning_progress:
                    learning_progress[course_id] = {
                        "totalTime": 0,
                        "lastAccess": datetime.now().isoformat(),
                        "chapters": {}
                    }
                
                learning_progress[course_id]["totalTime"] += 30
                learning_progress[course_id]["chapters"][str(chapter['id'])] = {
                    "progress": progress,
                    "lastAccess": datetime.now().isoformat()
                }
                
                total_study_time += 30
                print(f"章节{chapter['id']}进度: {progress}% ({current_time}/{chapter['duration']}秒)")
                
                # 保存数据到localStorage
                try:
                    with open('video_progress.json', 'w') as f:
                        json.dump(video_progress, f, indent=2)
                    with open('learning_progress.json', 'w') as f:
                        json.dump(learning_progress, f, indent=2)
                except Exception as e:
                    print(f"保存数据失败: {e}")
                
                time.sleep(0.5)  # 模拟学习间隔
        
        # 打印学习统计
        print("\n学习统计:")
        print(f"总学习时长: {total_study_time/60:.1f}分钟")
        print(f"完成章节数: {len(chapters)}")
        print(f"平均完成度: 100%")
        
        print("\n详细数据:")
        print("视频进度:", json.dumps(video_progress, indent=2))
        print("学习行为:", json.dumps(learning_progress, indent=2))
        
    except KeyboardInterrupt:
        print("\n模拟被中断")
        # 保存最终数据
        with open('video_progress.json', 'w') as f:
            json.dump(video_progress, f, indent=2)
        with open('learning_progress.json', 'w') as f:
            json.dump(learning_progress, f, indent=2)
        print("已保存当前进度")

if __name__ == '__main__':
    simulate_learning() 