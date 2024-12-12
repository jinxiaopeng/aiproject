# 知识图谱服务文档

## 概述

知识图谱服务是系统的核心服务，负责管理和维护知识图谱的实体、关系和属性。它提供了完整的API接口，支持知识图谱的构建、查询、分析和可视化。

## 技术栈

- FastAPI: Web框架
- SQLAlchemy: ORM
- MySQL: 数据存储
- NetworkX: 图分析
- Pandas: 数据处理

## 数据库设计

### 1. 实体表 (kg_entities)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| name | String(255) | 实体名称 |
| entity_type | String(50) | 实体类型 |
| description | Text | 描述 |
| properties | Text | 属性(JSON) |
| source_type | Enum | 来源类型 |
| status | Enum | 状态 |
| version | Integer | 版本号 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| last_modified_by | String | 最后修改者 |

### 2. 关系表 (kg_relationships)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| name | String(255) | 关系名称 |
| description | Text | 描述 |
| properties | Text | 属性(JSON) |
| source_type | Enum | 来源类型 |
| status | Enum | 状态 |
| version | Integer | 版本号 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| last_modified_by | String | 最后修改者 |

### 3. 实体关系表 (kg_entity_relationships)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| source_entity_id | Integer | 源实体ID |
| target_entity_id | Integer | 目标实体ID |
| relationship_id | Integer | 关系ID |
| confidence | Float | 置信度 |
| confidence_level | Enum | 置信度级别 |
| source_type | Enum | 来源类型 |
| status | Enum | 状态 |
| version | Integer | 版本号 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| last_modified_by | String | 最后修改者 |

### 4. 实体属性表 (kg_entity_attributes)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| entity_id | Integer | 实体ID |
| name | String(255) | 属性名 |
| value | Text | 属性值 |
| data_type | String(50) | 数据类型 |
| source_type | Enum | 来源类型 |
| status | Enum | 状态 |
| version | Integer | 版本号 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| last_modified_by | String | 最后修改者 |

## API接口

### 1. 实体管理

#### 创建实体
- 端点: `/api/entities`
- 方法: POST
- 需要认证: 是
- 参数:
  ```json
  {
    "name": "string",
    "entity_type": "string",
    "description": "string",
    "properties": {
      "key": "value"
    }
  }
  ```

#### 查询实体
- 端点: `/api/entities/{entity_id}`
- 方法: GET
- 需要认证: 是
- 响应:
  ```json
  {
    "id": 1,
    "name": "string",
    "entity_type": "string",
    "description": "string",
    "properties": {},
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```

### 2. 关系管理

#### 创建关系
- 端点: `/api/relationships`
- 方法: POST
- 需要认证: 是
- 参数:
  ```json
  {
    "source_entity_id": 1,
    "target_entity_id": 2,
    "relationship_type": "string",
    "properties": {},
    "confidence": 0.95
  }
  ```

#### 查询关系
- 端点: `/api/relationships/{relationship_id}`
- 方法: GET
- 需要认证: 是
- 响应:
  ```json
  {
    "id": 1,
    "source_entity_id": 1,
    "target_entity_id": 2,
    "relationship_type": "string",
    "properties": {},
    "confidence": 0.95,
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```

### 3. 图谱分析

#### 社区发现
- 端点: `/api/analysis/community`
- 方法: GET
- 需要认证: 是
- 参数:
  - algorithm: 算法类型 (louvain/label_propagation)
  - min_size: 最小社区大小

#### 路径分析
- 端点: `/api/analysis/path`
- 方法: GET
- 需要认证: 是
- 参数:
  - source_id: 源实体ID
  - target_id: 目标实体ID
  - max_depth: 最大深度

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| DATABASE_URL | 数据库连接URL | mysql+mysqlconnector://root:password@localhost/aiproject |
| CACHE_URL | 缓存服务器URL | redis://localhost |
| LOG_LEVEL | 日志级别 | INFO |

## 部署说明

### 1. 准备环境

```bash
# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
# 创建迁移
python -m alembic revision --autogenerate -m "description"

# 执行迁移
python -m alembic upgrade head
```

### 3. 启动服务

```bash
python -m knowledge_graph.main
```

## 开发指南

### 添加新的实体类型

1. 在模型中定义实体类型
2. 添加相应的验证规则
3. 创建处理函数
4. 注册API路由

### 添加新的分析功能

1. 在services目录下创建新的服务类
2. 实现分析算法
3. 创建API端点
4. 添加测试用例

## 数据导入导出

### 导入数据

支持以下格式：
- CSV
- JSON
- RDF
- Neo4j导出文件

示例：
```bash
python -m knowledge_graph.tools.import --format csv --file data.csv
```

### 导出数据

支持以下格式：
- CSV
- JSON
- RDF
- Neo4j兼容格式

示例：
```bash
python -m knowledge_graph.tools.export --format json --output graph.json
```

## 性能优化

1. 查询优化
   - 使用适当的索引
   - 优化SQL查询
   - 实现缓存机制

2. 并发处理
   - 使用连接池
   - 实现任务队列
   - 异步处理

3. 缓存策略
   - 实体缓存
   - 关系缓存
   - 查询结果缓存

## 监控和日志

### 监控指标

1. 系统性能
   - API响应时间
   - 数据库查询时间
   - 内存使用情况

2. 业务指标
   - 实体数量
   - 关系数量
   - 查询频率

### 日志记录

1. 操作日志
   - 实体创建/修改
   - 关系创建/修改
   - 用户操作记录

2. 系统日志
   - 错误信息
   - 性能问题
   - 安全事件

## 常见问题

1. 图谱规模扩展
   - 使用分区策略
   - 实现增量更新
   - 优化查询性能

2. 数据一致性
   - 使用事务
   - 实现版本控制
   - 定期数据校验

3. 查询超时
   - 设置超时限制
   - 实现分页查询
   - 优化查询路径 