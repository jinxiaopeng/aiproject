@echo off
chcp 65001 > nul
echo 启动自动维护服务...

set SCRIPT_PATH=%~dp0auto-maintain.ps1
set POWERSHELL_PATH=C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

echo 正在启动PowerShell脚本...
"%POWERSHELL_PATH%" -ExecutionPolicy Bypass -NoProfile -File "%SCRIPT_PATH%"

if %ERRORLEVEL% NEQ 0 (
    echo [错误] 启动失败
    pause
    exit /b 1
)

echo 自动维护服务已启动
timeout /t 3

pause 