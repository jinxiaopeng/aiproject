import requests
import json

def get_auth_token():
    url = "http://localhost:3017/auth/login"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": "admin",
        "password": "jxp1210"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token = response.json().get("token")
            if token:
                print(f"\nToken: {token}")
                return token
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    get_auth_token() 