# Git自动提交脚本
Write-Host "Git自动提交脚本" -ForegroundColor Green

# 检查Git是否安装
try {
    $gitVersion = git --version
    Write-Host "Git版本: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[错误] 未找到Git，请确保已安装Git并添加到PATH环境变量" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 获取当前时间
$datetime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# 检查是否有未提交的更改
$status = git status --porcelain
if ($status) {
    # 添加所有更改
    Write-Host "正在添加更改..." -ForegroundColor Yellow
    git add .

    # 提交更改
    Write-Host "正在提交更改..." -ForegroundColor Yellow
    git commit -m "Auto commit: $datetime"
    if ($?) {
        Write-Host "[成功] 更改已提交" -ForegroundColor Green
        
        # 尝试推送到远程仓库
        Write-Host "正在推送到远程仓库..." -ForegroundColor Yellow
        git push
        if ($?) {
            Write-Host "[成功] 更改已推送到远程仓库" -ForegroundColor Green
        } else {
            Write-Host "[警告] 推送到远程仓库失败，请手动推送" -ForegroundColor Yellow
        }
    } else {
        Write-Host "[错误] 提交失败" -ForegroundColor Red
    }
} else {
    Write-Host "[信息] 没有需要提交的更改" -ForegroundColor Blue
}

Read-Host "按回车键退出" 