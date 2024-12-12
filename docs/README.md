# 知识图谱系统文档

## 项目概述

本项目是一个基于FastAPI和Vue.js开发的知识图谱系统，包含两个主要服务：

1. 知识图谱服务 (Knowledge Graph Service)
2. 认证服务 (Authentication Service)

## 系统架构

### 后端服务

#### 1. 认证服务 (端口: 8001)
- 位置: `/backend/auth_service`
- 功能:
  - 用户认证
  - 用户管理
  - JWT token生成和验证
- 数据库: MySQL (auth_db)

#### 2. 知识图谱服务 (端口: 8000)
- 位置: `/backend/knowledge_graph`
- 功能:
  - 实体管理
  - 关系管理
  - 图谱查询和分析
- 数据库: MySQL (aiproject)

### 前端应用 (端口: 3000)
- 位置: `/frontend`
- 技术栈:
  - Vue 3
  - Pinia (状态管理)
  - Element Plus (UI组件库)
  - Vite (构建工具)

## 快速开始

### 1. 环境要求
- Python 3.8+
- Node.js 14+
- MySQL 8.0+

### 2. 安装依赖

后端依赖:
```bash
cd backend
pip install -r requirements.txt
```

前端依赖:
```bash
cd frontend
npm install
```

### 3. 数据库配置

创建所需的数据库:
```sql
CREATE DATABASE auth_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE aiproject CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 启动服务

启动认证服务:
```bash
cd backend
python -m auth_service.run
```

启动知识图谱服务:
```bash
cd backend
python -m knowledge_graph.main
```

启动前端开发服务器:
```bash
cd frontend
npm run dev
```

## API文档

### 认证服务API

#### 登录
- 端点: `/api/auth/login`
- 方法: POST
- 参数:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

#### 注册
- 端点: `/api/auth/register`
- 方法: POST
- 参数:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```

### 知识图谱API

#### 创建实体
- 端点: `/api/entities`
- 方法: POST
- 需要认证: 是
- 参数:
  ```json
  {
    "name": "string",
    "entity_type": "string",
    "description": "string",
    "properties": {}
  }
  ```

#### 创建关系
- 端点: `/api/relationships`
- 方法: POST
- 需要认证: 是
- 参数:
  ```json
  {
    "source_id": "integer",
    "target_id": "integer",
    "relationship_type": "string",
    "properties": {}
  }
  ```

## 项目结构

```
project/
├── backend/
│   ├── auth_service/        # 认证服务
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   └── routes/
│   │
│   └── knowledge_graph/     # 知识图谱服务
│       ├── api/
│       ├── core/
│       ├── models/
│       └── services/
│
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── stores/
│   │   └── views/
│   │
│   └── public/
│
└── docs/                  # 项目文档
```

## 开发指南

### 代码规范
- Python: 遵循PEP 8规范
- TypeScript/Vue: 遵循项目内置的ESLint规则
- 提交信息: 使用语义化提交信息

### 分支管理
- main: 主分支，用于生产环境
- develop: 开发分支
- feature/*: 功能分支
- bugfix/*: 修复分支

## 部署指南

### Docker部署
1. 构建镜像
```bash
docker-compose build
```

2. 启动服务
```bash
docker-compose up -d
```

### 传统部署
1. 配置Nginx反向代理
2. 设置环境变量
3. 启动服务
4. 配置SSL证书

## 常见问题

1. 登录失败
   - 检查数据库连接
   - 验证用户凭据
   - 查看日志文件

2. 数据库连接错误
   - 确认数据库服务运行状态
   - 检查连接字符串
   - 验证用户权限

3. 前端API请求失败
   - 检查API地址配置
   - 确认代理设置
   - 查看浏览器控制台错误

## 更新日志

### v1.0.0 (2023-12-10)
- 初始版本发布
- 基本的用户认证功能
- 知识图谱基础功能

## 维护者

- 项目负责人：[您的名字]
- 联系方式：[您的邮箱]

## 许可证

MIT License 