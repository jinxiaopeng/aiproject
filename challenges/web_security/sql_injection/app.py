from flask import Flask, request, render_template
import mysql.connector
import os

app = Flask(__name__)

db_config = {
    'host': os.environ.get('CHALLENGE_DB_HOST', 'localhost'),
    'user': os.environ.get('CHALLENGE_DB_USER', 'root'),
    'password': os.environ.get('CHALLENGE_DB_PASSWORD', 'challenge_pass'),
    'database': os.environ.get('CHALLENGE_DB_NAME', 'challenge_db')
}

def execute_query(query):
    """执行SQL查询并处理多个结果集"""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as e:
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        try:
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            results = execute_query(query)
            
            if results:
                # 从结果中获取用户名并显示
                welcome_msg = f"Welcome back, {results[0].get('username', 'user')}!"
                return render_template('login.html', message=welcome_msg, results=results)
            return render_template('login.html', message="Login failed!")
            
        except mysql.connector.Error as e:
            return render_template('login.html', message=f"Login failed!")
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True) 




    