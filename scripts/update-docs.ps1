# 自动更新文档脚本
# UTF-8 with BOM
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 获取当前日期
$date = Get-Date -Format "yyyy-MM-dd"

# 更新函数
function Update-Documentation {
    param (
        [string]$CommitMessage
    )
    
    # 获取最近的Git提交
    $lastCommit = git log -1 --pretty=format:"%s"
    
    # 更新README.md
    $readmeContent = Get-Content README.md -Raw -Encoding UTF8
    $updateSection = @"
## 最新更新

### $date
- $CommitMessage
"@
    
    # 替换更新部分
    $readmeContent = $readmeContent -replace "(?s)## 最新更新.*?(?=##)", "$updateSection`n`n"
    $readmeContent | Set-Content README.md -Force -Encoding UTF8
    
    # 更新API文档
    Update-ApiDocs
    
    # 更新技术文档
    Update-TechDocs
    
    # 提交文档更新
    git add README.md docs/
    git commit -m "docs: Update documentation - $CommitMessage"
}

# 更新API文档
function Update-ApiDocs {
    # 检查并创建docs目录
    if (-not (Test-Path "docs/api")) {
        New-Item -ItemType Directory -Path "docs/api" -Force
    }
    
    # 扫描后端路由
    $apiDocs = @"
# API Documentation

## Authentication
- POST /api/auth/register - User Registration
- POST /api/auth/login - User Login
- GET /api/auth/me - Get Current User Info
- PUT /api/auth/profile - Update User Profile

## User Profile
- GET /api/profile/skills - Get Skill Assessment
- GET /api/profile/achievements - Get User Achievements
- GET /api/profile/learning-path - Get Learning Path

## Course Management
- GET /api/courses - Get Course List
- GET /api/courses/{id} - Get Course Details
- POST /api/courses - Create Course
- PUT /api/courses/{id} - Update Course
- DELETE /api/courses/{id} - Delete Course

## Lab Environment
- GET /api/labs - Get Lab List
- POST /api/labs/start - Start Lab Environment
- POST /api/labs/stop - Stop Lab Environment
- GET /api/labs/status - Get Environment Status

## Learning Records
- GET /api/learning/progress - Get Learning Progress
- POST /api/learning/record - Record Learning Activity
- GET /api/learning/statistics - Get Learning Statistics

## Achievement System
- GET /api/achievements - Get Achievement List
- GET /api/achievements/user - Get User Achievements
- POST /api/achievements/verify - Verify Achievement Completion
"@
    
    $apiDocs | Set-Content "docs/api/README.md" -Force -Encoding UTF8
}

# 更新技术文档
function Update-TechDocs {
    # 检查并创建docs目录
    if (-not (Test-Path "docs/tech")) {
        New-Item -ItemType Directory -Path "docs/tech" -Force
    }
    
    # 生成技术文档
    $techDocs = @"
# Technical Documentation

## Architecture Design
- Frontend-Backend Separation
- RESTful API Design
- Microservices Architecture Preparation

## Database Design
- User System Tables
- Course Management Tables
- Learning Records Tables
- Achievement System Tables

## Security Design
- JWT Authentication
- Password Encryption
- Permission Control
- Data Security Protection

## Deployment
- Docker Containerization
- Kubernetes Cluster
- CI/CD Pipeline
- Monitoring System
"@
    
    $techDocs | Set-Content "docs/tech/README.md" -Force -Encoding UTF8
}

# 主函数
function Main {
    # 获取最近的提交信息
    $lastCommit = git log -1 --pretty=format:"%s"
    
    # 更新文档
    Update-Documentation -CommitMessage $lastCommit
    
    Write-Host "Documentation update completed!" -ForegroundColor Green
}

# 运行主函数
Main 