# Web安全智能学习平台迁移指南

## 1. 环境要求

### 必需环境
- Python 3.8 或更高版本
- Node.js 16.x 或更高版本
- Docker Desktop（如果需要使用容器化功能）
- Git（可选，用于版本控制）

### 系统要求
- Windows 10/11 操作系统
- 至少 4GB 可用内存
- 至少 10GB 可用磁盘空间

## 2. 前置准备

1. **安装 Python**
   - 访问 [Python官网](https://www.python.org/downloads/) 下载并安装 Python
   - 安装时勾选 "Add Python to PATH"
   - 验证安装：打开命令提示符，运行 `python --version`

2. **安装 Node.js**
   - 访问 [Node.js官网](https://nodejs.org/) 下载并安装 Node.js
   - 验证安装：打开命令提示符，运行 `node --version` 和 `npm --version`

3. **安装 Docker Desktop**（如需使用容器化功能）
   - 访问 [Docker官网](https://www.docker.com/products/docker-desktop/) 下载并安装 Docker Desktop
   - 安装完成后启动 Docker Desktop
   - 验证安装：打开命令提示符，运行 `docker --version`

## 3. 项目迁移步骤

### 3.1 复制项目文件

1. 将整个项目文件夹复制到电脑的目标位置，确保包含以下关键文件和目录：
   ```
   - backend/
   - frontend/
   - docker/
   - requirements.txt
   - package.json
   - start.bat
   - init_all.bat
   - init_platform.sql
   ```

### 3.2 后端环境配置

1. **初始化Python环境**
   - 打开命令提示符，进入项目根目录
   - 运行 `init_all.bat`
   - 或者手动执行以下步骤：
     ```bash
     python -m venv venv
     venv\Scripts\activate
     pip install -r requirements.txt
     ```

2. **数据库迁移和初始化**
   - 如果原项目中有 `sql_app.db` 文件：
     - 确保已将 `sql_app.db` 文件复制到新环境的项目根目录
     - 如果登录失败，可能需要重新初始化数据库
   
   - 重新初始化数据库：
     - 删除现有的 `sql_app.db` 文件（如果存在）
     - 在项目根目录下运行：
       ```bash
       python scripts/init_db.py
       ```
     - 如果上述命令失败，可以手动执行SQL初始化：
       ```bash
       sqlite3 sql_app.db < init_platform.sql
       ```
     - 确保数据库中至少有一个可用的测试账号，如果没有，可以通过API接口注册新用户

3. **验证数据库**
   - 检查 `sql_app.db` 文件是否存在
   - 尝试使用测试账号登录系统
   - 如果登录失败，检查数据库中是否有用户数据：
     ```bash
     sqlite3 sql_app.db
     .tables
     SELECT * FROM users;
     .quit
     ```

### 3.3 前端环境配置

1. **安装前端依赖**
   ```bash
   cd frontend
   npm install
   ```

### 3.4 Docker配置（如需使用）

1. 确保 Docker Desktop 正在运行
2. 在项目根目录下执行：
   ```bash
   docker-compose -f docker/docker-compose.yml build
   ```

## 4. 启动项目

1. **启动后端服务**
   - 使用 `start.bat`
   - 或手动执行：
     ```bash
     cd backend
     python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
     ```

2. **启动前端服务**
   ```bash
   cd frontend
   npm run dev
   ```

## 5. 验证部署

1. 访问以下URL确认服务是否正常运行：
   - 后端API：http://localhost:8000/docs
   - 前端页面：http://localhost:5173

## 6. 常见问题解决

1. **Python依赖安装失败**
   - 确保pip已更新到最新版本：`python -m pip install --upgrade pip`
   - 尝试使用国内镜像源：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

2. **Node.js依赖安装失败**
   - 清除npm缓存：`npm cache clean --force`
   - 使用国内镜像源：`npm config set registry https://registry.npmmirror.com`
   - 重新安装：`npm install`

3. **数据库初始化失败**
   - 检查数据库配置文件
   - 确保没有其他程序占用相关端口
   - 手动执行 `init_platform.sql` 脚本

4. **Docker相关问题**
   - 确保Docker Desktop已正常启动
   - 检查Docker服务状态：`docker info`
   - 如遇到权限问题，以管理员身份运行命令提示符

## 7. 注意事项

1. 确保所有配置文件都已正确迁移
2. 保持原有的目录结构不变
3. 不要删除任何看似无用的文件，除非确认其用途
4. 建议在迁移前备份整个项目
5. 如果使用了自定义的环境变量，确保在新环境中也设置好

## 8. 技术支持

如遇到问题，请参考：
1. 项目文档：`docs/` 目录
2. README文件：`README.md`，`readme-zh.md`
3. 完整项目说明：`complete_project_readme.md` 