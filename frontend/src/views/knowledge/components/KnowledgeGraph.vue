<template>
  <div class="graph-container">
    <graph-renderer
      v-if="nodes.length > 0"
      ref="renderer"
      :nodes="nodes"
      :edges="edges"
      @node-click="handleNodeClick"
      @node-hover="handleNodeHover"
    />
    <graph-controls
      @zoom-in="handleZoomIn"
      @zoom-out="handleZoomOut"
      @reset="handleReset"
      @center="handleCenter"
    />
    <div v-if="error" class="error-message">
      <el-alert :title="error" type="error" show-icon :closable="false">
        <template #default>
          <el-button size="small" @click="handleRetry">重试</el-button>
        </template>
      </el-alert>
    </div>
    <div v-if="loading" class="loading-mask">
      <el-loading background="rgba(255, 255, 255, 0.9)" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useKnowledgeGraphStore } from '../store'
import { getKnowledgeGraph } from '@/api/knowledge'
import { ElMessage } from 'element-plus'
import GraphRenderer from './graph/GraphRenderer.vue'
import GraphControls from './graph/GraphControls.vue'
import type { KnowledgeNode, KnowledgeLink } from '@/api/knowledge'

// 状态变量
const renderer = ref()
const error = ref('')
const loading = ref(true)
const nodes = ref<KnowledgeNode[]>([])
const edges = ref<KnowledgeLink[]>([])

// 获取 store
const store = useKnowledgeGraphStore()

// 模拟数据
const mockData = {
  nodes: [
    {
      id: '1',
      name: 'SQL注入',
      category: 'vulnerability',
      difficulty: 'basic',
      value: 1,
      description: 'SQL注入是一种常见的Web应用程序漏洞',
      keyPoints: ['参数化查询', '输入验证', '最小权限原则'],
      resources: [
        {
          type: 'article',
          items: [
            {
              name: 'SQL注入基础',
              description: 'SQL注入攻击原理和防御',
              title: 'SQL注入基础教程',
              url: '#'
            }
          ]
        }
      ],
      prerequisites: [],
      nextSteps: ['2', '3']
    },
    // ... 其他节点数据
  ],
  links: [
    { source: '1', target: '2', type: '前置知识', value: 1 },
    // ... 其他连接数据
  ]
}

// 初始化数据
const initData = async () => {
  try {
    loading.value = true
    error.value = ''
    
    let data
    try {
      // 尝试从API获取数据
      data = await getKnowledgeGraph()
      console.log('API data loaded:', data)
    } catch (apiError) {
      console.warn('API call failed, using mock data:', apiError)
      // API调用失败时使用模拟数据
      data = mockData
      console.log('Using mock data:', data)
    }

    if (!data || !data.nodes || !data.links) {
      throw new Error('Invalid data format')
    }

    // 为每个节点添加默认的 resources 字段
    const processedNodes = data.nodes.map((node: KnowledgeNode) => ({
      ...node,
      resources: node.resources || [
        {
          type: 'article',
          items: [
            {
              name: `${node.name}基础`,
              description: `${node.name}的基本概念和应用`,
              title: `${node.name}学习指南`,
              url: '#'
            }
          ]
        }
      ]
    }))

    // 更新本地状态
    nodes.value = processedNodes
    edges.value = data.links

    // 更新 store
    store.setNodes(processedNodes)

    console.log('Nodes loaded:', nodes.value.length)
    console.log('Edges loaded:', edges.value.length)
  } catch (err) {
    console.error('Failed to load knowledge graph:', err)
    error.value = '加载知识图谱失败，请检查网络连接'
    ElMessage.error(error.value)
  } finally {
    loading.value = false
  }
}

// 事件处理
const handleNodeClick = (node: KnowledgeNode) => {
  store.setSelectedNode(node)
}

const handleNodeHover = (node: KnowledgeNode | null) => {
  if (node) {
    renderer.value?.highlightNode(node.id)
  } else {
    renderer.value?.resetHighlight()
  }
}

const handleZoomIn = () => {
  renderer.value?.zoomIn()
}

const handleZoomOut = () => {
  renderer.value?.zoomOut()
}

const handleReset = () => {
  renderer.value?.reset()
}

const handleCenter = () => {
  renderer.value?.centerView()
}

const handleRetry = () => {
  error.value = ''
  initData()
}

// 生命周期钩子
onMounted(() => {
  console.log('KnowledgeGraph mounted')
  initData()
})
</script>

<style scoped>
.graph-container {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 500px;
  background: #1a1d21;
  background-image: 
    radial-gradient(circle at 25px 25px, rgba(65, 184, 131, 0.15) 2%, transparent 0%),
    radial-gradient(circle at 75px 75px, rgba(66, 184, 231, 0.15) 2%, transparent 0%);
  background-size: 100px 100px;
  border-radius: 4px;
  overflow: hidden;
  border: 1px solid rgba(65, 184, 131, 0.1);
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
}

.error-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
}

.loading-mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(26, 29, 33, 0.9);
  z-index: 5;
}

:deep(.el-loading-mask) {
  background-color: rgba(26, 29, 33, 0.9);
}

:deep(.el-loading-spinner .path) {
  stroke: #41b883;
}

:deep(.el-loading-spinner .el-loading-text) {
  color: #41b883;
}

:deep(.el-alert--error) {
  background-color: rgba(245, 108, 108, 0.1);
  border: 1px solid rgba(245, 108, 108, 0.2);
  color: #f56c6c;
}

:deep(.el-alert__title) {
  color: #f56c6c;
}

:deep(.el-button--default) {
  background: transparent;
  border: 1px solid rgba(65, 184, 131, 0.3);
  color: #41b883;
}

:deep(.el-button--default:hover) {
  background: rgba(65, 184, 131, 0.1);
  border-color: rgba(65, 184, 131, 0.5);
}
</style> 