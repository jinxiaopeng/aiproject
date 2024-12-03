@echo off
chcp 65001
echo Git自动提交脚本

:: 检查Git是否安装
git --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Git，请确保已安装Git并添加到PATH环境变量
    pause
    exit /b 1
)

:: 获取当前时间
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set datetime=%datetime:~0,4%-%datetime:~4,2%-%datetime:~6,2% %datetime:~8,2%:%datetime:~10,2%:%datetime:~12,2%

:: 检查是否有未提交的更改
git status --porcelain > nul
if %errorlevel% equ 0 (
    :: 添加所有更改
    git add .

    :: 提交更改
    git commit -m "Auto commit: %datetime%"
    if %errorlevel% equ 0 (
        echo [成功] 更改已提交
        
        :: 尝试推送到远程仓库
        git push
        if %errorlevel% equ 0 (
            echo [成功] 更改已推送到远程仓库
        ) else (
            echo [警告] 推送到远程仓库失败，请手动推送
        )
    ) else (
        echo [错误] 提交失败
    )
) else (
    echo [信息] 没有需要提交的更改
)

pause 