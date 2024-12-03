# 信息安全智能学习平台

## 项目概述
本项目是一个信息安全智能学习平台，旨在为用户提供网络安全学习和实践的环境。项目包括前端和后端部分，支持在线和离线使用。

## 目录结构
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

## 各部分功能说明

### frontend/
- **public/**: 存放静态资源，如 HTML 文件、图标和其他公共文件。
- **src/**: 源代码目录，包含前端应用的所有代码。
  - **assets/**: 存放图片、样式等资源文件。
  - **components/**: Vue 组件，构建应用的 UI。
  - **views/**: 页面视图，定义应用的不同页面。
  - **router/**: 路由配置，管理页面导航。
  - **store/**: 状态管理，使用 Vuex 管理应用状态。
  - **utils/**: 工具函数，提供通用功能。
- **package.json**: 前端项目的依赖配置文件，列出所有依赖包。
- **vite.config.js**: Vite 的配置文件，定义构建和开发设置。

### backend/
- **api/**: 存放 API 接口的实现，处理前端请求。
- **core/**: 核心功能模块，包含主要业务逻辑。
  - **ai/**: AI 模型相关代码。
  - **lab/**: 靶场逻辑，处理靶场相关功能。
  - **auth/**: 认证和授权功能。
- **models/**: 数据模型定义，描述数据库结构。
- **utils/**: 工具函数，提供后端通用功能。

### config/
- **database.ini**: 数据库配置文件，定义数据库连接信息。
- **app.ini**: 应用配置文件，定义应用的全局设置。

### data/
- **mysql/**: 存放 MySQL 数据文件。
- **redis/**: 存放 Redis 数据文件。
- **models/**: 存放 AI 模型文件。

### scripts/
- **deploy/**: 部署脚本，自动化部署过程。
- **backup/**: 备份脚本，定期备份数据。
- **utils/**: 其他工具脚本。

### docs/
- **images/**: 存放文档中使用的图片。
- **api/**: API 文档，描述 API 接口的使用。
- **guide/**: 使用指南，帮助用户理解如何使用平台。

### logs/
- **app/**: 应用日志，记录应用运行时的日志信息。
- **access/**: 访问日志，记录用户访问情况。
- **error/**: 错误日志，记录应用错误信息。

### tests/
- **frontend/**: 前端测试文件，确保前端功能正常。
- **backend/**: 后端测试文件，确保后端功能正常。

### docker/
- **frontend/**: 前端 Docker 配置，定义前端容器。
- **backend/**: 后端 Docker 配置，定义后端容器。

### 维护建议
- 定期检查和更新文档，以确保其反映项目的最新状态。
- 在代码中添加必要的注释，以便其他开发者理解代码逻辑。
- 确保测试目录中的测试用例覆盖了主要功能，保持代码质量。
- 定期检查和清理日志文件，确保日志记录的有效性。

## 贡献
欢迎任何形式的贡献！请遵循以下步骤：
1. Fork 本项目
2. 创建你的特性分支 (`git checkout -b feature/YourFeature`)
3. 提交你的更改 (`git commit -m 'Add some feature'`)
4. 推送到分支 (`git push origin feature/YourFeature`)
5. 创建一个新的 Pull Request

## 许可证
本项目采用 [MIT](LICENSE) 开源协议。

## 联系我们
如有任何问题或建议，请联系 [你的名字或邮箱]。
