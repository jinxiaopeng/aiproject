<template>
  <div class="filters">
    <el-card class="filter-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>搜索</span>
        </div>
      </template>
      <el-input
        v-model="searchQuery"
        placeholder="搜索知识点..."
        clearable
        prefix-icon="Search"
        @input="handleSearch"
      />
    </el-card>

    <el-card class="filter-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>知识分类</span>
          <el-button text @click="resetFilters">重置</el-button>
        </div>
      </template>
      <el-checkbox-group v-model="selectedCategories" @change="handleCategoryChange">
        <div class="category-list">
          <div v-for="category in categories" :key="category" class="category-item">
            <el-checkbox :label="category">
              <div class="category-label">
                <span class="dot" :style="{ background: getCategoryColor(category) }"></span>
                {{ getCategoryLabel(category) }}
              </div>
            </el-checkbox>
          </div>
        </div>
      </el-checkbox-group>
    </el-card>

    <el-card class="filter-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>难度等级</span>
        </div>
      </template>
      <el-checkbox-group v-model="selectedDifficulties" @change="handleDifficultyChange">
        <div class="difficulty-list">
          <div v-for="difficulty in difficulties" :key="difficulty" class="difficulty-item">
            <el-checkbox :label="difficulty">
              <el-tag :type="getDifficultyType(difficulty)" size="small">
                {{ getDifficultyLabel(difficulty) }}
              </el-tag>
            </el-checkbox>
          </div>
        </div>
      </el-checkbox-group>
    </el-card>

    <el-card class="filter-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>布局设置</span>
        </div>
      </template>
      <div class="layout-controls">
        <el-radio-group v-model="layoutMode" @change="handleLayoutChange">
          <el-radio-button label="force">力导向布局</el-radio-button>
          <el-radio-button label="circular">环形布局</el-radio-button>
        </el-radio-group>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useKnowledgeGraphStore } from '../store'
import { Search } from '@element-plus/icons-vue'

const store = useKnowledgeGraphStore()
const { categories: storeCategories, difficulties: storeDifficulties } = storeToRefs(store)

// 状态
const searchQuery = ref('')
const selectedCategories = ref<string[]>([])
const selectedDifficulties = ref<string[]>([])
const layoutMode = ref<'force' | 'circular'>('force')

// 计算属性
const categories = computed(() => storeCategories.value)
const difficulties = computed(() => storeDifficulties.value)

// 方法
const getCategoryColor = (category: string) => {
  const colors: Record<string, string> = {
    'vulnerability': '#f56c6c',
    'concept': '#409eff',
    'tool': '#e6a23c',
    'technique': '#67c23a'
  }
  return colors[category] || '#909399'
}

const getCategoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    'vulnerability': '漏洞',
    'concept': '概念',
    'tool': '工具',
    'technique': '技术'
  }
  return labels[category] || category
}

const getDifficultyLabel = (difficulty: string) => {
  const labels: Record<string, string> = {
    'basic': '入门',
    'intermediate': '进阶',
    'advanced': '高级',
    'expert': '专家'
  }
  return labels[difficulty] || difficulty
}

const getDifficultyType = (difficulty: string) => {
  const types: Record<string, string> = {
    'basic': 'success',
    'intermediate': 'warning',
    'advanced': 'danger',
    'expert': ''
  }
  return types[difficulty] || 'info'
}

const handleSearch = () => {
  store.setFilters({ search: searchQuery.value })
}

const handleCategoryChange = () => {
  store.setFilters({ category: selectedCategories.value })
}

const handleDifficultyChange = () => {
  store.setFilters({ difficulty: selectedDifficulties.value })
}

const handleLayoutChange = () => {
  store.setLayoutMode(layoutMode.value)
}

const resetFilters = () => {
  searchQuery.value = ''
  selectedCategories.value = [...categories.value]
  selectedDifficulties.value = [...difficulties.value]
  store.clearFilters()
}
</script>

<style scoped>
.filters {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
  overflow-y: auto;
  padding-right: 8px;
}

.filter-card {
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #e5eaf3;
}

.category-list,
.difficulty-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.category-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e5eaf3;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.layout-controls {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1);
}

:deep(.el-input__inner) {
  color: #e5eaf3;
}

:deep(.el-checkbox__label) {
  color: #e5eaf3;
}

:deep(.el-radio-button__inner) {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: #e5eaf3;
}

:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: #409eff;
  border-color: #409eff;
  box-shadow: -1px 0 0 0 #409eff;
}

:deep(.el-tag) {
  background: transparent;
}

:deep(.el-tag--success) {
  border-color: rgba(103, 194, 58, 0.3);
  color: #67c23a;
}

:deep(.el-tag--warning) {
  border-color: rgba(230, 162, 60, 0.3);
  color: #e6a23c;
}

:deep(.el-tag--danger) {
  border-color: rgba(245, 108, 108, 0.3);
  color: #f56c6c;
}
</style> 