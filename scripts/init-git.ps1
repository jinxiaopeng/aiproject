# Git初始化脚本
Write-Host "Git初始化脚本" -ForegroundColor Green

# 检查Git是否安装
try {
    $gitVersion = git --version
    Write-Host "Git版本: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[错误] 未找到Git，请确保已安装Git并添加到PATH环境变量" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 初始化Git仓库
Write-Host "正在初始化Git仓库..." -ForegroundColor Yellow
git init
if ($?) {
    Write-Host "[成功] Git仓库初始化完成" -ForegroundColor Green
} else {
    Write-Host "[错误] Git仓库初始化失败" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 配置Git
Write-Host "正在配置Git..." -ForegroundColor Yellow
$userName = Read-Host "请输入Git用户名"
$userEmail = Read-Host "请输入Git邮箱"

git config user.name $userName
git config user.email $userEmail

# 添加文件
Write-Host "正在添加文件..." -ForegroundColor Yellow
git add .

# 初始提交
Write-Host "正在进行初始提交..." -ForegroundColor Yellow
git commit -m "Initial commit: Project setup"
if ($?) {
    Write-Host "[成功] 初始提交完成" -ForegroundColor Green
} else {
    Write-Host "[错误] 初始提交失败" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 询问是否添加远程仓库
$addRemote = Read-Host "是否要添加远程仓库？(y/n)"
if ($addRemote -eq "y") {
    $remoteUrl = Read-Host "请输入远程仓库地址"
    git remote add origin $remoteUrl
    if ($?) {
        Write-Host "[成功] 远程仓库添加成功" -ForegroundColor Green
        
        # 推送到远程仓库
        Write-Host "正在推送到远程仓库..." -ForegroundColor Yellow
        git push -u origin master
        if ($?) {
            Write-Host "[成功] 推送完成" -ForegroundColor Green
        } else {
            Write-Host "[错误] 推送失败" -ForegroundColor Red
        }
    } else {
        Write-Host "[错误] 远程仓库添加失败" -ForegroundColor Red
    }
}

Write-Host "Git初始化完成！" -ForegroundColor Green
Read-Host "按回车键退出" 