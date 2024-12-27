import sqlite3
import os

def check_database():
    db_path = 'learning.db'
    if not os.path.exists(db_path):
        print(f"数据库文件 {db_path} 不存在")
        return
        
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 检查表是否存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("\n现有的表:", [table[0] for table in tables])
        
        # 查看视频进度表
        try:
            cursor.execute("SELECT * FROM video_progress")
            rows = cursor.fetchall()
            print("\n视频进度表数据:")
            if rows:
                for row in rows:
                    print(f"ID: {row[0]}, 用户: {row[1]}, 课程: {row[2]}, 章节: {row[3]}, 进度: {row[4]}%, 时长: {row[5]}秒, 当前时间: {row[6]}秒")
            else:
                print("暂无数据")
        except sqlite3.OperationalError as e:
            print("视频进度表查询失败:", e)
            
        # 查看学习行为表
        try:
            cursor.execute("SELECT * FROM learning_behavior")
            rows = cursor.fetchall()
            print("\n学习行为表数据:")
            if rows:
                for row in rows:
                    print(f"ID: {row[0]}, 用户: {row[1]}, 课程: {row[2]}, 开始时间: {row[3]}, 结束时间: {row[4]}, 时长: {row[5]}秒")
            else:
                print("暂无数据")
        except sqlite3.OperationalError as e:
            print("学习行为表查询失败:", e)
            
    except Exception as e:
        print("查询数据库时出错:", e)
    finally:
        conn.close()

if __name__ == '__main__':
    check_database() 