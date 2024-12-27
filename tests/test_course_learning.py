import unittest
import json
import time
from datetime import datetime

class TestCourseLearning(unittest.TestCase):
    def setUp(self):
        # 初始化测试数据
        self.course_id = 1
        self.chapter_id = 1
        self.video_duration = 600  # 10分钟的视频
        
        # 清除localStorage模拟数据
        self.video_progress = {}
        self.learning_progress = {}
    
    def test_video_watching(self):
        """测试视频观看过程"""
        print("\n开始测试视频观看过程...")
        
        # 模拟观看视频
        current_time = 0
        while current_time < self.video_duration:
            # 每次增加30秒
            current_time += 30
            if current_time > self.video_duration:
                current_time = self.video_duration
            
            # 计算进度百分比
            progress = int((current_time / self.video_duration) * 100)
            
            # 更新视频进度
            self.video_progress[f"{self.course_id}-{self.chapter_id}"] = progress
            
            # 更新学习行为数据
            if self.course_id not in self.learning_progress:
                self.learning_progress[self.course_id] = {
                    "totalTime": 0,
                    "lastAccess": datetime.now().isoformat(),
                    "chapters": {}
                }
            
            self.learning_progress[self.course_id]["totalTime"] += 30
            self.learning_progress[self.course_id]["chapters"][str(self.chapter_id)] = {
                "progress": progress,
                "lastAccess": datetime.now().isoformat()
            }
            
            print(f"当前进度: {progress}% ({current_time}/{self.video_duration}秒)")
            time.sleep(1)  # 模拟实际观看时间
        
        # 验证最终进度
        self.assertEqual(
            self.video_progress[f"{self.course_id}-{self.chapter_id}"],
            100,
            "视频应该完成100%"
        )
        
        # 验证学习时长
        chapter_data = self.learning_progress[self.course_id]["chapters"][str(self.chapter_id)]
        self.assertEqual(
            chapter_data["progress"],
            100,
            "章节进度应该是100%"
        )
        
        print("\n测试数据:")
        print("视频进度:", json.dumps(self.video_progress, indent=2))
        print("学习行为:", json.dumps(self.learning_progress, indent=2))
    
    def test_multiple_chapters(self):
        """测试多章节学习"""
        print("\n开始测试多章节学习...")
        
        chapters = [
            {"id": 1, "duration": 300},  # 5分钟
            {"id": 2, "duration": 600},  # 10分钟
            {"id": 3, "duration": 450}   # 7.5分钟
        ]
        
        total_study_time = 0
        
        for chapter in chapters:
            print(f"\n开始学习章节 {chapter['id']}...")
            current_time = 0
            
            while current_time < chapter["duration"]:
                current_time += 30
                if current_time > chapter["duration"]:
                    current_time = chapter["duration"]
                
                progress = int((current_time / chapter["duration"]) * 100)
                self.video_progress[f"{self.course_id}-{chapter['id']}"] = progress
                
                if self.course_id not in self.learning_progress:
                    self.learning_progress[self.course_id] = {
                        "totalTime": 0,
                        "lastAccess": datetime.now().isoformat(),
                        "chapters": {}
                    }
                
                self.learning_progress[self.course_id]["totalTime"] += 30
                self.learning_progress[self.course_id]["chapters"][str(chapter['id'])] = {
                    "progress": progress,
                    "lastAccess": datetime.now().isoformat()
                }
                
                total_study_time += 30
                print(f"章节{chapter['id']}进度: {progress}% ({current_time}/{chapter['duration']}秒)")
                time.sleep(0.5)  # 加快模拟速度
        
        # 验证所有章节是否完成
        for chapter in chapters:
            self.assertEqual(
                self.video_progress[f"{self.course_id}-{chapter['id']}"],
                100,
                f"章节{chapter['id']}应该完成100%"
            )
        
        print("\n学习统计:")
        print(f"总学习时长: {total_study_time/60:.1f}分钟")
        print(f"完成章节数: {len(chapters)}")
        print(f"平均完成度: 100%")
        
        print("\n详细数据:")
        print("视频进度:", json.dumps(self.video_progress, indent=2))
        print("学习行为:", json.dumps(self.learning_progress, indent=2))

if __name__ == '__main__':
    unittest.main() 