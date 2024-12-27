# SQL注入挑战（进阶版）

这是一个模拟管理员登录系统的SQL注入挑战。

## 挑战描述

你需要绕过登录验证，获取管理员权限，并从管理面板获取flag。

### 难度：中等

### 知识点：
- SQL注入
- 密码哈希绕过
- 权限提升

### 提示：
1. 这是一个管理员登录页面
2. 密码经过了SHA256加密
3. 尝试绕过登录验证并获取管理员权限
4. 成功后可在管理面板获取flag

## 部署说明

### 使用Docker部署

1. 安装Docker和Docker Compose
2. 在项目目录下运行：
   ```bash
   docker-compose up -d
   ```
3. 访问 http://localhost:8082

### 手动部署

1. 安装Python 3.8+
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行应用
   ```bash
   cd src
   python app.py
   ```
4. 访问 http://localhost:8082

## 解题思路

1. 分析登录处的SQL注入点
2. 构造payload绕过密码哈希
3. 获取管理员权限
4. 访问管理面板获取flag

## Flag格式

flag{sql_injection_master_plus_2023} 