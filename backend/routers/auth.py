from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from core.database import get_db
from models import User
from core.security import (
    verify_password,
    create_access_token,
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
import traceback

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录"""
    try:
        # 打印调试信息
        print(f"Login attempt for user: {form_data.username}")
        
        # 查询用户
        user = db.query(User).filter(User.username == form_data.username).first()
        print(f"User found: {user is not None}")
        
        if user:
            # 验证密码
            is_valid = verify_password(form_data.password, user.hashed_password)
            print(f"Password valid: {is_valid}")
            
            if is_valid:
                # 创建访问令牌
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token(
                    data={"sub": user.username},
                    expires_delta=access_token_expires
                )
                
                return {
                    "access_token": access_token,
                    "token_type": "bearer",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "avatar": user.avatar,
                        "role": user.role,
                        "status": user.status
                    }
                }
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        # 打印详细的错误信息
        print(f"Login error: {str(e)}")
        print("Error traceback:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误，请稍后重试"
        )

@router.get("/user")
async def get_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    try:
        return {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "avatar": current_user.avatar,
            "role": current_user.role,
            "status": current_user.status
        }
    except Exception as e:
        print(f"Get user info error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户信息失败"
        ) 