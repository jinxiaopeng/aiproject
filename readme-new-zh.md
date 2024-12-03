# 信息安全智能学习平台

[![Stars](https://img.shields.io/github/stars/your-team/wsirp?style=social)](https://github.com/your-team/wsirp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Vue](https://img.shields.io/badge/vue-3.x-green.svg)](https://vuejs.org)

## 📖 创新亮点

### 原始技术创新
- **智能知识图谱构建**
  - 自研知识点关联算法
  - 动态更新的知识体系
  - 多维度知识映射技术
  - 自适应学习路径生成

- **靶场自动化技术**
  - 漏洞环境一键部署
  - 动态漏洞模拟引擎
  - 攻防场景实时构建
  - 自动化评测系统

- **AI辅助教学系统**
  - 深度学习模型训练
  - 智能题目生成引擎
  - 学习行为分析模型
  - 个性化推荐算法

### 职业导向创新
- **岗位能力画像**
  - 安全工程师技能模型
  - 渗透测试专家路径
  - 安全研发工程师图谱
  - 安全运维工程师技能树

- **企业实战对接**
  - 真实漏洞场景复现
  - 企业级安全工具实训
  - 红蓝对抗实战演练
  - 应急响应流程模拟

## 📖 项目概述

### 项目背景
随着网络安全形势日益严峻，企业对安全人才的需求与日俱增。本平台针对演示场景和日常使用场景进行了特别优化，既能保证演示时的流畅性和稳定性，又能在日常使用时提供完整的学习体验。

### 使用场景
- **演示场景**（离线环境）
  - 预加载核心资源
  - 本地靶场环境
  - 轻量级AI模型
  - 快速启动部署
  - 完全离线运行

- **日常使用**（在线环境）
  - 完整功能支持
  - 在线资源更新
  - 云端AI训练
  - 实时互动交流
  - 持续更新维护

## 🔥 环境要求

### 系统要求
- Windows 10/11
- 8GB以上内存
- 50GB可用磁盘空间
- 支持在线/离线环境

### 预置软件
- Python 3.8+
- Node.js 16+
- Docker Desktop for Windows
- Git for Windows（可选）

## 🚀 快速部署

### Windows环境准备
```powershell
# 1. 安装Docker Desktop for Windows
# 下载地址：https://www.docker.com/products/docker-desktop

# 2. 启用Hyper-V（以管理员身份运行PowerShell）
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All

# 3. 启动Docker服务
net start com.docker.service
```

### 离线部署步骤
```powershell
# 1. 解压离线资源包到指定目录
# wsirp-offline.zip → C:\wsirp

# 2. 进入项目目录
cd C:\wsirp

# 3. 检查环境
.\scripts\check-env.bat

# 4. 初始化数据库
.\scripts\init-db.bat

# 5. 启动服务
.\scripts\start-all.bat
```

## 📂 项目目录结构

```
G:\aiproject\                # 项目根目录
├── frontend\                # 前端项目
│   ├── public\             # 静态资源
│   ├── src\                # 源代码
│   │   ├── assets\        # 资源文件
│   │   ├── components\    # 组件
│   │   ├── views\         # 页面
│   │   ├── router\        # 路由
│   │   ├── store\         # 状态管理
│   │   └── utils\         # 工具函数
│   ├── package.json       # 依赖配置
│   └── vite.config.js     # Vite配置
│
├── backend\                # 后端项目
│   ├── api\               # API接口
│   ├── core\              # 核心功能
│   │   ├── ai\           # AI模型
│   │   ├── lab\          # 靶场逻辑
│   │   └── auth\         # 认证授权
│   ├── models\           # 数据模型
│   └── utils\            # 工具函数
│
├── config\                # 配置文件
│   ├── database.ini      # 数据库配置
│   └── app.ini           # 应用配置
│
├── data\                  # 数据目录
│   ├── mysql\            # MySQL数据
│   ├── redis\            # Redis数据
│   └── models\           # AI模型文件
│
├── scripts\              # 脚本文件
│   ├── deploy\          # 部署脚本
│   ├── backup\          # 备份脚本
│   └── utils\           # 工具脚本
│
├── docs\                 # 文档
│   ├── images\          # 文档图片
│   ├── api\             # API文档
│   └── guide\           # 使用指南
│
├── logs\                 # 日志文件
│   ├── app\             # 应用日志
│   ├── access\          # 访问日志
│   └── error\           # 错误日志
│
├── tests\               # 测试文件
│   ├── frontend\        # 前端测试
│   └── backend\         # 后端测试
│
├── docker\              # Docker相关
│   ├── frontend\        # 前端Docker
│   └── backend\         # 后端Docker
│
├── .gitignore           # Git忽略文件
├── README.md            # 项目说明
├── docker-compose.yml   # Docker编排
└── requirements.txt     # Python依赖
```

### 目录说明

1. **frontend/**: 前端项目目录
   - 使用Vue 3 + TypeScript开发
   - 包含所有前端源代码和资源

2. **backend/**: 后端项目目录
   - Python FastAPI开发
   - 包含API接口和核心业务逻辑

3. **config/**: 配置文件目录
   - 数据库连接配置
   - 应用全局配置

4. **data/**: 数据存储目录
   - 数据库文件
   - AI模型文件
   - 缓存数据

5. **scripts/**: 脚本工具目录
   - 部署脚本
   - 备份脚本
   - 维护工具

6. **docs/**: 文档目录
   - 项目文档
   - API文档
   - 使用指南

7. **logs/**: 日志目录
   - 应用运行日志
   - 访问日志
   - 错误日志

8. **tests/**: 测试目录
   - 单元测试
   - 集成测试

9. **docker/**: Docker配置目录
   - Docker配置文件
   - 容器编排配置

## 📚 使用指南

### 服务访问
```
# Web应用
http://localhost:8080

# 靶场环境
http://localhost:8081

# CTF平台
http://localhost:8082
```

### 默认账号
```
# 管理员账号
用户名: admin
密码: admin123

# 数据库账号
MySQL:
- 主机: localhost
- 端口: 3306
- 数据库: wsirp_db
- 用户名: root
- 密码: jxp1210

Redis:
- 主机: localhost
- 端口: 6379
```

### 配置文件
```ini
# config/database.ini
[mysql]
host = localhost
port = 3306
database = wsirp_db
user = root
password = jxp1210

[redis]
host = localhost
port = 6379
```

## ❓ 常见问题

### 部署相关
Q: Docker服务无法启动？
A: 检查以下几点：
1. 确保已启用Hyper-V
2. 以管理员身份运行Docker Desktop
3. 检查系统虚拟化是否开启

Q: 端口被占用？
A: 可以在配置文件中修改端口：
1. Web应用：config/app.ini中的port
2. 数据库：config/database.ini中的port

Q: 数据库连接失败？
A: 检查以下配置：
1. MySQL服务是否启动
2. 账号密码是否正确
3. 数据库是否已创建

### 使用相关
Q: 如何备份数据？
A: 执行脚本：
```powershell
.\scripts\backup-data.bat
```

Q: 如何更新离线资源？
A: 复制新的资源文件到data目录下，重启服务即可。

## 🗺️ 项目路线图

### 当前版本
- 版本号：v0.9.0
- 发布日期：2024.01
- 主要特性：离线演示支持

### 后续规划
- v1.0.0：完整版发布
- v1.1.0：在线功能增强
- v1.2.0：企业版支持

## 📞 联系我们

- 技术支持: support@internal.com
- 问题反馈: issues.internal.com
- 项目文档: docs.internal.com

## 📄 开源协议

本项目采用 [MIT](LICENSE) 开源协议

## 📸 功能展示

### 平台预览
![平台首页](docs/images/homepage.png)
![靶场系统](docs/images/lab.png)
![学习中心](docs/images/learning.png)

### 演示视频
- [平台功能介绍](https://example.com/demo-video)
- [快速部署指南](https://example.com/deploy-guide)
- [使用教程](https://example.com/tutorial)

## 📦 详细安装步骤

### 1. 基础环境配置
```powershell
# 1. 安装Python 3.8+
# 下载地址：https://www.python.org/downloads/
# 安装时勾选"Add Python to PATH"

# 2. 安装Node.js 16+
# 下载地址：https://nodejs.org/
# 选择LTS版本

# 3. 安装Docker Desktop
# 下载地址：https://www.docker.com/products/docker-desktop
```

### 2. 系统配置
```powershell
# 1. 启用Windows功能
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 2. 配置Docker资源
# 打开Docker Desktop → Settings → Resources
# - Memory: 4GB
# - Swap: 1GB
# - CPU: 2
```

### 3. 数据库配置
```powershell
# 1. 初始化MySQL
.\scripts\init-mysql.bat

# 2. 导入基础数据
.\scripts\import-data.bat

# 3. 配置Redis
.\scripts\setup-redis.bat
```

### 4. 安全配置
```powershell
# 1. 配置防火墙规则
.\scripts\setup-firewall.bat

# 2. 设置访问控制
.\scripts\setup-acl.bat

# 3. 启用SSL
.\scripts\enable-ssl.bat
```

## 📊 性能指标

### 系统要求
- CPU利用率: <30%
- 内存占用: <4GB
- 磁盘空间: 50GB
- 网络带宽: 10Mbps（在线模式）

### 并发支持
- 单机支持: 50用户同时在线
- 靶场环境: 20个并发实例
- 响应时间: <500ms

### 资源消耗
- Docker容器: 5-8个
- 数据库大小: <2GB
- 日志空间: <1GB/周

## 🔒 安全建议

### 系统加固
1. 定期更新系统补丁
2. 配置防火墙规则
3. 启用访问控制
4. 监控异常行为

### 数据安全
1. 定期备份数据
```powershell
# 自动备份脚本
.\scripts\backup.bat --auto
```

2. 加密敏感信息
3. 控制访问权限
4. 审计日志记录

### 运行监控
1. 查看系统状态
```powershell
# 检查服务状态
.\scripts\check-status.bat

# 查看日志
.\scripts\view-logs.bat
```

2. 性能监控
```powershell
# 资源使用监控
.\scripts\monitor.bat
```

## 📋 更新日志

### v0.9.0 (2024-01)
- 支持完全离线部署
- 优化AI模型性能
- 增加基础靶场环境
- 完善部署脚本

### v0.8.0 (2023-12)
- 初始版本发布
- 基础功能实现
- 核心模块开发

## 🎮 快速演示指南

### 演示前准备
1. **环境检查**
   ```powershell
   # 检查基础环境
   .\scripts\check-env.bat
   
   # 验证数据库状态
   .\scripts\verify-db.bat
   ```

2. **资源准备**
   - 确保离线资源包已解压
   - 检查示例数据已导入
   - 验证靶场环境就绪

3. **演示账号**
   ```
   管理员账号: admin
   密码: admin123
   演示用户: demo
   密码: demo123
   ```

### 演示流程

1. **平台概览** (5分钟)
   - 系统登录
   - 功能模块介绍
   - 整体架构说明

2. **核心功能** (15分钟)
   - Web安全学习模块
   - 靶场环境演示
   - AI辅助功能展示
   - 学习追踪系统

3. **实战演练** (10分钟)
   - SQL注入靶场
   - XSS攻防演示
   - 漏洞扫描实战
   - 应急响应模拟

4. **AI特性** (5分钟)
   - 智能学习路径
   - 自动题目生成
   - 个性化推荐
   - 学习效果分析

### 演示要点

1. **离线特性**
   - 完全离线运行
   - 本地资源加载
   - 实时响应速度
   - 稳定性保障

2. **创新亮点**
   - AI辅助学习
   - 自适应路径
   - 实战靶场
   - 全流程追踪

3. **实用价值**
   - 企业实战对接
   - 岗位能力提升
   - 快速部署使用
   - 持续更新维护

### 常见演示问题

1. **环境问题**
   ```powershell
   # 重置演示环境
   .\scripts\reset-demo.bat
   
   # 清理缓存数据
   .\scripts\clean-cache.bat
   ```

2. **功能问题**
   ```powershell
   # 检查服务状态
   .\scripts\check-services.bat
   
   # 重启特定服务
   .\scripts\restart-service.bat [service_name]
   ```

3. **数据问题**
   ```powershell
   # 重置演示数据
   .\scripts\reset-data.bat
   
   # 备份当前数据
   .\scripts\backup-demo.bat
   ```

### 应急处理

1. **快速恢复**
   ```powershell
   # 一键恢复环境
   .\scripts\quick-recovery.bat
   ```

2. **备用方案**
   - 准备备用环境
   - 使用备份数据
   - 切换演示场景

3. **技术支持**
   - 现场支持人员联系方式
   - 远程协助准备
   - 应急预案说明

## 📝 演示清单

### 环境检查
- [ ] 系统环境就绪
- [ ] 数据库连接正常
- [ ] 靶场环境可用
- [ ] AI模型加载完成

### 功能验证
- [ ] 用户登录正常
- [ ] 靶场访问正常
- [ ] AI功能响应及时
- [ ] 数据保存正常

### 资源确认
- [ ] 示例数据完整
- [ ] 演示账号可用
- [ ] 文档资料就绪
- [ ] 备用方案准备
