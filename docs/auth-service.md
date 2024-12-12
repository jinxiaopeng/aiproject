# 认证服务文档

## 概述

认证服务是一个独立的微服务，负责处理用户认证、授权和用户管理功能。它使用JWT（JSON Web Token）进行身份验证，并提供了完整的用户管理API。

## 技术栈

- FastAPI: Web框架
- SQLAlchemy: ORM
- PyJWT: JWT实现
- MySQL: 数据存储
- Pydantic: 数据验证

## 数据库设计

### 用户表 (users)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| username | String(50) | 用户名，唯一 |
| email | String(100) | 邮箱，唯一 |
| password | String(255) | 密码哈希 |
| role | Enum | 用户角色(admin/user) |
| status | Enum | 用户状态 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

## API接口

### 1. 用户认证

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
- 响应:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "username": "string",
      "email": "string",
      "role": "string",
      "status": "string"
    }
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
- 响应:
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "role": "string",
    "status": "string"
  }
  ```

### 2. 用户管理

#### 获取用户信息
- 端点: `/api/auth/user`
- 方法: GET
- 需要认证: 是
- 响应:
  ```json
  {
    "id": 1,
    "username": "string",
    "email": "string",
    "role": "string",
    "status": "string"
  }
  ```

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| DATABASE_URL | 数据库连接URL | mysql+mysqlconnector://root:password@localhost/auth_db |
| SECRET_KEY | JWT密钥 | your-secret-key-here |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token过期时间(分钟) | 30 |

### 配置文件

配置文件位于 `auth_service/core/config.py`，包含以下主要配置：

```python
class Settings(BaseSettings):
    PROJECT_NAME: str = "认证服务"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
```

## 部署说明

### 1. 准备环境

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置数据库

```sql
CREATE DATABASE auth_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 初始化数据库

```bash
python -m auth_service.init_db
```

### 4. 启动服务

```bash
python -m auth_service.run
```

## 开发指南

### 添加新的路由

1. 在 `routes` 目录下创建新的路由文件
2. 在路由文件中定义新的端点
3. 在 `main.py` 中注册路由

示例：
```python
from fastapi import APIRouter

router = APIRouter(prefix="/new", tags=["new"])

@router.get("/")
async def new_endpoint():
    return {"message": "New endpoint"}
```

### 添加新的模型

1. 在 `models` 目录下创建新的模型文件
2. 定义SQLAlchemy模型类
3. 在需要的地方导入并使用

示例：
```python
from sqlalchemy import Column, Integer, String
from database import Base

class NewModel(Base):
    __tablename__ = "new_table"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
```

## 安全说明

1. 密码使用bcrypt进行哈希处理
2. 使用JWT进行身份验证
3. 所有敏感配置都通过环境变量注入
4. 实现了请求频率限制
5. 支持CORS配置

## 日志说明

日志配置位于 `core/logger.py`，包含以下特性：

1. 控制台输出
2. 文件记录
3. 日志分级
4. 详细的错误追踪

## 测试

### 运行测试

```bash
pytest tests/
```

### 测试覆盖率

```bash
pytest --cov=auth_service tests/
```

## 常见问题

1. 数据库连接错误
   - 检查数据库服务是否运行
   - 验证连接字符串
   - 确认用户权限

2. Token验证失败
   - 检查token是否过期
   - 验证SECRET_KEY配置
   - 确认token格式

3. 密码重置失败
   - 检查邮件服务配置
   - 验证用户邮箱
   - 检查重置token 