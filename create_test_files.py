import os

# 创建测试目录
os.makedirs('test_challenge', exist_ok=True)

# 创建 Dockerfile
with open('test_challenge/Dockerfile', 'w') as f:
    f.write('''FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install flask
EXPOSE 8080
CMD ["python", "app.py"]''')

# 创建 docker-compose.yml
with open('test_challenge/docker-compose.yml', 'w') as f:
    f.write('''version: '3'
services:
  web:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - .:/app''')

# 创建 app.py
with open('test_challenge/app.py', 'w') as f:
    f.write('''from flask import Flask, render_template_string
app = Flask(__name__)

@app.route('/')
def hello():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Web Security Challenge</title>
        <style>
            body { 
                font-family: Arial, sans-serif;
                margin: 40px;
                text-align: center;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Web Security Challenge</h1>
            <p>Try to find the vulnerability!</p>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)''') 