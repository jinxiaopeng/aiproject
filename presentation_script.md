# 信息安全智能学习平台演示讲稿

各位评委老师好，我是成员A，是本次项目的技术工程师，负责网站的搭建和项目的启动。首先，我将为大家启动本次的项目。

## 一、项目架构介绍

我们的项目采用了现代化的前后端分离架构：

1. 后端技术栈：
   - Python FastAPI 框架
   - SQLAlchemy ORM
   - JWT认证机制
   - MySQL数据库

2. 前端技术栈：
   - Vue 3 框架
   - TypeScript 语言
   - Element Plus UI组件库
   - Axios 请求库

## 二、项目启动步骤

1. 首先，让我为大家展示项目的核心目录结构：
   - `backend/`: 后端服务代码，包含API接口和业务逻辑
   - `frontend/`: 前端界面代码，提供用户交互界面
   - `challenges/`: CTF靶场挑战题目
   - `docker/`: 容器化配置文件
   - `config/`: 系统配置文件

2. 现在，我们开始启动项目：
   - 第一步：启动后端服务
     ```bash
     uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
     ```
   - 第二步：启动前端服务
     ```bash
     cd frontend
     npm run dev
     ```
   - 第三步：访问靶场训练页面
     - http://localhost:3017/challenge 或
     - http://localhost:3017/practice （别名）

## 三、核心功能演示

1. 用户系统功能：
   - 演示用户注册流程
   - 展示JWT token认证机制
   - 演示用户权限管理
   - 展示用户画像功能

2. 学习平台功能：
   - 展示个性化学习路径
   - 演示进度追踪系统
   - 展示成就系统
   - 演示知识图谱

3. CTF靶场系统：
   - 演示靶场环境部署
   - 展示题目难度分级
   - 演示实时评分系统
   - 展示答题反馈机制

4. 安全防护措施：
   - 展示密码加密存储
   - 演示Docker容器隔离
   - 展示防注入措施
   - 演示访问控制机制

5. 核心组件功能
   - 终端模拟器（ChallengeTerminal）：
     - 界面特性：
       - 仿真终端标题栏
       - 最小化/最大化控制
       - 全屏模式支持
     - 交互功能：
       - 命令历史记录
       - 上下键导航历史
       - Tab自动补全
       - 实时命令执行
     - 状态显示：
       - 连接状态指示
       - 运行时间统计
       - 多种输出类型（命令/错误/成功）
   
   - Flag提交组件（FlagSubmit）：
     - 输入验证：
       - 空值检查
       - 格式验证
     - 提交功能：
       - 异步提交处理
       - 加载状态显示
       - 成功/失败反馈
     - 界面设计：
       - 暗色主题适配
       - 响应式布局
       - 用户友好提示
   
   - 讨论面板（DiscussionPanel）：
     - 评论功能：
       - 发表主评论
       - 回复评论
       - Markdown格式支持
     - 互动特性：
       - 点赞功能
       - 作者标识
       - 时间显示
     - 界面组织：
       - 分页加载
       - 嵌套回复展示
       - 实时更新

## 四、项目特色与创新点

1. 智能化学习：
   - 基于用户画像的个性化推荐
   - AI辅助的学习路径规划
   - 实时进度追踪和反馈

2. 安全性保障：
   - 完整的用户认证体系
   - 严格的环境隔离机制
   - 多层次的安全防护

3. 实用性设计：
   - 模块化的系统架构
   - 友好的用户界面
   - 完善的文档支持

## 五、总结

以上就是我们信息安全智能学习平台的主要功能演示。我们的平台通过现代化的技术架构、智能化的学习体系和严格的安全防护，为用户提供了一个全面的信息安全学习环境。感谢各位评委老师的聆听！

## 六、靶场训练演示

