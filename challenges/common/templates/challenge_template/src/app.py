"""
靶场主程序模板
"""

import os
import sys
import logging
from flask import Flask, request, jsonify
from models import db, init_db
from utils import setup_logging

# 配置日志
logger = setup_logging()

def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)
    
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 
        'mysql://root:password@localhost/ctf_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化数据库
    db.init_app(app)
    with app.app_context():
        init_db()
    
    return app

def main():
    """主函数"""
    try:
        # 获取端口号
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
        
        # 创建应用
        app = create_app()
        
        # 启动应用
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except Exception as e:
        logger.error(f"应用启动失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 