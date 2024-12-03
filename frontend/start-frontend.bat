@echo off
chcp 65001
echo 正在启动前端开发服务器...

:: 检查Node.js环境
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Node.js，请确保已安装Node.js并添加到PATH环境变量
    pause
    exit /b 1
)

:: 安装依赖
echo 安装依赖包...
call npm install
if %errorlevel% neq 0 (
    echo [错误] 安装依赖失败
    pause
    exit /b 1
)

:: 启动开发服务器
echo 启动开发服务器...
call npm run dev

pause 