1. 进入靶场训练界面
   - 顶部统计卡片展示：
     - 总训练数（TrophyBase图标）
     - 已完成数（StarFilled图标）
     - 进行中数量（Timer图标）
     - 总积分（Medal图标）
   
   - 主要内容区域：
     - 左侧面板：
       - 搜索功能：支持靶场名称搜索
       - 分类过滤：多个分类标签选择
       - 难度过滤：不同难度等级筛选
       - 状态过滤：完成状态筛选
       - 进度概览：图形化展示完成情况
     
     - 右侧面板：
       - 靶场列表标题
       - 靶场数量统计
       - 视图切换：网格/列表模式
       - 靶场卡片展示

2. 靶场卡片功能
   - 卡片头部：
     - 难度等级标识（不同颜色）
     - 积分显示（pts）
     - 分类标签
   - 卡片内容：
     - 靶场标题
     - 简要描述
     - 技能标签
   - 卡片底部：
     - 完成进度条
     - 状态指示器
     - 操作按钮（开始/继续）
   - 交互功能：
     - 状态变更通知
     - 完成事件处理
     - 统计数据更新

3. SQL注入靶场演示
   - 点击进入靶场详情页面，包含：
     - 目信息标签页：
       - 详细描述：一个存在SQL注入漏洞的登录系统
       - 前置知识：SQL基础语法、注入原理
       - 推荐工具：浏览器开发者工具、Burp Suite
     - WriteUp标签页（完成后解锁）
     - 解题记录标签页
   
   - 具体解题步骤：
     1. 环境准备：
        - 启动靶场容器
        - 访问登录页面：http://localhost:8081
        - 查看页面源码，找到登录表单

     2. 漏洞分析：
        - 定位注入点：登录表单的username和password字段
        - 分析后端代码：直接拼接SQL语句，存在注入风险
        ```python
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        ```

     3. 注入尝试：
        - 尝试万能密码：
          ```sql
          username: admin' --
          password: anything
          ```
        - 或者使用：
          ```sql
          username: admin' OR '1'='1
          password: anything
          ```

     4. 获取数据：
        - 成功登录后，尝试获取更多信息
        - 查找flag表：
          ```sql
          username: admin' UNION SELECT * FROM flag; --
          password: anything
          ```
        - 获取flag：flag{sql_1nj3ct10n_m4st3r_2023}

     5. 漏洞修复建议
        - 使用参数化查询
        - 过滤特殊字符
        - 限制查询权限
        - 加强输入验证

4. 实验环境操作
   - 靶场控制面板：
     - 启动靶场按钮（调用start_process接口）
     - 停止靶场按钮（调用stop_process接口）
     - 重启靶场按钮（调用restart_process接口）
     - 状态查询（调用status接口）
   - 实验环境管理：
     - 基于Docker容器化部署
     - 支持多种靶场类型：
       - SQL注入（sql-injection）
       - XSS跨站脚本（xss）
       - 文件上传漏洞（file-upload）
       - Linux提权（linux-priv）
     - 自动环境管理：
       - 配置文件加载
       - 进程状态监控
       - 日志实时收集
       - 环境自动清理
   - 日志查看功能：
     - 实时日志输出
     - 历史日志查询
     - 错误日志记录
     - 行状态监控

5. 学习反馈系统
   - 靶场详情展示：
     - 基本信息：
       - 靶场标题和描述
       - 难度等级标签
       - 分类标签
       - 积分显示
     - 学习内容：
       - 靶场描述
       - 学习目标列表
       - 训练环境信息
       - 训练步骤指导
     - 提示系统：
       - 分级提示解锁
       - 积分消耗机制
       - 帮助文档链接
   
   - 每日挑战系统：
     - 状态展示：
       - 连续打卡天数
       - 总积分统计
       - 完成率统计
     - 挑战内容：
       - 题目描述（Markdown格式）
       - 分级提示系统
       - 答案提交功能
     - 社区互动：
       - 讨论区功能
       - 评论发表
       - 解题分享
   
   - 进度追踪：
     - 解题用时统计
     - 完成度记录
     - 得分统计
   - 后续推荐：
     - 相关题目推荐
     - 进阶学习路径
     - 技能提升建议