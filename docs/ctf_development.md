# CTF靶场训练系统开发维护文档

## 1. 目录结构重构

### 1.1 新的目录结构
```
challenges/
├── web_security/           # Web安全类靶场
│   ├── sql_injection/     
│   ├── xss/
│   └── file_upload/
├── system_security/        # 系统安全类靶场
│   ├── privilege_escalation/
│   └── buffer_overflow/
├── crypto/                 # 密码学类靶场
│   ├── basic_crypto/
│   └── hash_collision/
└── common/                 # 公共组件
    ├── templates/          # 靶场模板
    ├── utils/             # 工具函数
    └── interfaces/        # 接口定义
```

### 1.2 单个靶场结构
```
[challenge_name]/
├── config.json            # 靶场配置
├── README.md             # 靶场说明
├── src/                  # 源代码
│   ├── app.py           # 主程序
│   ├── models/          # 数据模型
│   └── utils/           # 工具函数
├── database/            # 数据库相关
│   ├── init.sql        # 初始化脚本
│   └── data.sql        # 测试数据
└── tests/               # 测试用例
```

### 1.3 后端目录结构
```
backend/
├── core/                    # 核心功能模块
│   ├── process_manager.py   # 进程管理
│   ├── resource_monitor.py  # 资源监控
│   └── log_collector.py     # 日志收集
├── models/                  # 数据模型
│   ├── base.py             # 基础模型
│   ├── user.py             # 用户模型
│   ├── challenge.py        # 靶场模型
│   ├── process.py          # 进程模型
│   └── training.py         # 训练模型
├── routers/                 # API路由
│   ├── auth.py             # 认证路由
│   ├── challenge.py        # 靶场基础API
│   ├── challenge_process.py # 进程管理API
│   └── training.py         # 训练相关API
├── services/               # 业务逻辑
│   ├── auth_service.py     # 认证服务
│   ├── challenge_service.py # 靶场服务
│   └── training_service.py  # 训练服务
├── database/               # 数据库相关
│   ├── init_ctf_tables.sql # 初始化表
│   ├── update_users_table.sql # 用户表更新
│   └── add_training_tables.sql # 训练表
├── utils/                  # 工具函数
│   ├── security.py         # 安全相关
│   └── validators.py       # 数据验证
└── main.py                 # 主程序入口
```

### 1.4 前端目录结构
```
frontend/src/
├── api/                    # API接口
│   ├── auth.ts            # 认证接口
│   ├── challenge.ts       # 靶场基础API
│   ├── process.ts         # 进程管理API
│   └── training.ts        # 训练API
├── components/            # 组件
│   ├── common/           # 公共组件
│   │   ├── Header.vue    # 头部导航
│   │   └── Footer.vue    # 底部信息
│   ├── challenge/        # 靶场组件
│   │   ├── ProcessControl.vue  # 进程控制
│   │   ├── ResourceMonitor.vue # 资源监控
│   │   └── LogViewer.vue       # 日志查看
│   └── training/         # 训练组件
│       ├── StepList.vue   # 步骤列表
│       └── Progress.vue   # 进度展示
├── views/                 # 页面
│   ├── auth/             # 认证页面
│   │   ├── Login.vue     # 登录
│   │   └── Register.vue  # 注册
│   ├── challenge/        # 靶场页面
│   │   ├── List.vue      # 靶场列表
│   │   └── Detail.vue    # 靶场详情
│   └── training/         # 训练页面
│       ├── Session.vue    # 训练会话
│       └── History.vue    # 训练历史
├── store/                # 状态管理
│   ├── auth.ts           # 认证状态
│   ├── challenge.ts      # 靶场状态
│   └── training.ts       # 训练状态
├── utils/                # 工具函数
│   ├── request.ts        # 请求封装
│   └── auth.ts          # 认证工具
├── router/               # 路由配置
│   └── index.ts         # 路由定义
└── App.vue              # 根组件
```

## 2. 数据库改造

### 2.1 Users表更新
- 修改role字段为ENUM类型：'admin', 'teacher', 'student', 'guest'
- 修改status字段为ENUM类型：'active', 'inactive', 'banned', 'pending'
- 添加用户个人信息字段：nickname, avatar_url, bio
- 添加索引优化查询性能

