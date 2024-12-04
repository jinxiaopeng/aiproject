@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None
) -> Token:
    """用户登录"""
    try:
        # 验证用户
        user = await authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # 创建访问令牌
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["username"]}, 
            expires_delta=access_token_expires
        )
        
        # 创建用户会话记录
        if request:
            create_user_session(
                user["id"],
                access_token,
                request.client.host,
                request.headers.get("user-agent", "")
            )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "role": user["role"],
                "avatar": user.get("avatar", "https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png")
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        system_logger.error(f"登录失败: {str(e)}", "auth")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误"
        ) 