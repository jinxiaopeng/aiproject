@echo off
chcp 65001
echo 正在启动所有服务...

:: 检查环境
call scripts\check-env.bat
if %errorlevel% neq 0 (
    echo [错误] 环境检查失败，请修复问题后重试
    pause
    exit /b 1
)

:: 启动后端服务
echo 启动后端服务...
start "Backend Server" cmd /c "cd backend && python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000"
if %errorlevel% neq 0 (
    echo [错误] 后端服务启动失败
    pause
    exit /b 1
) else (
    echo [√] 后端服务启动成功
)

:: 等待后端服务启动
timeout /t 5 /nobreak

:: 启动前端服务
echo 启动前端服务...
start "Frontend Server" cmd /c "cd frontend && npm run dev"
if %errorlevel% neq 0 (
    echo [错误] 前端服务启动失败
    pause
    exit /b 1
) else (
    echo [√] 前端服务启动成功
)

echo 所有服务启动完成！
echo 后端服务: http://localhost:8000
echo 前端服务: http://localhost:3000
echo API文档: http://localhost:8000/docs

pause 