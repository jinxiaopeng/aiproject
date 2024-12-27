import os
import sqlite3

def create_directory_structure():
    """创建项目目录结构"""
    directories = [
        'challenge_analysis',
        'challenge_analysis/core',
        'challenge_analysis/data',
        'challenge_analysis/models',
        'challenge_analysis/utils',
        'challenge_analysis/tests',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        # 在每个目录下创建__init__.py
        with open(os.path.join(directory, '__init__.py'), 'w') as f:
            f.write('"""{}"""\n'.format(directory.split('/')[-1]))

def create_base_files():
    """创建基础文件"""
    files = {
        'challenge_analysis/core/analyzer.py': '"""数据分析模块"""\n\nclass ChallengeAnalyzer:\n    pass\n',
        'challenge_analysis/core/recommender.py': '"""推荐系统模块"""\n\nclass ChallengeRecommender:\n    pass\n',
        'challenge_analysis/core/generator.py': '"""题目生成器模块"""\n\nclass ChallengeGenerator:\n    pass\n',
        
        'challenge_analysis/data/collector.py': '"""数据收集��块"""\n\nclass DataCollector:\n    pass\n',
        'challenge_analysis/data/sync.py': '"""数据同步模块"""\n\nclass DataSync:\n    pass\n',
        'challenge_analysis/data/storage.py': '"""SQLite管理模块"""\n\nclass SQLiteManager:\n    pass\n',
        
        'challenge_analysis/models/analysis.py': '"""分析结果模型"""\n\nclass AnalysisResult:\n    pass\n',
        'challenge_analysis/models/feedback.py': '"""反馈数据模型"""\n\nclass UserFeedback:\n    pass\n',
        'challenge_analysis/models/recommendation.py': '"""推荐模型"""\n\nclass Recommendation:\n    pass\n',
        
        'challenge_analysis/utils/db.py': '"""数据库工具"""\n\nclass DatabaseUtils:\n    pass\n',
        'challenge_analysis/utils/metrics.py': '"""评估指标工具"""\n\nclass Metrics:\n    pass\n',
        
        'challenge_analysis/config.py': '"""配置文件"""\n\nclass Config:\n    SQLITE_DB_PATH = "challenge_analysis.db"\n',
        'challenge_analysis/requirements.txt': 'SQLAlchemy==1.4.41\npandas==1.5.3\nnumpy==1.24.2\nscikit-learn==1.2.2\n',
    }
    
    for file_path, content in files.items():
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

def create_sqlite_database():
    """创建SQLite数据库和表"""
    db_path = 'challenge_analysis/challenge_analysis.db'
    
    # SQL语句
    tables = {
        'challenge_analytics': '''
            CREATE TABLE IF NOT EXISTS challenge_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                challenge_id INTEGER NOT NULL,
                total_attempts INTEGER DEFAULT 0,
                successful_attempts INTEGER DEFAULT 0,
                avg_completion_time INTEGER DEFAULT 0,
                avg_hints_used REAL DEFAULT 0,
                difficulty_score REAL DEFAULT 0,
                last_analysis_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(challenge_id)
            )
        ''',
        'challenge_feedback': '''
            CREATE TABLE IF NOT EXISTS challenge_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                challenge_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                difficulty_rating INTEGER CHECK(difficulty_rating BETWEEN 1 AND 5),
                quality_rating INTEGER CHECK(quality_rating BETWEEN 1 AND 5),
                feedback_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''',
        'challenge_recommendations': '''
            CREATE TABLE IF NOT EXISTS challenge_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                challenge_id INTEGER NOT NULL,
                recommendation_type TEXT,
                score REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, challenge_id)
            )
        '''
    }
    
    # 创建数据库连接
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建表
    for table_name, create_table_sql in tables.items():
        cursor.execute(create_table_sql)
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_challenge_analytics_id ON challenge_analytics(challenge_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_challenge_feedback_ids ON challenge_feedback(challenge_id, user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_challenge_recommendations_ids ON challenge_recommendations(user_id, challenge_id)')
    
    conn.commit()
    conn.close()

def main():
    """主函数"""
    print("开始创建项目结构...")
    create_directory_structure()
    print("创建基础文件...")
    create_base_files()
    print("创建SQLite数据库...")
    create_sqlite_database()
    print("项目���始化完成！")

if __name__ == '__main__':
    main() 