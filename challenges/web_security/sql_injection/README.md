# SQL注入基础挑战

这是一个基础的SQL注入训练靶场，用于学习和练习SQL注入技术。

## 挑战描述

这是一个简单的登录系统，存在SQL注入漏洞。你的目标是：
1. 绕过登录验证
2. 获取管理员权限
3. 获取flag

## 环境要求

- Docker
- Docker Compose

## 快速开始

1. 构建并启动环境：
   ```bash
   docker-compose up -d
   ```

2. 访问靶场：
   - 打开浏览器访问：http://localhost:8081

3. 获取提示：
   - 访问 http://localhost:8081/hint

## 目录结构

```
.
├── app.py              # 主应用程序
├── database/
│   └── init.sql       # 数据库初始化脚本
├── src/
│   └── templates/     # HTML模板文件
├── Dockerfile         # Docker构建文件
├── docker-compose.yml # Docker编排文件
└── requirements.txt   # Python依赖
```

## Flag格式

flag{sql_injection_master_2023}