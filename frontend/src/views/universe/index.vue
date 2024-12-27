<template>
  <div class="universe-container">
    <div v-if="isLoading" class="loading-overlay">
      <el-spinner />
      <p>加载知识宇宙中...</p>
    </div>
    
    <div class="toolbar">
      <el-button-group>
        <el-button @click="resetCamera">
          重置视图
        </el-button>
        <el-button @click="toggleAutoRotate">
          {{ isAutoRotating ? '停止旋转' : '开始旋转' }}
        </el-button>
      </el-button-group>
    </div>

    <!-- 添加筛选面板 -->
    <div class="filter-panel">
      <div class="search-box">
        <el-input
          v-model="searchQuery"
          placeholder="搜索知识点..."
          clearable
          @input="filterNodes"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>

      <div class="category-filters">
        <h4>知识分类</h4>
        <el-checkbox-group v-model="selectedCategories" @change="filterNodes">
          <el-checkbox v-for="cat in categories" :key="cat.value" :label="cat.value">
            <span class="category-label" :style="{ color: getCategoryColor(cat.value) }">
              {{ cat.label }}
            </span>
          </el-checkbox>
        </el-checkbox-group>
      </div>

      <div class="filter-stats">
        <p>显示 {{ filteredNodes.length }}/{{ nodes.length }} 个知识点</p>
      </div>
    </div>
    
    <KnowledgeUniverse 
      v-if="!isLoading && nodes.length > 0"
      ref="universeRef"
      :nodes="filteredNodes"
      :links="filteredLinks"
      @node-click="handleNodeClick"
      @node-hover="handleNodeHover"
    />

    <!-- 节点详情弹窗 -->
    <el-dialog
      v-model="showNodeDetail"
      :title="selectedNode?.name"
      width="500px"
      destroy-on-close
    >
      <div v-if="selectedNode" class="node-detail">
        <p class="category">类别：{{ selectedNode.category }}</p>
        <p class="description">{{ selectedNode.description }}</p>
        <div class="related-nodes">
          <h4>相关知识点：</h4>
          <el-tag 
            v-for="node in relatedNodes" 
            :key="node.id"
            class="related-node-tag"
            @click="selectNode(node)"
          >
            {{ node.name }}
          </el-tag>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { Search } from '@element-plus/icons-vue'
import KnowledgeUniverse from './components/KnowledgeUniverse.vue'
import { generateMockData } from './mock/data'

// 组件引用
const universeRef = ref()

// 状态
const isLoading = ref(true)
const isAutoRotating = ref(false)
const showNodeDetail = ref(false)
const selectedNode = ref<any>(null)
const nodes = ref<any[]>([])
const links = ref<any[]>([])
const searchQuery = ref('')
const selectedCategories = ref<string[]>([])

// 分类定义
const categories = [
  { label: 'Web技术', value: 'web' },
  { label: '安全技术', value: 'security' },
  { label: '网络技术', value: 'network' },
  { label: '系统技术', value: 'system' },
  { label: '数据库', value: 'database' }
]

// 计算属性
const filteredNodes = computed(() => {
  let filtered = nodes.value

  // 应用搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(node => 
      node.name.toLowerCase().includes(query) ||
      node.description.toLowerCase().includes(query)
    )
  }

  // 应用分类过滤
  if (selectedCategories.value.length > 0) {
    filtered = filtered.filter(node => 
      selectedCategories.value.includes(node.category)
    )
  }

  return filtered
})

const filteredLinks = computed(() => {
  const filteredNodeIds = new Set(filteredNodes.value.map(n => n.id))
  return links.value.filter(link => 
    filteredNodeIds.has(link.source) && filteredNodeIds.has(link.target)
  )
})

const relatedNodes = computed(() => {
  if (!selectedNode.value) return []
  return nodes.value.filter(node => 
    links.value.some(link => 
      (link.source === selectedNode.value.id && link.target === node.id) ||
      (link.target === selectedNode.value.id && link.source === node.id)
    )
  )
})

// 方法
const resetCamera = () => {
  universeRef.value?.resetCamera()
}

const toggleAutoRotate = () => {
  isAutoRotating.value = !isAutoRotating.value
  universeRef.value?.toggleAutoRotate(isAutoRotating.value)
}

const handleNodeClick = (node: any) => {
  selectedNode.value = node
  showNodeDetail.value = true
}

const handleNodeHover = (node: any) => {
  universeRef.value?.highlightNode(node)
}

const selectNode = (node: any) => {
  selectedNode.value = node
  universeRef.value?.focusNode(node)
}

const filterNodes = () => {
  // 触发重新渲染
  nodes.value = [...nodes.value]
}

const getCategoryColor = (category: string) => {
  const colors: { [key: string]: string } = {
    'web': '#4A90E2',
    'security': '#FF6B6B',
    'network': '#50E3C2',
    'system': '#F8E71C',
    'database': '#B8E986'
  }
  return colors[category] || '#cccccc'
}

// 初始化
onMounted(async () => {
  try {
    console.log('Initializing universe view')
    const mockData = generateMockData()
    
    // 模拟加载延迟
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    nodes.value = mockData.nodes
    links.value = mockData.links
    selectedCategories.value = categories.map(c => c.value)
    
    console.log('Data loaded:', { 
      nodes: nodes.value.length, 
      links: links.value.length 
    })
    
    isLoading.value = false
  } catch (error) {
    console.error('Error initializing universe:', error)
  }
})
</script>

<style lang="scss" scoped>
.universe-container {
  width: 100%;
  height: 100vh;
  background: #000;
  position: relative;
  overflow: hidden;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  z-index: 100;
  
  p {
    margin-top: 16px;
  }
}

.toolbar {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
}

.filter-panel {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 280px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 8px;
  padding: 16px;
  color: #fff;
  z-index: 10;

  .search-box {
    margin-bottom: 16px;
  }

  .category-filters {
    h4 {
      margin-bottom: 12px;
      font-weight: normal;
      color: #999;
    }

    .el-checkbox {
      display: block;
      margin-bottom: 8px;
      
      :deep(.el-checkbox__label) {
        color: #fff;
      }
    }

    .category-label {
      margin-left: 4px;
    }
  }

  .filter-stats {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    font-size: 12px;
    color: #999;
  }
}

.node-detail {
  color: #333;
  
  .category {
    color: #666;
    margin-bottom: 12px;
  }
  
  .description {
    line-height: 1.6;
    margin-bottom: 20px;
  }
  
  .related-nodes {
    h4 {
      margin-bottom: 12px;
    }
    
    .related-node-tag {
      margin: 0 8px 8px 0;
      cursor: pointer;
    }
  }
}
</style> 