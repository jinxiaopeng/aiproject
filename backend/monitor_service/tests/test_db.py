import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from monitor_service.database import MonitorDB

def test_database_operations():
    """测试数据库基本操作"""
    db = MonitorDB()
    
    # 测试记录视频进度
    print("\n测试记录视频进度:")
    db.record_video_progress(
        user_id=1,
        course_id=1,
        chapter_id=1,
        progress=75,
        duration=600,
        current_time=450
    )
    print("✓ 视频进度记录成功")
    
    # 测试记录学习行为
    print("\n测试记录学习行为:")
    db.record_learning_behavior(
        user_id=1,
        course_id=1,
        behavior_type='video_watch',
        content_id=1,
        duration=300
    )
    print("✓ 学习行为记录成功")
    
    # 测试更新靶场进度
    print("\n测试更新靶场进度:")
    db.update_challenge_progress(
        user_id=1,
        challenge_id=1,
        status='completed',
        attempts=3,
        hints=1,
        score=100
    )
    print("✓ 靶场进度更新成功")
    
    # 测试更新每日统计
    print("\n测试更新每日统计:")
    db.update_daily_stats(
        user_id=1,
        study_time=1800,
        video_complete=1,
        challenge_complete=1,
        score=100
    )
    print("✓ 每日统计更新成功")
    
    # 测试获取用户统计数据
    print("\n测试获取用户统计数据:")
    stats = db.get_user_stats(user_id=1, days=7)
    print("用户统计数据:")
    print(f"- 每日统计: {len(stats['daily_stats'])} 条记录")
    print(f"- 视频完成率: {stats['video_stats']['completion_rate']}%")
    print(f"- 靶场完成率: {stats['challenge_stats']['completion_rate']}%")
    print(f"- 总得分: {stats['challenge_stats']['total_score']}")
    
    print("\n所有测试完成!")

if __name__ == '__main__':
    test_database_operations() 