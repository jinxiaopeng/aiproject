from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
import mysql.connector
import traceback

from config import JWT_SECRET_KEY, JWT_ALGORITHM, DB_CONFIG
from core.logger import system_logger

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password: str, password: str) -> bool:
    """验证密码"""
    try:
        system_logger.debug("开始密码验证", "auth")
        # 对于测试阶段,直接比较明文密码
        result = plain_password == password
        system_logger.debug(f"密码验证完成: {result}", "auth")
        return result
    except Exception as e:
        system_logger.error(f"密码验证失败: {str(e)}", "auth")
        return False

def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    try:
        return password  # 测试阶段直接返回明文密码
    except Exception as e:
        system_logger.error(f"密码哈希失败: {str(e)}", "auth")
        raise

async def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """验证用户"""
    conn = None
    cursor = None
    try:
        system_logger.info(f"尝试验证用户: {username}", "auth")
        conn = mysql.connector.connect(**DB_CONFIG)
        if not conn.is_connected():
            raise HTTPException(status_code=500, detail="数据库连接失败")
            
        cursor = conn.cursor(dictionary=True)
        
        # 查询用户
        system_logger.debug(f"执行用户查询", "auth")
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND disabled = FALSE",
            (username,)
        )
        user = cursor.fetchone()
        
        if not user:
            system_logger.warning(f"用户不存在或已禁用: {username}", "auth")
            return None
            
        # 验证密码
        if not verify_password(password, user["password"]):
            system_logger.warning(f"密码验证失败: {username}", "auth")
            return None
        
        # 返回完整的用户信息（除了密码）
        user_info = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user.get("role", "user"),  # 默认角色为user
            "disabled": user["disabled"]
        }
        
        system_logger.info(f"用户验证成功: {username}", "auth")
        return user_info
        
    except mysql.connector.Error as e:
        system_logger.error(f"数据库错误: {str(e)}", "auth", {
            'error_code': e.errno,
            'error_msg': str(e)
        })
        raise HTTPException(
            status_code=500,
            detail="数据库错误，请稍后重试"
        )
    except Exception as e:
        system_logger.error(f"用户验证过程出错: {str(e)}", "auth", {
            'username': username,
            'error': str(e),
            'traceback': traceback.format_exc()
        })
        raise HTTPException(
            status_code=500,
            detail="服务器内部错误"
        )
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        system_logger.info(f"创建访问令牌成功: {data.get('sub')}", "auth")
        return encoded_jwt
    except Exception as e:
        system_logger.error(f"创建访问令牌失败: {str(e)}", "auth", {
            'data': data,
            'error': str(e)
        })
        raise

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码JWT令牌
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            system_logger.warning("令牌中缺少用户名", "auth")
            raise credentials_exception
        
        system_logger.info(f"令牌解码成功: {username}", "auth")
            
        # 从数据库获取用户信息
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND disabled = FALSE",
            (username,)
        )
        user = cursor.fetchone()
        
        if user is None:
            system_logger.warning(f"用户不存在已禁用: {username}", "auth")
            raise credentials_exception
        
        system_logger.info(f"获取当前用户成功: {username}", "auth")
        return user
        
    except JWTError as e:
        system_logger.error(f"JWT解码失败: {str(e)}", "auth")
        raise credentials_exception
    except Exception as e:
        system_logger.error(f"获取当前用户失败: {str(e)}", "auth")
        raise
    finally:
        cursor.close()
        conn.close()

def create_user_session(user_id: int, token: str, ip_address: str, user_agent: str):
    """创建用户会话"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO user_sessions (user_id, token, ip_address, user_agent)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, token, ip_address, user_agent)
        )
        conn.commit()
        system_logger.info(f"创建用户会话成功: {user_id}", "auth")
        
    except Exception as e:
        system_logger.error(f"创建用户会话失败: {str(e)}", "auth", {
            'user_id': user_id,
            'error': str(e)
        })
    finally:
        cursor.close()
        conn.close()

def update_last_activity(user_id: int, token: str):
    """更新用户最后活动时间"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE user_sessions 
            SET last_activity = CURRENT_TIMESTAMP
            WHERE user_id = %s AND token = %s
            """,
            (user_id, token)
        )
        conn.commit()
        system_logger.info(f"更新用户活动时间成功: {user_id}", "auth")
        
    except Exception as e:
        system_logger.error(f"更新用户活动时间失败: {str(e)}", "auth", {
            'user_id': user_id,
            'error': str(e)
        })
    finally:
        cursor.close()
        conn.close()

def invalidate_user_sessions(user_id: int):
    """使用户所有会话失效"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute(
            "DELETE FROM user_sessions WHERE user_id = %s",
            (user_id,)
        )
        conn.commit()
        system_logger.info(f"使用户会话失效成功: {user_id}", "auth")
        
    except Exception as e:
        system_logger.error(f"使用户会话失效失败: {str(e)}", "auth", {
            'user_id': user_id,
            'error': str(e)
        })
    finally:
        cursor.close()
        conn.close()