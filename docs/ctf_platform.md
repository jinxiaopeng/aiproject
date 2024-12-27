# CTF 靶场训练平台设计文档

## 1. 系统架构

### 1.1 技术栈
- 前端：Vue3 + Element Plus
- 后端：Python FastAPI
- 数据库：MySQL
- 进程管理：Python multiprocessing

### 1.2 数据库配置
```bash
Host: localhost
Database: aiproject
Username: root
Password: jxp1210
Character Set: utf8mb4
```

## 2. 数据库设计

### 2.1 数据库表结构
```sql
-- 复用现有users表
-- 用户靶场档案表
CREATE TABLE IF NOT EXISTS user_ctf_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,           -- 关联到users表的外键
    points INT DEFAULT 0,                  -- 总积分
    rank INT DEFAULT 0,                    -- 排名
    last_challenge_time TIMESTAMP NULL,    -- 最后挑战时间
    completed_challenges INT DEFAULT 0,     -- 完成的靶场数
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 靶场表
CREATE TABLE IF NOT EXISTS challenges (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    difficulty ENUM('easy', 'medium', 'hard') NOT NULL,
    points INT NOT NULL DEFAULT 0,
    flag VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 用户技能表
CREATE TABLE IF NOT EXISTS user_skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    skill_type VARCHAR(50) NOT NULL,      -- 技能类型(web/system/crypto)
    skill_level INT DEFAULT 0,            -- 技能等级
    skill_points INT DEFAULT 0,           -- 技能积分
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 学习路径表
CREATE TABLE IF NOT EXISTS learning_paths (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    challenge_id INT NOT NULL,
    status ENUM('not_started','in_progress','completed') DEFAULT 'not_started',
    start_time TIMESTAMP NULL,
    complete_time TIMESTAMP NULL,
    attempts INT DEFAULT 0,
    hints_used INT DEFAULT 0,
    score INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (challenge_id) REFERENCES challenges(id)
);

-- 提交记录表
CREATE TABLE IF NOT EXISTS submissions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    challenge_id INT NOT NULL,
    submitted_flag VARCHAR(255) NOT NULL,
    is_correct BOOLEAN NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (challenge_id) REFERENCES challenges(id)
);
```

## 3. 功能模块

### 3.1 基础功能
1. 用户系统（复用现有）
   - 登录注册
   - 权限管理
   - 用户信息管理

2. 靶场管理
   - 分类展示
   - 难度分级（简单、中等、困难）
   - 积分系统
   - 进度管理
   - 排行榜

### 3.2 创新功能
1. 交互式学习
   - 实时引导系统
   - 可视化攻击效果
   - 即时操作反馈
   - 动态提示

2. 智能学习系统
   - 个性化学习路径
   - 智能提示机制
   - 知识点关联
   - 学习建议

3. 技能进度
   - 技能雷达图
   - 学习统计
   - 自动报告生成
   - 成就系统

## 4. 靶场内容

### 4.1 靶场分类
1. Web安全
   - SQL注入
   - XSS攻击
   - 文件上传漏洞
   - CSRF攻击
   - 命令注入

2. 系统安全
   - 权限提升
   - 缓冲区溢出
   - 内存漏洞
   - 系统漏洞利用

3. 密码学
   - 基础加密
   - 高级加密
   - 哈希碰撞
   - 密码破解

### 4.2 单个靶场结构
1. 基础信息
   - 描述说明
   - 难度等级
   - 分值设置
   - 预计完成时间

2. 学习资源
   - 相关知识点
   - 参考资料
   - 提示信息
   - 解题思路

3. 实验环境
   - 本地进程管理
   - 资源使用限制
   - 环境隔离
   - 状态监控

4. 验证系统
   - 阶段性检查点
   - Flag验证
   - 完成度评估
   - 解题报告

## 5. 系统特点

1. 完整性
   - 复用现有认证系统
   - 完整的学习追踪
   - 全面的技能评估

2. 创新性
   - 交互式学习体验
   - 智能提示系统
   - 可视化进度展示

3. 实用性
   - 模块化设计
   - 个性化学习路径
   - 即时反馈机制

4. 扩展性
   - 易于添加新靶场
   - 支持多种类型题目
   - 灵活的评分机制 

## 6. 系统改造计划

### 6.1 改动范围

1. 前端改动
   - 复用现有登录认证系统
   - 新增靶场相关页面和组件
   - 新增技能雷达图等可视化组件
   - 新增实时交互功能

2. 后端改动
   - 复用现有认证API
   - 新增靶场相关API
   - 修改环境管理(从Docker改为进程)
   - 新增学习路径和提示系统

3. 数据库改动
   - 保持现有users表不变
   - 新增靶场相关表：
     * user_ctf_profiles (用户靶场档案)
     * challenges (靶场信息)
     * user_skills (用户技能)
     * learning_paths (学习路径)
     * submissions (提交记录)

### 6.2 改造步骤

1. 第一阶段：基础设施改造
   - 创建新的数据库表
   - 实现进程管理系统
   - 开发基础API接口

2. 第二阶段：功能开发
   - 实现靶场管理功能
   - 开发进度追踪系统
   - 完成Flag验证机制

3. 第三阶段：创新功能
   - 开发交互式学习系统
   - 实现智能提示机制
   - 添加可视化组件

### 6.3 具体任务

1. 必须改动
   - 环境管理系统
     * Docker改为进程
     * 资源控制逻辑
   - 数据库
     * 新增5个表
     * 数据关联逻辑
   - API接口
     * 靶场管理API
     * 进度追踪API

2. 新增功能
   - 前端页面
     * 靶场列表
     * 靶场详情
     * 进度展示
   - 交互系统
     * 实时引导
     * 可视化效果
   - 智能系统
     * 学习路径
     * 提示机制

### 6.4 开发优先级

1. 第一优先级
   - 数据库表创建和关联
   - 进程管理系统实现
   - 基础API开发

2. 第二优先级
   - 靶场管理功能
   - 用户进度追踪
   - 前端基础页面

3. 第三优先级
   - 交互式学习功能
   - 智能提示系统
   - 可视化组件

### 6.5 注意事项

1. 兼容性
   - 保持与现有系统的兼容
   - 确保数据迁移平滑
   - 维护API接口稳定

2. 性能
   - 优化进程管理
   - 控制资源使用
   - 提高响应速度

3. 安全性
   - 进程隔离
   - 资源限制
   - 权限L