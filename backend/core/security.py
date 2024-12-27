from typing import Optional, Dict
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from backend.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import logging

# 配置日志记录
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    try:
        logger.debug(f"Verifying password (length: {len(plain_password)})")
        result = pwd_context.verify(plain_password, hashed_password)
        logger.debug(f"Password verification result: {result}")
        return result
    except Exception as e:
        logger.error(f"Password verification error: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    try:
        logger.debug(f"Generating password hash (length: {len(password)})")
        hashed = pwd_context.hash(password)
        logger.debug("Password hash generated successfully")
        return hashed
    except Exception as e:
        logger.error(f"Password hash generation error: {str(e)}")
        raise

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    try:
        logger.debug("Creating access token")
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        logger.debug(f"Token payload: {to_encode}")
        
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        logger.debug("Access token created successfully")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Token creation error: {str(e)}")
        raise

def verify_token(token: str) -> Optional[Dict]:
    """验证令牌"""
    try:
        logger.debug("Verifying token")
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        logger.debug(f"Token payload: {payload}")
        return payload
    except JWTError as e:
        logger.error(f"Token verification error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected token verification error: {str(e)}")
        return None