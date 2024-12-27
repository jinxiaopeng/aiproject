import requests
import json
from requests.exceptions import RequestException, Timeout

def test_local_model():
    """测试本地模型的可用性"""
    # 尝试多个可能的地址
    base_urls = [
        "http://198.18.0.1:1234",
        "http://127.0.0.1:1234",
        "http://localhost:1234",
        "http://0.0.0.0:1234"
    ]
    timeout = 5  # 减少超时时间
    
    # 测试所有可能的地址
    for base_url in base_urls:
        print(f"\n尝试连接服务器: {base_url}")
        
        # 1. 测试服务器连接
        try:
            print(f"测试健康检查: GET {base_url}/health")
            response = requests.get(f"{base_url}/health", timeout=timeout)
            print(f"服务器状态码: {response.status_code}")
            
            # 如果连接成功，继续测试
            if response.status_code == 200:
                print("服务器连接成功！")
                return test_model_api(base_url, timeout)
        except Timeout:
            print(f"连接超时: {base_url}")
            continue
        except RequestException as e:
            print(f"连接失败: {str(e)}")
            continue
    
    print("\n所有地址都无法连接，请确保服务器已启动")

def test_model_api(base_url: str, timeout: int):
    """测试模型API功能"""
    # 2. 测试模型列表
    print("\n=== 测试获取模型列表 ===")
    try:
        print(f"发送请求: GET {base_url}/v1/models")
        response = requests.get(f"{base_url}/v1/models", timeout=timeout)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            models = response.json()
            print("可用模型列表:")
            for model in models.get("data", []):
                print(f"- {model.get('id', 'unknown')}")
        else:
            print(f"获取模型列表失败: {response.text}")
            return
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return

    # 3. 测试聊天功能
    print("\n=== 测试聊天功能 ===")
    try:
        chat_payload = {
            "model": "qwen2.5-coder-7b-instruct",
            "messages": [
                {"role": "user", "content": "你好，请简单介绍一下你自己。"}
            ],
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        print(f"发送请求: POST {base_url}/v1/chat/completions")
        print(f"请求数据: {json.dumps(chat_payload, ensure_ascii=False, indent=2)}")
        
        response = requests.post(
            f"{base_url}/v1/chat/completions",
            json=chat_payload,
            timeout=timeout
        )
        
        print(f"响应状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("\n模型回复:")
            print(result["choices"][0]["message"]["content"])
        else:
            print(f"聊天请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

if __name__ == "__main__":
    test_local_model() 