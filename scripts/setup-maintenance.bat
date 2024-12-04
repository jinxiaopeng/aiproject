@echo off
chcp 65001
echo 设置自动维护计划任务...

:: 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 请以管理员权限运行此脚本
    pause
    exit /b 1
)

:: 创建任务目录
schtasks /Create /TN "\WebSecurityPlatform" /F >nul 2>&1

:: 创建文档更新任务
schtasks /Create /TN "\WebSecurityPlatform\UpdateDocs" /TR "powershell.exe -ExecutionPolicy Bypass -File \"%~dp0update-docs.ps1\"" /SC MINUTE /MO 10 /F
if %errorlevel% equ 0 (
    echo [成功] 文档更新任务已创建
) else (
    echo [错误] 创建文档更新任务失败
)

:: 创建Git维护任务
schtasks /Create /TN "\WebSecurityPlatform\GitMaintenance" /TR "powershell.exe -ExecutionPolicy Bypass -File \"%~dp0git-auto-commit.ps1\"" /SC MINUTE /MO 10 /F
if %errorlevel% equ 0 (
    echo [成功] Git维护任务已创建
) else (
    echo [错误] 创建Git维护任务失败
)

:: 显示任务状态
echo.
echo 当前计划任务状态：
schtasks /Query /TN "\WebSecurityPlatform\UpdateDocs"
schtasks /Query /TN "\WebSecurityPlatform\GitMaintenance"

echo.
echo [信息] 系统将每10分钟自动运行维护任务
echo [信息] 可以在任务计划程序中查看详细信息

pause 