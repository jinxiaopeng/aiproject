# Web安全智能学习平台 (WSIRP)

[![Stars](https://img.shields.io/github/stars/your-team/wsirp?style=social)](https://github.com/your-team/wsirp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Vue](https://img.shields.io/badge/vue-3.x-green.svg)](https://vuejs.org)

## 📖 项目亮点

- 🤖 **AI驱动学习**: 智能推荐学习路径,自动生成练习题
- 🔒 **全真靶场**: 真实漏洞环境,在线渗透测试
- 📈 **数据分析**: 学习行为分析,进度可视化
- 🚀 **快速部署**: 支持Docker/K8s一键部署
- 🔄 **持续更新**: 定期更新安全知识库

## 📖 功能特性

### 1. 智能学习系统
- 知识图谱自动构建
- 个性化学习路径推荐
- 智能答疑与评测
- 学习进度追踪
- 知识点关联分析

### 2. 实战演练环境
- 漏洞复现靶场
- CTF挑战题库
- 渗透测试工具集
- 安全工具教学
- 实时评分反馈

### 3. AI辅助功能
- GPT驱动的智能问答
- 自动生成练习题
- 代码安全分析
- 学习效果预测
- 个性化建议

## 🛠️ 技术架构

### 前端技术栈
- Vue 3 + TypeScript
- Element Plus UI
- ECharts 数据可视化
- WebSocket 实时通信

### 后端技术栈
- Python FastAPI 
- MySQL 8.0 + Redis
- RabbitMQ 消息队列
- Docker 容器化
- Kubernetes 编排

## 🚀 快速开始

### 环境要求
- Python >= 3.8
- Node.js >= 16
- Docker >= 20.10

### 本地开发

```bash
# 克隆项目
git clone https://github.com/your-team/wsirp.git
cd wsirp

# 后端配置
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 前端配置
npm install
npm run dev

# 启动服务
python manage.py runserver
```

### Docker部署

```bash
# 一键部署
docker-compose up -d
```

## 📚 项目文档

- 接口文档: http://localhost:8000/docs
- 部署文档: http://docs.internal.com/deploy
- 使用手册: http://docs.internal.com/manual

## 🤝 参与贡献

1. Fork 本项目
2. 新建分支 (`git checkout -b feature/xxx`)
3. 提交代码 (`git commit -m 'feat: xxx'`)
4. 推送分支 (`git push origin feature/xxx`)
5. 提交 Pull Request

## 📞 联系我们

- 技术支持: support@wsirp.com
- 项目文档: docs.wsirp.com
- 问题反馈: issues.wsirp.com

## 📄 开源协议

本项目采用 [MIT](LICENSE) 开源协议