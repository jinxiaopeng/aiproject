<template>
  <div class="graph-filters">
    <!-- 搜索框 -->
    <el-input
      v-model="searchQuery"
      placeholder="搜索知识点..."
      clearable
      prefix-icon="Search"
      @input="handleSearch"
    >
      <template #append>
        <el-tag v-if="filteredCount" type="info" size="small">
          {{ filteredCount }} 个结果
        </el-tag>
      </template>
    </el-input>

    <!-- 分类过滤器 -->
    <div class="filter-section">
      <div class="section-header">
        <h4>知识分类</h4>
        <el-tag v-if="selectedCategories.length" type="info" size="small">
          已选 {{ selectedCategories.length }}
        </el-tag>
      </div>
      <el-checkbox-group v-model="selectedCategories" @change="handleCategoryChange">
        <el-checkbox
          v-for="category in categories"
          :key="category.key"
          :label="category.key"
        >
          <div class="category-label">
            <span class="color-dot" :style="{ backgroundColor: category.color }"></span>
            {{ category.label }}
            <el-tag 
              v-if="getCategoryCount(category.key)" 
              size="small" 
              :style="{ backgroundColor: category.color + '20', color: category.color }"
            >
              {{ getCategoryCount(category.key) }}
            </el-tag>
          </div>
        </el-checkbox>
      </el-checkbox-group>
    </div>

    <!-- 难度过滤器 -->
    <div class="filter-section">
      <div class="section-header">
        <h4>难度等级</h4>
        <el-tag v-if="selectedDifficulties.length" type="info" size="small">
          已选 {{ selectedDifficulties.length }}
        </el-tag>
      </div>
      <el-checkbox-group v-model="selectedDifficulties" @change="handleDifficultyChange">
        <el-checkbox
          v-for="difficulty in difficulties"
          :key="difficulty.key"
          :label="difficulty.key"
        >
          <div class="difficulty-label">
            <el-rate
              :model-value="getDifficultyLevel(difficulty.key)"
              disabled
              :colors="[difficulty.color]"
            />
            {{ difficulty.label }}
            <el-tag 
              v-if="getDifficultyCount(difficulty.key)" 
              size="small"
              :style="{ backgroundColor: difficulty.color + '20', color: difficulty.color }"
            >
              {{ getDifficultyCount(difficulty.key) }}
            </el-tag>
          </div>
        </el-checkbox>
      </el-checkbox-group>
    </div>

    <!-- 学习状态过滤器 -->
    <div class="filter-section">
      <div class="section-header">
        <h4>学习状态</h4>
      </div>
      <el-radio-group v-model="learningStatus" @change="handleStatusChange">
        <el-radio label="all">全部</el-radio>
        <el-radio label="learning">学习中</el-radio>
        <el-radio label="completed">已完成</el-radio>
        <el-radio label="recommended">推荐学习</el-radio>
      </el-radio-group>
    </div>

    <!-- 关系过滤器 -->
    <div v-if="selectedNode" class="filter-section">
      <div class="section-header">
        <h4>知识关系</h4>
        <el-tag type="success">{{ selectedNode.name }}</el-tag>
      </div>
      <el-checkbox-group v-model="selectedRelations" @change="handleRelationChange">
        <el-checkbox label="prerequisites">前置知识</el-checkbox>
        <el-checkbox label="nextSteps">后续知识</el-checkbox>
        <el-checkbox label="related">相关知识</el-checkbox>
      </el-checkbox-group>
    </div>

    <!-- 重置按钮 -->
    <div class="filter-actions">
      <el-button type="primary" text @click="handleReset">
        <el-icon><Refresh /></el-icon>
        重置过滤器
      </el-button>
      <el-button type="success" text @click="handleSaveFilters">
        保存筛选
      </el-button>
    </div>

    <!-- 保存的筛选条件 -->
    <div v-if="savedFilters.length" class="filter-section">
      <div class="section-header">
        <h4>已保存的筛选</h4>
      </div>
      <div class="saved-filters">
        <el-tag
          v-for="filter in savedFilters"
          :key="filter.id"
          class="saved-filter"
          closable
          @click="handleApplyFilter(filter)"
          @close="handleDeleteFilter(filter)"
        >
          {{ filter.name }}
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useKnowledgeStore } from '../store'
import { categories, difficulties } from '../mock/data'
import { Refresh } from '@element-plus/icons-vue'
import type { KnowledgeNode, SavedFilter, FilterState } from '../types'
import { ElMessageBox } from 'element-plus'

const store = useKnowledgeStore()
const { nodes, selectedNode, filters } = storeToRefs(store)

// 本地状态
const searchQuery = ref('')
const selectedCategories = ref<string[]>([])
const selectedDifficulties = ref<string[]>([])
const learningStatus = ref<'all' | 'learning' | 'completed' | 'recommended'>('all')
const selectedRelations = ref<string[]>([])
const savedFilters = ref<SavedFilter[]>([])

// 计算属性
const filteredCount = computed(() => store.filteredNodes.length)

