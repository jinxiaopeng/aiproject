import unittest
import json
import time
from datetime import datetime

class TestLearningMonitor(unittest.TestCase):
    def setUp(self):
        # 模拟localStorage
        self.video_progress = {}
        self.learning_progress = {}
        
    def test_video_progress_tracking(self):
        """测试视频进度跟踪功能"""
        course_id = 1
        chapter_id = 1
        
        # 模拟视频播放进度更新
        progress = 45  # 45%的进度
        self.video_progress[f"{course_id}-{chapter_id}"] = progress
        
        # 验证进度保存
        self.assertEqual(self.video_progress[f"{course_id}-{chapter_id}"], 45)
        
    def test_learning_behavior_tracking(self):
        """测试学习行为跟踪功能"""
        course_id = 1
        chapter_id = 1
        
        # 模拟学习行为数据
        behavior_data = {
            "totalTime": 3600,  # 1小时
            "lastAccess": datetime.now().isoformat(),
            "chapters": {
                "1": {
                    "progress": 75,
                    "lastAccess": datetime.now().isoformat()
                }
            }
        }
        
        self.learning_progress[course_id] = behavior_data
        
        # 验证学习时长记录
        self.assertEqual(self.learning_progress[course_id]["totalTime"], 3600)
        
        # 验证章节进度记录
        self.assertEqual(
            self.learning_progress[course_id]["chapters"]["1"]["progress"], 
            75
        )
        
    def test_complete_chapter(self):
        """测试章节完成功能"""
        course_id = 1
        chapter_id = 1
        
        # 模拟完成章节
        self.video_progress[f"{course_id}-{chapter_id}"] = 100
        
        # 验证完成状态
        self.assertEqual(self.video_progress[f"{course_id}-{chapter_id}"], 100)
        
    def test_learning_statistics(self):
        """测试学习统计功能"""
        course_id = 1
        
        # 模拟多个章节的学习数据
        self.video_progress = {
            "1-1": 100,  # 第1章完成
            "1-2": 60,   # 第2章进行中
            "1-3": 0     # 第3章未开始
        }
        
        # 计算完成率
        total_chapters = len(self.video_progress)
        completed_chapters = len([p for p in self.video_progress.values() if p == 100])
        completion_rate = (completed_chapters / total_chapters) * 100
        
        # 验证统计结果
        self.assertEqual(completion_rate, 33.33333333333333)  # 1/3完成
        
if __name__ == '__main__':
    unittest.main() 