@echo off
chcp 65001
echo 正在启动Web安全智能学习平台...

:: 检查Python环境
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python，请确保已安装Python并添加到PATH环境变量
    pause
    exit /b 1
)

:: 检查虚拟环境
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
)

:: 激活虚拟环境
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [错误] 激活虚拟环境失败
    pause
    exit /b 1
)

:: 安装依赖
echo 安装依赖包...
python -m pip install -r backend/requirements.txt
if %errorlevel% neq 0 (
    echo [错误] 安装依赖包失败
    pause
    exit /b 1
)

:: 设置环境变量
set PYTHONPATH=%cd%

:: 初始化数据库
echo 初始化数据库...
python scripts/init_db.py
if %errorlevel% neq 0 (
    echo [警告] 数据库初始化可能未完全成功
    echo 请检查数据库配置和连接
)

:: 启动应用
echo 启动应用程序...
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

pause 