from fastapi import APIRouter, HTTPException, Depends, status, Request, Form
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel
import logging
import traceback

from database import get_db
from models.user import User
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import create_access_token, verify_password, get_password_hash
from core.deps import get_current_user

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """用户登录"""
    try:
        logger.info(f"Login attempt - username: {username}")
        
        # 查询用户
        try:
            user = db.query(User).filter(User.username == username).first()
            logger.info(f"User query result: {user is not None}")
            
            if user:
                logger.info(f"Found user: id={user.id}, username={user.username}, role={user.role}")
                logger.info(f"Stored password hash: {user.password}")
            else:
                logger.info(f"No user found with username: {username}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="用户名或密码错误"
                )
        except Exception as e:
            logger.error(f"Database query error: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"数据库查询错误: {str(e)}"
            )
            
        # 验证密码
        try:
            is_valid = verify_password(password, user.password)
            logger.info(f"Password verification result: {is_valid}")
            
            if not is_valid:
                logger.info("Password verification failed")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="用户名或密码错误"
                )
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"密码验证错误: {str(e)}"
            )
            
        # 创建访问令牌
        try:
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username, "id": user.id, "role": user.role},
                expires_delta=access_token_expires
            )
            logger.info("Access token created successfully")
            
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
        except Exception as e:
            logger.error(f"Token creation error: {str(e)}")
            logger.error(traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"令牌创建错误: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in login: {str(e)}")
        logger.error(traceback.format_exc())
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