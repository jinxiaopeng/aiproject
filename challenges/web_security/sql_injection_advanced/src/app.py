from flask import Flask, request, render_template, jsonify, session, redirect, url_for
import sqlite3
import os
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)

# 数据库初始化
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # 创建用户表
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # 创建秘密表（存储flag）
    c.execute('''
        CREATE TABLE IF NOT EXISTS secrets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            value TEXT NOT NULL
        )
    ''')
    
    # 创建管理员账号和flag
    admin_pass = hashlib.sha256('admin123'.encode()).hexdigest()
    try:
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                 ('admin', admin_pass, 'admin'))
        c.execute('INSERT INTO secrets (key, value) VALUES (?, ?)',
                 ('flag', 'flag{sql_injection_master_plus_2023}'))
    except sqlite3.IntegrityError:
        pass  # 管理员已存在
    
    conn.commit()
    conn.close()

init_db()

def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            error = "请输入用户名和密码"
            return render_template('login.html', error=error)
        
        conn = get_db()
        c = conn.cursor()
        
        try:
            # 故意使用不安全的查询方式
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hashlib.sha256(password.encode()).hexdigest()}'"
            c.execute(query)
            user = c.fetchone()
            
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                return redirect(url_for('dashboard'))
            else:
                error = "用户名或密码错误"
        except sqlite3.Error as e:
            error = f"数据库错误: {str(e)}"
        finally:
            conn.close()
            
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_info = {
        'username': session['username'],
        'role': session['role']
    }
    
    # 如果是管理员，显示管理面板链接
    if session['role'] == 'admin':
        return render_template('admin_dashboard.html', user=user_info)
    
    return render_template('dashboard.html', user=user_info)

@app.route('/admin/panel')
def admin_panel():
    if 'user_id' not in session or session['role'] != 'admin':
        return "Access Denied", 403
    
    conn = get_db()
    c = conn.cursor()
    
    try:
        c.execute('SELECT * FROM secrets')
        secrets = c.fetchall()
        return render_template('admin_panel.html', secrets=secrets)
    finally:
        conn.close()

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082, debug=True) 