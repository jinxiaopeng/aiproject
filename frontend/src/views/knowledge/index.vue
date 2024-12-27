<template>
  <div class="knowledge-view">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
      <div class="left">
        <el-button-group>
          <el-button
            :type="layoutMode === 'force' ? 'primary' : 'default'"
            @click="setLayoutMode('force')"
          >
            力导向布局
          </el-button>
          <el-button
            :type="layoutMode === 'tree' ? 'primary' : 'default'"
            @click="setLayoutMode('tree')"
          >
            树形布局
          </el-button>
        </el-button-group>
      </div>
      <div class="right">
        <el-button-group>
          <el-button
            :type="showFilters ? 'primary' : 'default'"
            @click="showFilters = !showFilters"
          >
            筛选
          </el-button>
          <el-button
            :type="showDetail ? 'primary' : 'default'"
            @click="showDetail = !showDetail"
          >
            详情
          </el-button>
        </el-button-group>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧筛选面板 -->
      <div
        v-show="showFilters"
        class="filters-panel"
        :class="{ 'panel-hidden': !showFilters }"
      >
        <graph-filters />
      </div>

      <!-- 中间图谱区域 -->
      <div class="graph-container">
        <graph-renderer
          :layout-mode="layoutMode"
          @node-click="handleNodeClick"
          @node-hover="handleNodeHover"
        />
      </div>

      <!-- 右侧详情面板 -->
      <div
        v-show="showDetail"
        class="detail-panel"
        :class="{ 'panel-hidden': !showDetail }"
      >
        <el-tabs v-model="activeTab">
          <el-tab-pane label="知识点详情" name="detail">
            <node-detail />
          </el-tab-pane>
          <el-tab-pane label="职业路径" name="career">
            <career-path-planner />
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useKnowledgeStore } from './store'
import GraphFilters from './components/GraphFilters.vue'
import GraphRenderer from './components/graph/GraphRenderer.vue'
import NodeDetail from './components/NodeDetail.vue'
import CareerPathPlanner from './components/CareerPathPlanner.vue'
import type { KnowledgeNode } from './types'

const store = useKnowledgeStore()
const activeTab = ref('detail')

// 布局模式
const layoutMode = ref<'force' | 'tree'>('force')
const setLayoutMode = (mode: 'force' | 'tree') => {
  layoutMode.value = mode
}

// 面板显示状态
const showFilters = ref(false)
const showDetail = ref(false)

// 事件处理
const handleNodeClick = (node: KnowledgeNode) => {
  store.setSelectedNode(node)
  showDetail.value = true
}

const handleNodeHover = (node: KnowledgeNode | null) => {
  store.setHoveredNode(node)
}

// 初始化数据
onMounted(async () => {
  await store.fetchGraphData()
})
</script>

<style scoped>
.knowledge-view {
  height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  background: #141414;
  overflow: hidden;
}

.toolbar {
  height: 48px;
  min-height: 48px;
  flex-shrink: 0;
  padding: 0 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
}

.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
  position: relative;
  min-height: 0;
}

.filters-panel,
.detail-panel {
  width: 320px;
  min-width: 320px;
  height: 100%;
  padding: 16px;
  background: rgba(30, 35, 40, 0.95);
  border-right: 1px solid rgba(65, 184, 131, 0.1);
  transition: transform 0.3s ease;
  overflow-y: auto;
}

.detail-panel {
  border-right: none;
  border-left: 1px solid rgba(65, 184, 131, 0.1);
}

.panel-hidden {
  transform: translateX(-100%);
}

.detail-panel.panel-hidden {
  transform: translateX(100%);
}

.graph-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  min-width: 0;
  min-height: 0;
  height: 100%;
}

:deep(.el-button) {
  --el-button-bg-color: transparent;
  --el-button-border-color: rgba(65, 184, 131, 0.2);
  --el-button-hover-bg-color: rgba(65, 184, 131, 0.1);
  --el-button-hover-border-color: rgba(65, 184, 131, 0.3);
  --el-button-active-bg-color: rgba(65, 184, 131, 0.2);
  --el-button-active-border-color: rgba(65, 184, 131, 0.4);
  --el-button-text-color: #e5eaf3;
}

:deep(.el-button--primary) {
  --el-button-bg-color: rgba(65, 184, 131, 0.1);
  --el-button-border-color: rgba(65, 184, 131, 0.3);
  --el-button-hover-bg-color: rgba(65, 184, 131, 0.2);
  --el-button-hover-border-color: rgba(65, 184, 131, 0.4);
  --el-button-active-bg-color: rgba(65, 184, 131, 0.3);
  --el-button-active-border-color: rgba(65, 184, 131, 0.5);
}
</style> 