from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from core.database import get_db
from core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据"
    )
    
    try:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise credentials_exception
            
        scheme, token = auth_header.split()
        if scheme.lower() != 'bearer':
            raise credentials_exception
            
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except (JWTError, ValueError):
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_optional(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """获取当前用户（可选的）"""
    try:
        return await get_current_user(request, db)
    except HTTPException:
        return None 