// 获取各分类的节点数量
const getCategoryCount = (category: string) => {
  return nodes.value.filter(node => node.category === category).length
}

// 获取各难度的节点数量
const getDifficultyCount = (difficulty: string) => {
  return nodes.value.filter(node => node.difficulty === difficulty).length
}

// 获取难度等级对应的星级
const getDifficultyLevel = (difficulty: string) => {
  const levels = {
    basic: 1,
    intermediate: 2,
    advanced: 3,
    expert: 4
  }
  return levels[difficulty as keyof typeof levels] || 1
}

// 监听过滤器变化
watch(() => filters.value, (newFilters) => {
  searchQuery.value = newFilters.search
  selectedCategories.value = newFilters.categories
  selectedDifficulties.value = newFilters.difficulties
  learningStatus.value = newFilters.learningStatus || 'all'
}, { deep: true })

// 事件处理
const handleSearch = () => {
  store.setFilters({ search: searchQuery.value })
}

const handleCategoryChange = () => {
  store.setFilters({ categories: selectedCategories.value })
}

const handleDifficultyChange = () => {
  store.setFilters({ difficulties: selectedDifficulties.value })
}

const handleStatusChange = () => {
  store.setFilters({ learningStatus: learningStatus.value })
}

const handleRelationChange = () => {
  if (!selectedNode.value) return
  store.setFilters({ 
    relations: {
      nodeId: selectedNode.value.id,
      types: selectedRelations.value
    }
  })
}

const handleReset = () => {
  searchQuery.value = ''
  selectedCategories.value = []
  selectedDifficulties.value = []
  learningStatus.value = 'all'
  selectedRelations.value = []
  store.resetFilters()
}

const handleSaveFilters = async () => {
  const name = await ElMessageBox.prompt('请输入筛选条件名称', '保存筛选', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
  })
  
  if (name.action === 'confirm') {
    const newFilter: SavedFilter = {
      id: Date.now(),
      name: name.value,
      filters: {
        search: searchQuery.value,
        categories: selectedCategories.value,
        difficulties: selectedDifficulties.value,
        learningStatus: learningStatus.value,
        relations: selectedRelations.value.length ? {
          nodeId: selectedNode.value?.id || '',
          types: selectedRelations.value
        } : undefined
      }
    }
    savedFilters.value.push(newFilter)
  }
}

const handleApplyFilter = (filter: SavedFilter) => {
  const { search, categories, difficulties, learningStatus: status, relations } = filter.filters
  searchQuery.value = search
  selectedCategories.value = categories
  selectedDifficulties.value = difficulties
  learningStatus.value = status as 'all' | 'learning' | 'completed' | 'recommended'
  if (relations && 'nodeId' in relations) {
    selectedRelations.value = relations.types
  } else {
    selectedRelations.value = []
  }
  store.setFilters(filter.filters)
}

const handleDeleteFilter = (filter: SavedFilter) => {
  savedFilters.value = savedFilters.value.filter(f => f.id !== filter.id)
}
</script>

<style scoped>
.graph-filters {
  display: flex;
  flex-direction: column;
  gap: 20px;
  height: 100%;
  overflow-y: auto;
  padding-right: 8px;
}

.filter-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(65, 184, 131, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header h4 {
  margin: 0;
  font-size: 14px;
  color: #e5eaf3;
  font-weight: 500;
}

.category-label,
.difficulty-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.color-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

:deep(.el-checkbox) {
  margin-right: 16px;
  margin-bottom: 8px;
  width: 100%;
}

:deep(.el-checkbox__label) {
  color: #e5eaf3;
  flex: 1;
}

:deep(.el-input__wrapper) {
  background: rgba(0, 0, 0, 0.2);
  box-shadow: none;
  border: 1px solid rgba(65, 184, 131, 0.2);
}

:deep(.el-input__wrapper:hover) {
  border-color: rgba(65, 184, 131, 0.4);
}

:deep(.el-input__inner) {
  color: #e5eaf3;
}

:deep(.el-input__inner::placeholder) {
  color: rgba(229, 234, 243, 0.4);
}

.filter-actions {
  display: flex;
  gap: 12px;
  margin-top: auto;
  padding: 16px;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  border: 1px solid rgba(65, 184, 131, 0.1);
}

.saved-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.saved-filter {
  cursor: pointer;
  transition: all 0.3s;
}

.saved-filter:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

:deep(.el-radio) {
  margin-right: 16px;
  margin-bottom: 8px;
}

:deep(.el-radio__label) {
  color: #e5eaf3;
}

:deep(.el-rate) {
  height: 16px;
}

:deep(.el-rate__item) {
  transform: scale(0.7);
}

:deep(.el-tag) {
  background: rgba(0, 0, 0, 0.2);
  border: none;
}

:deep(.el-button) {
  background: transparent;
  border: 1px solid rgba(65, 184, 131, 0.2);
}

:deep(.el-button:hover) {
  background: rgba(65, 184, 131, 0.1);
  border-color: rgba(65, 184, 131, 0.4);
}

:deep(.el-radio-group) {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

:deep(.el-checkbox-group) {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 8px;
}
</style> 