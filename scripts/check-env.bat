@echo off
chcp 65001
echo 正在检查环境...

:: 检查Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python，请确保已安装Python并添加到PATH环境变量
    exit /b 1
) else (
    echo [√] Python环境正常
)

:: 检查Node.js
node --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Node.js，请确保已安装Node.js并添加到PATH环境变量
    exit /b 1
) else (
    echo [√] Node.js环境正常
)

:: 检查MySQL
sc query MySQL80 > nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] MySQL服务未运行或未安装
) else (
    echo [√] MySQL服务正常
)

:: 检查Redis
sc query Redis > nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] Redis服务未运行或未安装
) else (
    echo [√] Redis服务正常
)

:: 检查目录结构
if not exist frontend (
    echo [错误] 前端目录不存在
    exit /b 1
) else (
    echo [√] 前端目录正常
)

if not exist backend (
    echo [错误] 后端目录不存在
    exit /b 1
) else (
    echo [√] 后端目录正常
)

if not exist data (
    echo [错误] 数据目录不存在
    exit /b 1
) else (
    echo [√] 数据目录正常
)

echo 环境检查完成！ 