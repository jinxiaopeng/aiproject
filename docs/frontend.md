# 前端应用文档

## 概述

前端应用是一个基于Vue 3的单页面应用，提供了知识图谱的可视化界面和用户交互功能。它使用了最新的Vue生态系统技术栈，包括Composition API、TypeScript和Pinia状态管理。

## 技术栈

- Vue 3: 核心框架
- TypeScript: 类型系统
- Pinia: 状态管理
- Vue Router: 路由管理
- Element Plus: UI组件库
- Vite: 构建工具
- Axios: HTTP客户端
- ECharts: 图表可视化
- Cytoscape.js: 图谱可视化

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API请求
│   ├── assets/           # 静态资源
│   ├── components/       # 通用组件
│   ├── composables/      # 组合式函数
│   ├── layouts/          # 布局组件
│   ├── router/           # 路由配置
│   ├── stores/           # 状态管理
│   ├── styles/           # 样式文件
│   ├── types/            # 类型定义
│   ├── utils/            # 工具函数
│   └── views/            # 页面组件
├── public/               # 公共资源
└── tests/                # 测试文件
```

## 功能模块

### 1. 用户认证

#### 登录页面
- 路径: `/auth/login`
- 组件: `src/views/Login.vue`
- 状态管理: `src/stores/auth.ts`
- 功能:
  - 用户登录
  - 记住密码
  - 错误提示

#### 注册页面
- 路径: `/auth/register`
- 组件: `src/views/Register.vue`
- 功能:
  - 用户注册
  - 表单验证
  - 邮箱验证

### 2. 知识图谱

#### 图谱展示
- 路径: `/graph`
- 组件: `src/views/Graph.vue`
- 功能:
  - 图谱可视化
  - 节点交互
  - 关系展示
  - 缩放和平移

#### 实体管理
- 路径: `/entities`
- 组件: `src/views/Entities.vue`
- 功能:
  - 实体列表
  - 实体创建
  - 实体编辑
  - 实体删除

#### 关系管理
- 路径: `/relationships`
- 组件: `src/views/Relationships.vue`
- 功能:
  - 关系列表
  - 关系创建
  - 关系编辑
  - 关系删除

## API集成

### 1. API配置

```typescript
// src/utils/request.ts
import axios from 'axios'

const service = axios.create({
  baseURL: '/api',
  timeout: 30000
})

service.interceptors.request.use(...)
service.interceptors.response.use(...)

export default service
```

### 2. API模块

```typescript
// src/api/auth.ts
import request from '@/utils/request'

export const login = (data: LoginRequest) => {
  return request.post('/auth/login', data)
}

export const register = (data: RegisterRequest) => {
  return request.post('/auth/register', data)
}
```

## 状态管理

### 1. 认证状态

```typescript
// src/stores/auth.ts
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: '',
    user: null
  }),
  actions: {
    async login(username: string, password: string) {
      // 登录逻辑
    }
  }
})
```

### 2. 图谱状态

```typescript
// src/stores/graph.ts
import { defineStore } from 'pinia'

export const useGraphStore = defineStore('graph', {
  state: () => ({
    nodes: [],
    edges: []
  }),
  actions: {
    async loadGraph() {
      // 加载图谱数据
    }
  }
})
```

## 组件开发

### 1. 创建新组件

```vue
<!-- src/components/Example.vue -->
<template>
  <div class="example">
    <!-- 组件模板 -->
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// 组件逻辑
</script>

<style scoped>
/* 组件样式 */
</style>
```

### 2. 组件通信

- Props和Events
- Provide/Inject
- 状态管理
- 组合式函数

## 路由配置

```typescript
// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/auth/login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/graph',
    component: () => import('@/views/Graph.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 认证检查
})
```

## 样式管理

### 1. 全局样式

```scss
// src/styles/index.scss
@import './variables.scss';
@import './mixins.scss';
@import './transitions.scss';
```

### 2. 主题定制

```typescript
// src/styles/element-variables.scss
@forward 'element-plus/theme-chalk/src/common/var.scss' with (
  $colors: (
    'primary': (
      'base': #409eff,
    ),
  )
);
```

## 开发指南

### 1. 开发环境设置

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 运行测试
npm run test
```

### 2. 代码规范

- ESLint配置
- Prettier配置
- TypeScript配置
- Git提交规范

## 测试

### 1. 单元测试

```typescript
// tests/unit/example.spec.ts
import { mount } from '@vue/test-utils'
import Example from '@/components/Example.vue'

describe('Example.vue', () => {
  it('renders props correctly', () => {
    const wrapper = mount(Example, {
      props: {
        msg: 'Hello'
      }
    })
    expect(wrapper.text()).toContain('Hello')
  })
})
```

### 2. E2E测试

```typescript
// tests/e2e/specs/test.js
describe('Example', () => {
  it('visits the app root url', () => {
    cy.visit('/')
    cy.contains('h1', 'Welcome')
  })
})
```

## 部署

### 1. 构建配置

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  build: {
    target: 'es2015',
    outDir: 'dist'
  }
})
```

### 2. 环境配置

```env
# .env.production
VITE_API_BASE_URL=/api
VITE_APP_TITLE=知识图谱系统
```

## 性能优化

1. 路由懒加载
2. 组件按需导入
3. 图片懒加载
4. 虚拟滚动
5. 缓存优化

## 安全考虑

1. XSS防护
2. CSRF防护
3. 敏感信息加密
4. 权限控制

## 常见问题

1. 开发环境配置
   - Node.js版本要求
   - 依赖安装问题
   - 代理配置

2. 构建部署
   - 打包优化
   - 环境变量配置
   - 静态资源处理

3. 性能问题
   - 首屏加载优化
   - 大数据渲染
   - 内存泄漏 