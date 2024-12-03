# 信息安全智能学习平台

[![Stars](https://img.shields.io/github/stars/jinxiaopeng/aiproject?style=social)](https://github.com/jinxiaopeng/aiproject)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Vue](https://img.shields.io/badge/vue-3.x-green.svg)](https://vuejs.org)

## 📖 项目概述

基于 Vue 3 + FastAPI 开发的信息安全智能学习平台，集成了 AI 辅助学习、靶场训练、知识图谱等功能。支持在线和离线两种使用模式，适合企业培训和个人学习。

### 主要特性

- **智能学习**
  - AI 辅助教学
  - 个性化学习路径
  - 知识图谱构建
  - 学习进度追踪

- **实战训练**
  - 在线靶场环境
  - CTF 挑战系统
  - 漏洞复现训练
  - 应急响应演练

- **企业特性**
  - 完整的权限管理
  - 详细的操作日志
  - 数据统计分析
  - 多环境部署支持

## 🚀 快速开始

### 环境要求

- Windows 10/11
- Python 3.8+
- Node.js 16+
- Docker Desktop
- Git (可选)

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/jinxiaopeng/aiproject.git
cd aiproject
```

2. **安装依赖**
```bash
# 后端依赖
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
```

3. **启动服务**
```bash
# Windows
.\start-all.bat

# 或分别启动
.\start-frontend.bat
.\start-backend.bat
```

4. **访问平台**
```
前端: http://localhost:8080
后端: http://localhost:8000
```

## 📂 项目结构

```
aiproject/
├── frontend/          # 前端项目 (Vue 3 + TypeScript)
├── backend/           # 后端项目 (FastAPI)
├── config/           # 配置文件
├── scripts/          # 脚本工具
└── docs/            # 项目文档
```

## 🔧 配置说明

### 数据库配置
```ini
# config/database.ini
[mysql]
host = localhost
port = 3306
database = aiproject
user = root
password = jxp1210
```

### 应用配置
```ini
# config/app.ini
[app]
debug = false
secret_key = your-secret-key
```

## 📝 开发指南

### 代码规范
- 使用 ESLint 和 Prettier 进行代码格式化
- 遵循 Vue 3 组合式 API 规范
- 使用 TypeScript 进行类型检查
- 遵循 PEP 8 Python 代码规范

### Git 工作流
- 主分支: master
- 开发分支: develop
- 功能分支: feature/*
- 修复分支: hotfix/*

### 提交规范
```
feat(模块): 添加新功能
fix(模块): 修复问题
docs(模块): 更新文档
style(模块): 代码格式
refactor(模块): 代码重构
test(模块): 添加测试
chore(模块): 构建过程或辅助工具的变动
```

## 🤝 参与贡献

1. Fork 本项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 开源协议

本项目采用 [MIT](LICENSE) 开源协议

## 🔄 更新日志

### v0.9.0 (2024-01)
- 支持完全离线部署
- 优化 AI 模型性能
- 增加基础靶场环境
- 完善部署脚本

### v0.8.0 (2023-12)
- 初始版本发布
- 基础功能实现
- 核心模块开发

## 📞 联系我们

- Issues: [GitHub Issues](https://github.com/jinxiaopeng/aiproject/issues)
- Email: support@example.com
- QQ群: 123456789
