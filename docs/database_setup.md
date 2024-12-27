# CTF靶场训练系统数据库设计文档

## 1. 数据库架构

### 1.1 系统主数据库 (aiproject)
用于存储系统核心数据,包括用户信息、靶场配置、学习进度等。

```sql
Host: localhost
Database: aiproject
Username: root
Password: jxp1210
Character Set: utf8mb4
```

#### 核心表结构:
1. users - 用户表(已有)
2. user_ctf_profiles - 用户靶场档案表
3. challenges - 靶场基本信息表
4. user_skills - 用户技能表
5. learning_paths - 学习路径表
6. submissions - 提交记录表

### 1.2 靶场训练数据库
每个靶场使用独立的数据库,用于存储训练过程中的数据。

#### SQL注入靶场 (ctf_challenge_1)
```sql
Database: ctf_challenge_1
Tables:
- challenge_users
- challenge_articles
- challenge_sensitive_data
```

#### XSS靶场 (ctf_challenge_2)
```sql
Database: ctf_challenge_2
Tables:
- challenge_users
- challenge_posts
- challenge_comments
```

#### 文件上传靶场 (ctf_challenge_3)
```sql
Database: ctf_challenge_3
Tables:
- challenge_users
- challenge_files
- challenge_logs
```

## 2. 初始化步骤

### 2.1 系统主数据库初始化
1. 运行系统数据库初始化脚本:
```bash
python backend/scripts/init_mysql.py
```

2. 初始化靶场基础数据:
```bash
python backend/init_data.py
```

### 2.2 靶场数据库初始化
1. SQL注入靶场:
```bash
cd challenges/web_security/sql_injection
python init_db.py
```

2. XSS靶场:
```bash
cd challenges/web_security/xss
python init_db.py
```

3. 文件上传靶场:
```bash
cd challenges/web_security/file_upload
python init_db.py
```

## 3. 数据库管理

### 3.1 权限管理
1. 系统主数据库:
- root用户拥有完整权限
- 应用程序使用专门的用户访问

2. 靶场数据库:
- 每个靶场使用独立的数据库用户
- 权限仅限于对应的靶场数据库

### 3.2 数据备份
1. 系统主数据库:
- 定期完整备份
- 实时binlog备份

2. 靶场数据库:
- 保存初始状态备份
- 定期重置到初始状态

### 3.3 数据隔离
1. 系统数据隔离:
- 主数据库与靶场数据库分离
- 避免靶场漏洞影响系统数据

2. 靶场环境隔离:
- 每个靶场使用独立数据库
- 靶场之间互不影响

## 4. 维护指南

### 4.1 日常维护
1. 数据库监控:
- 监控连接数
- 监控资源使用
- 监控错误日志

2. 性能优化:
- 定期分析慢查询
- 优化索引结构
- 清理过期数据

### 4.2 故障处理
1. 系统主数据库:
- 配置主从复制
- 准备故障切换方案
- 定期演练恢复流程

2. 靶场数据库:
- 保持初始化脚本可用
- 随时可以重建环境
- 定期验证重置功能

## 5. 安全建议

### 5.1 访问控制
1. 网络隔离:
- 使用内部网络
- 限制外部访问
- 配置防火墙规则

2. 用户权限:
- 最小权限原则
- 定期审计权限
- 及时移除无用账号

### 5.2 数据保护
1. 敏感数据:
- 加密存储
- 访问审计
- 定期清理

2. 备份保护:
- 加密备份文件
- 安全存储备份
- 定期验证备份

## 6. 注意事项

1. 数据库重置:
- 靶场数据库可以随时重置
- 不影响系统主数据库
- 保持用户进度数据

2. 性能考虑:
- 控制单个靶场资源使用
- 监控数据库性能
- 及时处理异常

3. 安全防护:
- 防止SQL注入
- 控制资源访问
- 监控异常行为 