import sqlite3
import os
from datetime import datetime
from pathlib import Path

def view_database_content():
    """查看数据库中的所有表内容"""
    # 获取数据库路径
    db_path = Path(__file__).parent.parent / 'data' / 'monitor.db'
    
    if not db_path.exists():
        print(f"数据库文件不存在: {db_path}")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 获取所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\n=== {table_name} 表内容 ===")
            
            # 获取表结构
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print("\n列名:", end=" ")
            for col in columns:
                print(f"{col[1]}({col[2]})", end=" | ")
            print("\n" + "-" * 80)
            
            # 获取表数据
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if not rows:
                print("(空表)")
                continue
                
            # 打印数据
            for row in rows:
                print(row)
            
            # 打印表统计
            print(f"\n总记录数: {len(rows)}")
            
            # 针对特定表的统计
            if table_name == 'video_progress':
                cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN progress = 100 THEN 1 ELSE 0 END) as completed,
                    AVG(progress) as avg_progress
                FROM video_progress
                ''')
                stats = cursor.fetchone()
                print(f"完成视频数: {stats[1]}/{stats[0]}")
                print(f"平均进度: {stats[2]:.1f}%")
                
            elif table_name == 'challenge_progress':
                cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                    AVG(score) as avg_score,
                    AVG(attempts) as avg_attempts
                FROM challenge_progress
                ''')
                stats = cursor.fetchone()
                print(f"完成靶场数: {stats[1]}/{stats[0]}")
                print(f"平均分数: {stats[2]:.1f}")
                print(f"平均尝试次数: {stats[3]:.1f}")
                
            elif table_name == 'daily_stats':
                cursor.execute('''
                SELECT 
                    SUM(total_study_time) as total_time,
                    SUM(video_completion_count) as total_videos,
                    SUM(challenge_completion_count) as total_challenges,
                    SUM(score_gained) as total_score
                FROM daily_stats
                ''')
                stats = cursor.fetchone()
                print(f"总学习时长: {stats[0]/3600:.1f}小时")
                print(f"总完成视频: {stats[1]}个")
                print(f"总完成靶场: {stats[2]}个")
                print(f"总获得分数: {stats[3]}分")
    
    finally:
        conn.close()

if __name__ == '__main__':
    view_database_content() 