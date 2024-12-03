@echo off
chcp 65001
echo 正在初始化数据库...

:: 检查Python环境
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python，请确保已安装Python并添加到PATH环境变量
    pause
    exit /b 1
)

:: 检查MySQL服务
sc query MySQL80 > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] MySQL服务未运行或未安装
    pause
    exit /b 1
)

:: 安装必要的Python包
echo 正在安装必要的Python包...
pip install mysql-connector-python > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 安装Python包失败
    pause
    exit /b 1
)

:: 执行数据库初始化脚本
echo 正在执行数据库初始化...
python scripts/init_db.py
if %errorlevel% neq 0 (
    echo [错误] 数据库初始化失败
    pause
    exit /b 1
)

echo 数据库初始化完成！
pause 