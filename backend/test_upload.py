import requests
import os

def test_file_upload():
    # 测试文件路径
    test_files = [
        "test_files/Dockerfile",
        "test_files/docker-compose.yml",
        "test_files/app.py"
    ]
    
    # 创建测试文件
    os.makedirs("test_files", exist_ok=True)
    
    # 创建示例 Dockerfile
    with open("test_files/Dockerfile", "w") as f:
        f.write("""FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
""")
    
    # 创建示例 docker-compose.yml
    with open("test_files/docker-compose.yml", "w") as f:
        f.write("""version: '3'
services:
  web:
    build: .
    ports:
      - "8000:8000"
""")
    
    # 创建示例 app.py
    with open("test_files/app.py", "w") as f:
        f.write("""from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
""")
    
    # 准备上传文件
    file_objects = []
    files = []
    
    try:
        # 打开文件
        for file_path in test_files:
            file_obj = open(file_path, 'rb')
            file_objects.append(file_obj)
            files.append(
                ('files', (os.path.basename(file_path), file_obj, 'application/octet-stream'))
            )
        
        # 发送上传请求
        response = requests.post(
            'http://localhost:8000/api/challenges/upload',
            files=files
        )
        
        # 打印响应
        print("Status Code:", response.status_code)
        print("Response:", response.json())
        
        if response.status_code == 200:
            # 获取上传的文件列表
            challenge_id = response.json()['challenge_id']
            files_response = requests.get(
                f'http://localhost:8000/api/challenges/files/{challenge_id}'
            )
            print("\nUploaded Files:", files_response.json())
            
    except Exception as e:
        print("Error:", str(e))
    
    finally:
        # 关闭所有打开的文件
        for file_obj in file_objects:
            file_obj.close()

if __name__ == "__main__":
    test_file_upload() 