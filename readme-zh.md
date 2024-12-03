# Web安全智能学习平台 (WSIRP)

[![Stars](https://img.shields.io/github/stars/your-team/wsirp?style=social)](https://github.com/your-team/wsirp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Vue](https://img.shields.io/badge/vue-3.x-green.svg)](https://vuejs.org)

## 📖 项目概述

### 项目背景
随着网络安全形势日益严峻，企业对安全人才的需求与日俱增。本平台旨在提供一个全方位的安全学习环境：

1. **行业现状**
   - 安全人才缺口持续扩大
   - 传统学习方式效率低下
   - 理论与实践脱节严重

2. **平台价值**
   - 提供系统化的学习路径
   - 实战与理论相结合
   - AI辅助个性化学习
   - 全面的进度跟踪

### 核心特性
- 🔒 **全面课程**: 覆盖Web安全核心领域
- 🤖 **AI赋能**: 智能学习路径推荐
- ⚡ **实战演练**: 在线靶场与CTF训练
- 📊 **数据分析**: 学习效果可视化
- 🔄 **持续进化**: 自适应学习系统
- 🌐 **内网部署**: 安全可控的学习环境

## 🔥 核心功能模块

### 1. 智能学习中心
- 多维度知识图谱
- 个性化学习路径
- 智能进度追踪
- 学习效果评估
- 知识点关联分析

**技术实现**:
- 前端: Vue3 + TypeScript + Element Plus
- 后端: Python FastAPI
- 数据库: MySQL 8.0
- 缓存: Redis
- 消息队列: RabbitMQ
- 监控: Prometheus + Grafana

### 2. 实战演练平台
- CTF题库系统
- 漏洞复现环境
- 安全工具实训
- 靶场动态部署
- 实时评分反馈

### 3. AI辅助系统
- 学习路径推荐
- 知识点关联分析
- 答疑自动化
- 学习效果预测
- 个性化建议生成

### 4. 进度追踪与评估
- 技能评估体系
- 学习数据分析
- 进度可视化
- 成果认证体系

## 💻 快速开始

### 环境要求
- Python >= 3.8
- Node.js >= 16
- MySQL >= 8.0
- Redis >= 6.0
- Docker >= 20.10

### 本地开发环境搭建

1. **克隆项目**
```bash
git clone https://github.com/your-team/wsirp.git
cd wsirp
```

2. **后端环境配置**
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

3. **前端环境配置**
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

4. **数据库配置**
```bash
# 复制配置文件
cp .env.example .env

# 初始化数据库
python manage.py db:create
python manage.py db:migrate
```

## 🚀 部署指南

### Docker部署
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

### Kubernetes部署
详见 `deploy/kubernetes/` 目录下的配置文件

## 📚 项目文档

### 目录结构
```
├── frontend/                # 前端项目
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   ├── components/     # 通用组件
│   │   └── utils/          # 工具函数
│   └── tests/              # 测试文件
├── backend/                # 后端项目
│   ├── api/               # API接口
│   ├── core/              # 核心功能
│   └── models/            # 数据模型
└── deploy/                # 部署配置
```

### API文档
- 本地开发环境: http://localhost:8000/docs
- 内网环境: http://api.internal.com/docs

## 🤝 参与贡献

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 📞 技术支持

- 项目负责人: [name](mailto:email@example.com)
- 技术支持: [support@internal.com](mailto:support@internal.com)
- 项目文档: http://docs.internal.com

## 📄 开源协议

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情