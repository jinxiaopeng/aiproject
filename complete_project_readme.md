# Web安全智能防护与响应平台 (WSIRP)

[![Stars](https://img.shields.io/github/stars/your-team/wsirp?style=social)](https://github.com/your-team/wsirp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Vue](https://img.shields.io/badge/vue-3.x-green.svg)](https://vuejs.org)

![系统架构图](./screenshots/architecture.png)
![系统界面](./screenshots/dashboard.png)

## 📖 项目概述

### 项目背景
随着数字经济的蓬勃发展，企业数字化转型进程不断加快，Web应用系统在企业运营中扮演着越来越重要的角色。然而，伴随而来的安全威胁也日益严峻：

1. **安全形势严峻**
   - 2022年全球Web应用攻击增长178%
   - 零日漏洞利用时间从发现到攻击缩短至24小时内
   - 超过60%的数据泄露事件源于Web应用漏洞

2. **传统防护不足**
   - 人工安全检测效率低下，无法应对海量威胁
   - 被动防御模式导致防护滞后，难以预防未知威胁
   - 安全工具分散，缺乏统一的安全态势管理

3. **企业需求迫切**
   - 需要更智能、自动化的安全防护方案
   - 要求更快速的威胁发现和响应能力
   - 期望更全面的安全态势感知能力

基于以上背景，本项目立足于解决企业在Web安全领域面临的实际问题，采用人工智能、大数据分析等前沿技术，打造新一代智能化的Web安全防护平台。通过将传统安全能力与现代智能技术相结合，为企业提供全方位、智能化、自动化的安全防护解决方案。

### 项目特性
- 🔒 **全面防护**: 覆盖OWASP Top 10安全风险
- 🤖 **AI驱动**: 基于深度学习的智能威胁检测
- ⚡ **实时响应**: 毫秒级威胁检测与防护
- 📊 **可视分析**: 多维度安全态势展示
- 🔄 **持续进化**: 自学习的安全防护体系
- 🌐 **分布式架构**: 支持大规模部署与扩展
- 📱 **多端支持**: Web、移动端完整适配

### 技术架构
```
                    ┌─────────────────┐
                    │    前端展示层    │
                    │  Vue3 + TypeScript │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │    网关层      │
                    │   Nginx/Kong    │
                    └────────┬────────┘
                             │
        ┌──────────────────┬─┴──┬──────────────────┐
        │                  │    │                  │
┌───────▼───────┐  ┌──────▼────▼──┐  ┌────────────▼─────────┐
│   认证服务     │  │  业务服务集群  │  │     AI分析集群      │
│ OAuth2.0/JWT  │  │   FastAPI     │  │ TensorFlow/PyTorch  │
└───────┬───────┘  └──────┬────────┘  └──────────┬─────────┘
        │                  │                      │
        └──────────┬──────┴──────────┬───────────┘
                   │                 │
         ┌─────────▼─────────┐    ┌─▼────────────────┐
         │    数据存储层      │    │   消息队列/缓存   │
         │ MySQL/MongoDB     │    │ Redis/RabbitMQ   │
         └───────────────────┘    └──────────────────┘
```

### 快速开始

1. **克隆项目**
```bash
git clone https://github.com/your-team/wsirp.git
cd wsirp
```

2. **环境准备**
```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
npm install
```

3. **配置文件**
```bash
cp .env.example .env
# 编辑.env文件，配置必要的环境变量
```

4. **启动服务**
```bash
# 后端服务
python manage.py runserver

# 前端开发服务
npm run dev
```

### 开发规范

#### 代码风格
- 后端遵循[PEP 8](https://www.python.org/dev/peps/pep-0008/)规范
- 前端遵循[Vue Style Guide](https://v3.vuejs.org/style-guide/)
- 使用ESLint + Prettier进行代码格式化

#### Git提交规范
```bash
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构代码
test: 测试相关
chore: 构建/工具相关
```

#### 安全开发规范
- 所有API必须进行认证和授权
- 敏感数据必须加密存储
- 定期进行依赖包安全更新
- 必须进行输入验证和输出转义
- 使用参数化查询防止SQL注入

### 测试与部署

#### 自动化测试
```bash
# 运行单元测试
python -m pytest tests/

# 运行端到端测试
npm run test:e2e
```

#### Docker部署
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

### 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

### 版本发布

使用[语义化版本](https://semver.org/)进行版本控制：
- MAJOR.MINOR.PATCH
- MAJOR: 不兼容的API修改
- MINOR: 向下兼容的功能性新增
- PATCH: 向下兼容的问题修正

### 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

### 联系我们

- 项目负责人: [name](mailto:email@example.com)
- 技术支持: [support@example.com](mailto:support@example.com)
- 项目主页: [https://github.com/your-team/wsirp](https://github.com/your-team/wsirp)

## 🔥 核心功能模块

### 1. 智能认证中心
- 多因素身份认证
- 基于行为的身份识别
- 细粒度RBAC权限管理
- 全方位审计日志
- 单点登录(SSO)支持
- OAuth2.0社交登录

**技术栈**:
- 前端: Vue3 + TypeScript + Element Plus
- 后端: Python FastAPI
- 数据库: MySQL 8.0
- 认证: OAuth2.0 + JWT
- 缓存: Redis
- 消息队列: RabbitMQ
- 监控: Prometheus + Grafana

### 2. AI驱动的漏洞扫描引擎
- 智能爬虫技术
- 深度学习漏洞识别
- 自适应扫描策略
- 误报智能过滤
- 实时扫描监控

**创新特性**:
- 基于CNN的漏洞特征提取
- 智能化扫描路径规划
- 动态验证机制
- 自学习规则引擎

### 3. 智能攻防演练平台
- 自动化渗透测试
- 攻击链路分析
- 威胁情报融合
- 场景化攻防演练

**核心能力**:
- 集成OWASP TOP10检测
- 自定义攻击脚本框架
- 智能化攻击路径推荐
- 攻击效果评估体系

### 4. 自动化应急响应
- 智能化漏洞修复
- 自动化应急处置
- 安全基线核查
- 修复效果验证

**创新价值**:
- AI辅助代码修复建议
- 自动化补丁部署
- 修复知识图谱
- 闭环验证机制

### 5. 安全态势感知
- 多维度监控预警
- 智能化事件分析
- 可视化态势展示
- 预测性防御

**技术架构**:
- Elasticsearch集群
- Grafana可视化
- AI预警模型
- 分布式计算框架

## 🌟 项目价值

### 行业应用价值
- 提升企业安全防护能力
- 降低安全运营成本
- 加速安全响应效率
- 构建主动防御体系
- 优化安全运营流程
- 提高安全管理效率

### 创新突破
- AI算法在安全领域的创新应用
- 自动化响应机制的突破
- 智能化决策支持系统
- 新一代安全防护理念

### 社会贡献
- 促进网络空间安全建设
- 推动安全技术发展
- 培养网络安全人才
- 提升产业数字化水平

## 🚀 快速部署

### 环境要求
- Python >= 3.8
- Node.js >= 16
- MySQL >= 8.0
- Redis >= 6.0
- RabbitMQ >= 3.8
- Docker >= 20.10
- Docker Compose >= 2.0

## 💻 系统实现

### 详细架构设计
```
├── frontend/                # 前端项目
│   ├── src/
│   │   ├── views/          # 页面组件
│   │   │   ├── dashboard/  # 控制台
│   │   │   ├── scan/       # 扫描管理
│   │   │   └── report/     # 报告管理
│   │   ├── components/     # 通用组件
│   │   └── utils/          # 工具函数
│   └── tests/              # 测试文件
├── backend/                # 后端项目
│   ├── api/               # API接口
│   ├── core/              # 核心功能
│   │   ├── scanner/       # 扫描引擎
│   │   ├── detector/      # 检测模型
│   │   └── analyzer/      # 分析模块
│   └── models/            # 数据模型
└── deploy/                # 部署配置
    ├── docker/           # Docker配置
    └─ kubernetes/       # K8s配置
```

### 数据库设计
```sql
-- 目标资产表
CREATE TABLE targets (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    url VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    type VARCHAR(50),
    status TINYINT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_url (url),
    INDEX idx_status (status)
);

-- 漏洞信息表
CREATE TABLE vulnerabilities (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    target_id BIGINT NOT NULL,
    type VARCHAR(50) NOT NULL,
    severity ENUM('low', 'medium', 'high', 'critical'),
    description TEXT,
    solution TEXT,
    status TINYINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (target_id) REFERENCES targets(id),
    INDEX idx_severity (severity),
    INDEX idx_type (type)
);
```

### API接口设计
```python
# api/routes/scan.py
from fastapi import APIRouter, Depends
from typing import List

router = APIRouter()

@router.post("/scan/start")
async def start_scan(target: ScanTarget, current_user: User = Depends(get_current_user)):
    """启动扫描任务"""
    task = await scanner.create_task(target, current_user)
    return {"task_id": task.id}

@router.get("/scan/{task_id}/status")
async def get_scan_status(task_id: int):
    """获取扫描状态"""
    status = await scanner.get_task_status(task_id)
    return {"status": status}
```

### 前端实现
```typescript
// src/views/scan/ScanManager.vue
<template>
  <div class="scan-manager">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>扫描任务管理</span>
          <el-button type="primary" @click="startNewScan">
            新建扫描
          </el-button>
        </div>
      </template>
      
      <el-table :data="scanTasks" v-loading="loading">
        <el-table-column prop="id" label="任务ID" width="100" />
        <el-table-column prop="target" label="目标" />
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <scan-status :status="row.status" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button @click="viewDetails(row)">查看</el-button>
            <el-button type="danger" @click="stopScan(row)">
              停止
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getScanTasks, startScan, stopScan } from '@/api/scan'

export default defineComponent({
  name: 'ScanManager',
  setup() {
    const scanTasks = ref([])
    const loading = ref(false)

    const loadTasks = async () => {
      loading.value = true
      try {
        scanTasks.value = await getScanTasks()
      } catch (error) {
        ElMessage.error('加载任务失败')
      }
      loading.value = false
    }

    onMounted(loadTasks)

    return {
      scanTasks,
      loading,
      startNewScan: async () => {
        // 实现新建扫描逻辑
      },
      stopScan: async (task) => {
        // 实现停止扫描逻辑
      }
    }
  }
})
</script>
```

### Windows环境快速开始

1. **安装必要的软件**
```powershell
# 安装 Python 3.8+
# 从 https://www.python.org/downloads/ 下载并安装

# 安装 Node.js 16+
# 从 https://nodejs.org/download/ 下载并安装

# 安装 Git
# 从 https://git-scm.com/download/win 下载并安装
```

2. **克隆项目**
```powershell
# 打开 PowerShell 或 CMD
git clone https://github.com/your-team/wsirp.git
cd wsirp
```

3. **配置Python环境**
```powershell
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\activate

# 安装Python依赖
pip install -r requirements.txt
```

4. **配置Node环境**
```powershell
# 安装前端依赖
npm install
```

5. **配置数据库**
```powershell
# 安装 MySQL 8.0
# 从 https://dev.mysql.com/downloads/installer/ 下载并安装

# 安装 Redis for Windows
# 从 https://github.com/microsoftarchive/redis/releases 下载并安装

# 启动Redis服务
net start redis

# 安装 RabbitMQ
# 从 https://www.rabbitmq.com/install-windows.html 下载并安装
```

6. **环境配置**
```powershell
# 复制环境配置文件
copy .env.example .env

# 使用记事本编辑 .env 文件
notepad .env

# 配置以下必要参数:
# DB_HOST=localhost
# DB_PORT=3306
# DB_NAME=wsirp
# DB_USER=your_username
# DB_PASSWORD=your_password
# REDIS_HOST=localhost
# REDIS_PORT=6379
# RABBITMQ_HOST=localhost
```

7. **初始化数据库**
```powershell
# 创建数据库
python manage.py db:create

# 运行数据库迁移
python manage.py db:migrate
```

8. **启动服务**
```powershell
# 启动后端服务 (在一个新的 PowerShell 窗口中)
python manage.py runserver

# 启动前端开发服务器 (在另一个新的 PowerShell 窗口中)
npm run dev
```

9. **访问应用**
- 前端页面: http://localhost:3000
- API文档: http://localhost:8000/docs

### Windows环境故障排除

1. **Python相关问题**
```powershell
# 如果提示"无法加载文件 xxx.ps1,因为在此系统上禁止运行脚本"
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 如果安装包时出现网络问题,可以使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

2. **Node.js相关问题**
```powershell
# 如果npm安装过慢,可以使用淘宝镜像
npm config set registry https://registry.npmmirror.com
npm install

# 如果出现node-gyp相关错误,需要安装构建工具
npm install --global --production windows-build-tools
```

3. **数据库相关问题**
```powershell
# 检查MySQL服务状态
net start mysql

# 检查Redis服务状态
net start redis

# 检查RabbitMQ服务状态
net start RabbitMQ
```

### Windows开发工具推荐

- IDE: Visual Studio Code
  - 推荐插件:
    - Python
    - Vetur (Vue工具)
    - ESLint
    - Prettier
    - GitLens
    
- 数据库工具: Navicat Premium
- API测试: Postman
- Git客户端: SourceTree

### Windows性能优化建议

1. **Python优化**
```powershell
# 使用pypy3提升性能
pip install pypy3

# 启用uvicorn多工作进程
uvicorn main:app --workers 4
```

2. **Node.js优化**
```powershell
# 生产环境构建
npm run build

# 使用pm2管理进程
npm install -g pm2
pm2 start npm -- start
```

### 核心功能实现示例

#### 1. AI模型训练与部署
```python
# backend/app/core/ai/model.py
import torch
import torch.nn as nn
from transformers import BertModel

class SecurityDetectionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased')
        self.classifier = nn.Linear(768, 4)  # 4类安全威胁分类
        
    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        return self.classifier(outputs.pooler_output)

# 模型训练
def train_model(train_loader, model, optimizer, epochs=5):
    model.train()
    for epoch in range(epochs):
        for batch in train_loader:
            optimizer.zero_grad()
            input_ids = batch['input_ids']
            attention_mask = batch['attention_mask']
            labels = batch['labels']
            
            outputs = model(input_ids, attention_mask)
            loss = nn.CrossEntropyLoss()(outputs, labels)
            
            loss.backward()
            optimizer.step()
```

#### 2. 实时威胁检测
```python
# backend/app/core/detector/realtime.py
from fastapi import WebSocket
import asyncio
import json

class ThreatDetector:
    def __init__(self):
        self.model = SecurityDetectionModel()
        self.model.load_state_dict(torch.load('model.pth'))
        self.model.eval()
        
    async def detect_threats(self, websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                threat = await self.analyze_threat(json.loads(data))
                if threat['severity'] > 0.7:  # 高危威胁
                    await self.trigger_alert(threat)
                await websocket.send_json(threat)
        except Exception as e:
            logger.error(f"Detection error: {e}")
            
    async def analyze_threat(self, data):
        # 实时威胁分析逻辑
        return {
            'type': 'sql_injection',
            'severity': 0.95,
            'details': '检测到SQL注入攻击尝试'
        }
```

#### 3. 自动化漏洞修复
```python
# backend/app/core/repair/auto_fix.py
from typing import Dict
import ast

class VulnerabilityFixer:
    def __init__(self):
        self.fix_patterns = self.load_fix_patterns()
        
    def fix_vulnerability(self, code: str, vuln_type: str) -> str:
        tree = ast.parse(code)
        fixer = self.fix_patterns.get(vuln_type)
        if fixer:
            return fixer(tree)
        return code
        
    def fix_sql_injection(self, tree: ast.AST) -> str:
        # SQL注入修复逻辑
        return "SELECT * FROM users WHERE id = %s"
        
    def fix_xss(self, tree: ast.AST) -> str:
        # XSS修复逻辑
        return "html.escape(user_input)"
```

#### 4. 安全态势大屏
```typescript
// frontend/src/views/dashboard/SecurityDashboard.vue
<template>
  <div class="security-dashboard">
    <el-row :gutter="20">
      <el-col :span="8">
        <threat-trend-chart :data="threatTrend" />
      </el-col>
      <el-col :span="8">
        <vulnerability-distribution :data="vulnDist" />
      </el-col>
      <el-col :span="8">
        <alert-list :alerts="recentAlerts" />
      </el-col>
    </el-row>
    
    <el-row :gutter="20">
      <el-col :span="16">
        <attack-map :attacks="attackData" />
      </el-col>
      <el-col :span="8">
        <risk-score-card :score="riskScore" />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSecurityStore } from '@/stores/security'
import ThreatTrendChart from './components/ThreatTrendChart.vue'
import VulnerabilityDistribution from './components/VulnDistribution.vue'
import AttackMap from './components/AttackMap.vue'
import RiskScoreCard from './components/RiskScoreCard.vue'
import AlertList from './components/AlertList.vue'

const securityStore = useSecurityStore()
const threatTrend = ref([])
const vulnDist = ref([])
const attackData = ref([])
const riskScore = ref(0)
const recentAlerts = ref([])

onMounted(async () => {
  await securityStore.fetchSecurityData()
  threatTrend.value = securityStore.threatTrend
  vulnDist.value = securityStore.vulnerabilityDistribution
  attackData.value = securityStore.attackData
  riskScore.value = securityStore.riskScore
  recentAlerts.value = securityStore.recentAlerts
})
</script>
```

#### 5. 安全知识图谱
```python
# backend/app/core/knowledge/graph.py
from neo4j import GraphDatabase

class SecurityKnowledgeGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def add_vulnerability(self, vuln_data: dict):
        with self.driver.session() as session:
            session.write_transaction(self._create_vulnerability, vuln_data)
            
    def _create_vulnerability(self, tx, vuln_data):
        query = """
        MERGE (v:Vulnerability {cve: $cve})
        SET v.description = $description,
            v.severity = $severity,
            v.solution = $solution
        WITH v
        UNWIND $affected_systems as system
        MERGE (s:System {name: system})
        MERGE (s)-[:AFFECTED_BY]->(v)
        """
        tx.run(query, vuln_data)
        
    def get_related_vulnerabilities(self, system_name: str):
        with self.driver.session() as session:
            return session.read_transaction(self._get_vulnerabilities, system_name)
```

#### 6. 自动化应急响应流程
```python
# backend/app/core/incident/response.py
from typing import List
import asyncio

class IncidentResponse:
    def __init__(self):
        self.response_steps = []
        self.status = "initialized"
        
    async def handle_incident(self, incident_data: dict):
        self.status = "responding"
        try:
            # 1. 威胁隔离
            await self.isolate_threat(incident_data)
            
            # 2. 证据收集
            evidence = await self.collect_evidence(incident_data)
            
            # 3. 影响评估
            impact = await self.assess_impact(evidence)
            
            # 4. 修复执行
            await self.execute_fix(impact)
            
            # 5. 恢复确认
            await self.verify_recovery()
            
            self.status = "resolved"
            return {"status": "success", "details": self.response_steps}
            
        except Exception as e:
            self.status = "failed"
            return {"status": "failed", "error": str(e)}
```

### 部署配置示例

#### 1. Docker Compose配置
```yaml
# deploy/docker/docker-compose.yml
version: '3.8'

services:
  frontend:
    build: 
      context: ../../frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    depends_on:
      - backend
      
  backend:
    build:
      context: ../../backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DB_HOST=db
      - REDIS_HOST=redis
      - RABBITMQ_HOST=rabbitmq
    depends_on:
      - db
      - redis
      - rabbitmq
      
  db:
    image: mysql:8.0
    volumes:
      - mysql_data:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=secure_password
      - MYSQL_DATABASE=wsirp
      
  redis:
    image: redis:6.2
    volumes:
      - redis_data:/data
      
  rabbitmq:
    image: rabbitmq:3.9-management
    ports:
      - "5672:5672"
      - "15672:15672"
      
volumes:
  mysql_data:
  redis_data:
```

#### 2. Kubernetes配置
```yaml
# deploy/kubernetes/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wsirp-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wsirp-backend
  template:
    metadata:
      labels:
        app: wsirp-backend
    spec:
      containers:
      - name: wsirp-backend
        image: wsirp-backend:latest
        ports:
        - containerPort: 8000
        resources:
          limits:
            cpu: "1"
            memory: "1Gi"
          requests:
            cpu: "500m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Windows快速启动（自动配置）

我们提供了自动化配置脚本来简化Windows环境下的部署过程：

1. 确保已安装以下基础软件：
   - Python 3.8+
   - Git
   - MySQL 8.0（可选，脚本会检查）
   - Redis（可选，脚本会检查）

2. 打开PowerShell（管理员权限），允许执行脚本：
   ```powershell
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. 运行配置脚本：
   ```powershell
   .\setup_backend.ps1
   ```

4. 根据脚本提示完成配置过程

脚本会自动处理以下任务：
- 环境检查
- 虚拟环境创建
- 依赖安装
- 服务检查
- 配置文件生成
- 数据库初始化（可选）
- 服务启动（可选）