### 2.2 新增靶场相关表
1. user_ctf_profiles（用户靶场档案表）
   - 用户总积分和排名
   - 完成的靶场数量
   - 最后挑战时间

2. challenges（靶场信息表）
   - 基本信息：标题、描述、类别
   - 难度和分值设置
   - 进程和资源配置
   - Flag信息

3. user_skills（用户技能表）
   - 不同类型的技能等级
   - 技能积分统计
   - 技能发展追踪

4. learning_paths（学习路径表）
   - 学习进度跟踪
   - 完成状态记录
   - 学习时间统计

5. submissions（提交记录表）
   - Flag提交历史
   - 得分记录
   - 时间戳记录

## 3. 已完成工作

### 3.1 结构化改造 (2024-01-13)
1. 创建新的目录结构
   - [x] 建立web_security/sql_injection目录
   - [x] 创建标准化的靶场模板
   - [x] 迁移现有SQL注入靶场到新结构

2. 建立靶场模板
   - [x] 创建config.json模板
   - [x] 创建README.md模板
   - [x] 建立标准的目录结构

3. 规范化配置文件
   - [x] 统一配置文件格式
   - [x] 添加详细的配置说明
   - [x] 实现资源限制配置

### 3.2 数据库改造 (2024-01-13)
1. 更新users表结构
   - [x] 修改role和status为ENUM类型
   - [x] 添加用户个人信息字段
   - [x] 添加必要的索引

2. 创建新的靶场相关表
   - [x] 创建user_ctf_profiles表
   - [x] 创建challenges表
   - [x] 创建user_skills表
   - [x] 创建learning_paths表
   - [x] 创建submissions表

3. 建立表间关联
   - [x] 设置外键关系
   - [x] 创建必要的索引
   - [x] 添加级联规则

### 3.3 文档维护 (2024-01-13)
1. 创建开发维护文档
   - [x] 记录目录结构
   - [x] 说明数据库设计
   - [x] 制定开发计划

### 3.4 模块化重构 (2024-01-14)
1. 后端核心模块
   - [x] 进程管理模块 (ProcessManager)
   - [x] 资源监控模块 (ResourceMonitor)
   - [x] 日志收集模块 (LogCollector)

2. 后端服务层
   - [x] 训练服务 (TrainingService)
   - [x] 进程管理API
   - [x] 训练API路由

3. 前端接口层
   - [x] 进程管理接口
   - [x] 训练接口
   - [x] 类型定义

4. 数据模型
   - [x] Training模型
   - [x] TrainingStep模型
   - [x] Process模型

## 4. 待完成工作

### 4.1 第一阶段：基础设施
1. 进程管理系统实现
   - [ ] 进程创建和管理
   - [ ] 资源限制控制
   - [ ] 进程监控和日志

2. 基础API开发
   - [ ] 靶场管理接口
   - [ ] 用户进度接口
   - [ ] 评分系统接口

### 4.2 第二阶段：功能开发
1. 靶场管理功能
   - [ ] 靶场创建和部署
   - [ ] 靶场状态监控
   - [ ] 资源使用统计

2. 学习追踪系统
   - [ ] 进度记录
   - [ ] 技能评估
   - [ ] 学习路径推荐

### 4.3 第三阶段：优化升级
1. 交互式学习
   - [ ] 实时引导系统
   - [ ] 动态提示机制
   - [ ] 可视化反馈

2. 性能优化
   - [ ] 数据库查询优化
   - [ ] 进程管理优化
   - [ ] 资源使用优化

## 5. 维护指南

### 5.1 添加新靶场
1. 使用模板创建目录结构
2. 配置config.json
3. 编写README.md
4. 实现核心功能
5. 添加测试用例

### 5.2 数据库维护
1. 定期备份数据
2. 监控表大小
3. 优化查询性能
4. 清理过期数据

### 5.3 系统监控
1. 进程状态监控
2. 资源使用监控
3. 用户活动监控
4. 错误日志监控

## 6. 注意事项

### 6.1 安全性
- 严格控制进程权限
- 定期更新依赖
- 监控异常行为
- 保护敏感数据

### 6.2 可扩展性
- 遵循模块化设计
- 保持接口统一
- 文档及时更新
- 代码规范统一 