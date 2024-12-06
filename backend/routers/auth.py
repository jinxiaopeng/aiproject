from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from models import User

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录"""
    try:
        # 查询用户
        user = db.query(User).filter(User.username == form_data.username).first()
        
        # 验证用户名和密码
        if user and user.password == form_data.password:  # 测试阶段直接比较密码
            return {
                "access_token": "test_token",
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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")  # 打印错误信息
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误，请稍后重试"
        )

@router.get("/user")
async def get_user_info():
    """获取当前用户信息"""
    # 测试阶段，直接返回模拟数据
    return {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
        "status": "active"
    } 