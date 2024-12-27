"""
SQL注入训练靶场
"""

from flask import Flask, request, render_template, jsonify, session, make_response
import sqlite3
import os
import logging
import time
from functools import wraps
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 用于session加密

# 安全配置
@app.after_request
def add_security_headers(response):
    """添加安全响应头"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'"
    return response

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

# 提示系统
HINTS = [
    {
        "id": 1,
        "title": "基础提示",
        "content": "尝试在用户名输入框中使用单引号",
        "cost": 0
    },
    {
        "id": 2,
        "title": "SQL语法提示",
        "content": "考虑使用OR 1=1绕过登录验证",
        "cost": 5
    },
    {
        "id": 3,
        "title": "进阶提示",
        "content": "尝试使用UNION SELECT语句获取更多信息",
        "cost": 10
    }
]

def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect('test.db')
    conn.row_factory = sqlite3.Row  # 设置行工厂，使结果可以通过列名访问
    return conn

def init_db():
    """初始化数据库"""
    try:
        conn = get_db()
        c = conn.cursor()
        
        # 创建用户表
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        ''')
        
        # 创建敏感数据表
        c.execute('''
        CREATE TABLE IF NOT EXISTS sensitive_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL UNIQUE,
            value TEXT NOT NULL
        )
        ''')
        
        # 创建登录日志表
        c.execute('''
        CREATE TABLE IF NOT EXISTS login_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            ip_address TEXT NOT NULL,
            user_agent TEXT,
            status TEXT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 创建进度追踪表
        c.execute('''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            current_step INTEGER DEFAULT 1,
            hints_used TEXT DEFAULT '[]',
            attempts INTEGER DEFAULT 0,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # 插入测试数据
        c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", 
                 ("admin", "admin123"))
        c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", 
                 ("test", "test123"))
        
        c.execute("INSERT OR IGNORE INTO sensitive_data (key, value) VALUES (?, ?)", 
                 ("flag", "flag{test_sql_injection_success}"))
        c.execute("INSERT OR IGNORE INTO sensitive_data (key, value) VALUES (?, ?)", 
                 ("secret_key", "this_is_a_secret_key"))
        
        conn.commit()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise
    finally:
        conn.close()

def get_or_create_progress():
    """获取或创建进度记录"""
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    
    conn = get_db()
    c = conn.cursor()
    
    # 查找现有进度
    c.execute("SELECT * FROM progress WHERE session_id = ?", (session['session_id'],))
    progress = c.fetchone()
    
    if not progress:
        # 创建新进度记录
        c.execute("""
        INSERT INTO progress (session_id, current_step, hints_used, attempts)
        VALUES (?, 1, '[]', 0)
        """, (session['session_id'],))
        conn.commit()
        
        c.execute("SELECT * FROM progress WHERE session_id = ?", (session['session_id'],))
        progress = c.fetchone()
    
    conn.close()
    return dict(progress)

def update_progress(field, value):
    """更新进度记录"""
    conn = get_db()
    c = conn.cursor()
    
    c.execute(f"""
    UPDATE progress 
    SET {field} = ?, updated_at = CURRENT_TIMESTAMP
    WHERE session_id = ?
    """, (value, session['session_id']))
    
    conn.commit()
    conn.close()

def log_login_attempt(username, status, message=None):
    """记录登录尝试"""
    try:
        conn = get_db()
        c = conn.cursor()
        
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        c.execute('''
        INSERT INTO login_logs (username, ip_address, user_agent, status, message)
        VALUES (?, ?, ?, ?, ?)
        ''', (username, ip_address, user_agent, status, message))
        
        conn.commit()
        
        # 更新尝试次数
        progress = get_or_create_progress()
        update_progress('attempts', progress['attempts'] + 1)
        
    except Exception as e:
        logger.error(f"Failed to log login attempt: {str(e)}")
    finally:
        conn.close()

def rate_limit(func):
    """简单的速率限制装饰器"""
    last_requests = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        ip = request.remote_addr
        current_time = time.time()
        
        if ip in last_requests:
            time_passed = current_time - last_requests[ip]
            if time_passed < 1:  # 限制每秒最多1次请求
                return jsonify({
                    "success": False,
                    "message": "Too many requests, please try again later"
                }), 429
        
        last_requests[ip] = current_time
        return func(*args, **kwargs)
    
    return wrapper

@app.route('/')
def index():
    progress = get_or_create_progress()
    return render_template('index.html', progress=progress)

@app.route('/login', methods=['POST'])
@rate_limit
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    # 记录尝试的参数
    logger.info(f"Login attempt - Username: {username}")
    
    try:
        conn = get_db()
        c = conn.cursor()
        
        # 故意使用不安全的SQL查询
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        logger.debug(f"Executing query: {query}")
        
        try:
            c.execute(query)
            user = c.fetchone()
            
            if user:
                # 如果登录成功，返回flag
                c.execute("SELECT value FROM sensitive_data WHERE key='flag'")
                flag = c.fetchone()['value']
                
                # 更新进度
                update_progress('completed', True)
                log_login_attempt(username, "success")
                
                return jsonify({
                    "success": True,
                    "message": "Login successful!",
                    "flag": flag
                })
            else:
                log_login_attempt(username, "failed", "Invalid credentials")
                return jsonify({
                    "success": False,
                    "message": "Invalid username or password"
                })
                
        except sqlite3.Error as e:
            # 记录SQL错误（这是故意的，帮助学习者理解SQL注入）
            error_msg = str(e)
            log_login_attempt(username, "error", error_msg)
            return jsonify({
                "success": False,
                "message": f"Database error: {error_msg}"
            })
            
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        log_login_attempt(username, "error", str(e))
        return jsonify({
            "success": False,
            "message": "An unexpected error occurred"
        })
    finally:
        conn.close()

@app.route('/hints')
def get_hints():
    """获取可用提示"""
    progress = get_or_create_progress()
    used_hints = eval(progress['hints_used'])
    
    available_hints = []
    for hint in HINTS:
        hint_data = hint.copy()
        hint_data['unlocked'] = hint['id'] in used_hints
        available_hints.append(hint_data)
    
    return jsonify({
        "hints": available_hints,
        "used_count": len(used_hints)
    })

@app.route('/hints/<int:hint_id>/unlock', methods=['POST'])
def unlock_hint(hint_id):
    """解锁提示"""
    progress = get_or_create_progress()
    used_hints = eval(progress['hints_used'])
    
    if hint_id in used_hints:
        return jsonify({
            "success": False,
            "message": "Hint already unlocked"
        })
    
    hint = next((h for h in HINTS if h['id'] == hint_id), None)
    if not hint:
        return jsonify({
            "success": False,
            "message": "Hint not found"
        })
    
    # 更新已使用的提示
    used_hints.append(hint_id)
    update_progress('hints_used', str(used_hints))
    
    return jsonify({
        "success": True,
        "hint": hint
    })

@app.route('/progress')
def get_progress():
    """获取当前进度"""
    progress = get_or_create_progress()
    return jsonify(progress)

@app.route('/stats')
def stats():
    """查看登录统计（仅用于教学目的）"""
    try:
        conn = get_db()
        c = conn.cursor()
        
        # 获取最近的登录尝试
        c.execute('''
        SELECT username, ip_address, status, message, created_at
        FROM login_logs
        ORDER BY created_at DESC
        LIMIT 10
        ''')
        
        logs = [dict(row) for row in c.fetchall()]
        
        # 获取统计信息
        c.execute('''
        SELECT status, COUNT(*) as count
        FROM login_logs
        GROUP BY status
        ''')
        
        stats = [dict(row) for row in c.fetchall()]
        
        return jsonify({
            "recent_logs": logs,
            "statistics": stats
        })
        
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to get statistics"
        })
    finally:
        conn.close()

@app.route('/reset', methods=['POST'])
def reset_progress():
    """重置训练进度"""
    try:
        conn = get_db()
        c = conn.cursor()
        
        # 删除当前会话的进度
        c.execute("DELETE FROM progress WHERE session_id = ?", (session['session_id'],))
        conn.commit()
        
        # 创建新的进度记录
        progress = get_or_create_progress()
        
        return jsonify({
            "success": True,
            "message": "Progress reset successfully",
            "progress": progress
        })
    except Exception as e:
        logger.error(f"Reset error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Failed to reset progress"
        })
    finally:
        conn.close()

if __name__ == '__main__':
    # 确保数据库存在
    if not os.path.exists('test.db'):
        init_db()
    
    # 获取端口号
    port = int(os.environ.get('PORT', 3000))
    
    # 启动应用
    app.run(host='0.0.0.0', port=port, debug=True) 