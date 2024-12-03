from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict
import mysql.connector
import logging
from backend.config import CONFIG

# 配置日志
logger = logging.getLogger(__name__)

# 获取JWT配置
JWT_SECRET_KEY = CONFIG["jwt"]["jwt_secret_key"]
JWT_ALGORITHM = CONFIG["jwt"]["jwt_algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = CONFIG["jwt"]["access_token_expire_minutes"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"密码验证失败: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"密码哈希生成失败: {str(e)}")
        raise ValueError("密码处理失败")

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
            
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    except Exception as e:
        logger.error(f"创建访问令牌失败: {str(e)}")
        raise ValueError("令牌生成失败")

def get_user(username: str) -> Optional[Dict]:
    """获取用户信息"""
    try:
        conn = mysql.connector.connect(**CONFIG["database"])
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id, username, password, email, role, status
                FROM users 
                WHERE username = %s
            """, (username,))
            user = cursor.fetchone()
            
            if user and user['status'] != 'active':
                logger.warning(f"非活动用户尝试登录: {username}")
                return None
                
            return user
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return None

async def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """认证用户"""
    try:
        user = get_user(username)
        if not user:
            return None
            
        if not verify_password(password, user['password']):
            logger.warning(f"用户密码验证失败: {username}")
            return None
            
        # 不返回密码
        user.pop('password', None)
        return user
    except Exception as e:
        logger.error(f"用户认证失败: {str(e)}")
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 验证令牌
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
        # 获取用户信息
        user = get_user(username)
        if user is None:
            raise credentials_exception
            
        # 检查用户状态
        if user['status'] != 'active':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="用户账号已被禁用"
            )
            
        # 不返回密码
        user.pop('password', None)
        return user
        
    except JWTError as e:
        logger.error(f"JWT解码失败: {str(e)}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"获取当前用户失败: {str(e)}")
        raise credentials_exception

def update_last_activity(user_id: int, session_token: str) -> None:
    """更新用户最后活动时间"""
    try:
        conn = mysql.connector.connect(**CONFIG["database"])
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE user_sessions 
                SET last_activity = CURRENT_TIMESTAMP
                WHERE user_id = %s AND session_token = %s
            """, (user_id, session_token))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        logger.error(f"更新用户活动时间失败: {str(e)}")

def create_user_session(user_id: int, token: str, ip_address: str = None, user_agent: str = None) -> None:
    """创建用户会话记录"""
    try:
        conn = mysql.connector.connect(**CONFIG["database"])
        cursor = conn.cursor()
        try:
            # 清理旧会话
            cursor.execute("""
                DELETE FROM user_sessions 
                WHERE user_id = %s OR 
                      (last_activity < DATE_SUB(NOW(), INTERVAL 24 HOUR))
            """, (user_id,))
            
            # 创建新会话
            cursor.execute("""
                INSERT INTO user_sessions 
                (user_id, session_token, ip_address, user_agent)
                VALUES (%s, %s, %s, %s)
            """, (user_id, token, ip_address, user_agent))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        logger.error(f"创建用户会话失败: {str(e)}")

def invalidate_user_sessions(user_id: int) -> None:
    """使用户所有会话失效"""
    try:
        conn = mysql.connector.connect(**CONFIG["database"])
        cursor = conn.cursor()
        try:
            cursor.execute("""
                DELETE FROM user_sessions 
                WHERE user_id = %s
            """, (user_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
    except Exception as e:
        logger.error(f"使用户会话失效失败: {str(e)}")

def check_password_strength(password: str) -> bool:
    """检查密码强度"""
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        return False
    return True 