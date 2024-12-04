# 信息安全智能学习平台

## 最新更新

### 2024-01-20
- 完善用户认证系统
  - 实现JWT认证
  - 添加用户画像功能
  - 集成成就系统
  - 优化数据库结构

## 功能特性

### 用户系统
- JWT基础认证
- 用户画像管理
- 学习进度追踪
- 成就系统集成
- 个性化学习路径

### 数据库设计
- 用户基础信息表
- 用户画像表
- 学习记录表
- 成就系统表

### 安全特性
- 密码加密存储
- JWT令牌认证
- 会话管理
- 权限控制

## 开发进度

- [x] 用户认证系统
  - [x] JWT认证实现
  - [x] 密码加密
  - [x] 用户注册/登录
  - [x] 会话管理
- [ ] 课程管理系统
- [ ] 实验环境
- [ ] AI助手集成
- [ ] 知识图谱
- [ ] 实时对战

## 技术栈

### 后端
- Python FastAPI
- SQLAlchemy ORM
- JWT认证
- MySQL数据库

### 前端
- Vue 3
- TypeScript
- Element Plus
- Axios

## 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/your-org/cyber-edu.git
cd cyber-edu
```

2. 安装依赖
```bash
# 后端依赖
cd backend
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
```

3. 初始化数据库
```bash
# Windows
scripts/init-db.bat

# Linux/Mac
./scripts/init-db.sh
```

4. 启动服务
```bash
# 后端服务
cd backend
python run.py

# 前端服务
cd frontend
npm run dev
```

## API文档

### 用户认证API
- POST /api/auth/register - 用户注册
- POST /api/auth/login - 用户登录
- GET /api/auth/me - 获取当前用户信息
- PUT /api/auth/profile - 更新用户资料

### 用户画像API
- GET /api/profile/skills - 获取技能评估
- GET /api/profile/achievements - 获取用户成就
- GET /api/profile/learning-path - 获取学习路径

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 开源协议

MIT License

