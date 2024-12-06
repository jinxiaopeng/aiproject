import hashlib
import hmac
import base64
from typing import Optional, Dict
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[Dict]:
    """验证令牌"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

# 保留原有的flag相关函数
def verify_flag(submitted_flag: str, stored_flag: str) -> bool:
    """验证提交的flag是否正确"""
    submitted_flag = submitted_flag.strip()
    stored_flag = stored_flag.strip()
    return hmac.compare_digest(
        submitted_flag.encode('utf-8'),
        stored_flag.encode('utf-8')
    )

def generate_flag(challenge_id: int, seed: Optional[str] = None) -> str:
    """生成flag"""
    if seed is None:
        seed = str(challenge_id)
    flag_data = f"{challenge_id}:{seed}".encode('utf-8')
    flag_hash = hashlib.sha256(flag_data).hexdigest()[:16]
    return f"flag{{{flag_hash}}}"

def encrypt_flag(flag: str) -> str:
    """加密flag"""
    return base64.b64encode(flag.encode('utf-8')).decode('utf-8')

def decrypt_flag(encrypted_flag: str) -> str:
    """解密flag"""
    return base64.b64decode(encrypted_flag.encode('utf-8')).decode('utf-8') 