from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from core.database import get_db
from models.user import User
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import create_access_token, verify_password
from core.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录"""
    try:
        print(f"Login attempt for user: {form_data.username}")
        
        # 查询用户
        user = db.query(User).filter(User.username == form_data.username).first()
        print(f"Found user: {user is not None}")
        
        if user:
            print(f"User data: id={user.id}, username={user.username}")
            print(f"Verifying password...")
        
        # 验证用户名和密码
        if user and verify_password(form_data.password, user.password):
            print("Login successful")
            
            # 创建访问令牌
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username, "id": user.id, "role": user.role},
                expires_delta=access_token_expires
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role,
                    "status": user.status
                }
            }
        else:
            print("Login failed - Invalid credentials")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器内部错误: {str(e)}"
        )

@router.get("/user")
async def get_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "status": current_user.status
    } 