<template>
  <div class="graph-container">
    <graph-renderer
      v-if="nodes.length > 0"
      :nodes="filteredNodes"
      :edges="filteredEdges"
      @nodeClick="handleNodeClick"
      @nodeHover="handleNodeHover"
    />
    <div v-if="error" class="error-message">
      <el-alert :title="error" type="error" show-icon :closable="false">
        <template #default>
          <el-button size="small" @click="handleRetry">重试</el-button>
        </template>
      </el-alert>
    </div>
    <div v-if="loading" class="loading-mask">
      <el-loading background="rgba(26, 29, 33, 0.9)" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useKnowledgeGraphStore } from '../store/index'
import { getKnowledgeGraph } from '@/api/knowledge'
import { ElMessage } from 'element-plus'
import GraphRenderer from './graph/GraphRenderer.vue'
import type { KnowledgeNode, KnowledgeLink } from '@/api/knowledge'

// 状态变量
const nodes = ref<KnowledgeNode[]>([])
const edges = ref<KnowledgeLink[]>([])
const error = ref('')
const loading = ref(true)

// 获取 store
const store = useKnowledgeGraphStore()
const { filteredNodes, filteredEdges } = storeToRefs(store)

// 初始化数据
const initData = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const data = await getKnowledgeGraph()
    nodes.value = data.nodes
    edges.value = data.links

    // 更新 store
    store.setNodes(data.nodes)
    store.setEdges(data.links)

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
  store.setHoveredNode(node)
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
  min-height: 600px;
  background: transparent;
  border-radius: 4px;
  overflow: hidden;
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
  right: 0;
  bottom: 0;
  background: rgba(26, 29, 33, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

:deep(.el-alert) {
  background: rgba(245, 108, 108, 0.1);
  border: 1px solid rgba(245, 108, 108, 0.2);
}

:deep(.el-alert__title) {
  color: #f56c6c;
}

:deep(.el-button--default) {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: #e5eaf3;
}

:deep(.el-button--default:hover) {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  color: #fff;
}
</style> 