<template>
  <div class="filters">
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
                {{ category }}
              </div>
            </el-checkbox>
          </div>
        </div>
      </el-checkbox-group>
    </el-card>

    <el-card class="difficulty-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span>难度等级</span>
        </div>
      </template>
      <el-checkbox-group v-model="selectedDifficulties" @change="handleDifficultyChange">
        <div class="difficulty-list">
          <el-checkbox label="入门">
            <el-tag size="small" type="success">入门</el-tag>
          </el-checkbox>
          <el-checkbox label="进阶">
            <el-tag size="small" type="warning">进阶</el-tag>
          </el-checkbox>
          <el-checkbox label="高级">
            <el-tag size="small" type="danger">高级</el-tag>
          </el-checkbox>
        </div>
      </el-checkbox-group>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useKnowledgeGraphStore } from '../store'

const store = useKnowledgeGraphStore()

// 状态
const categories = ['领域', '漏洞', '技能', '工具']
const selectedCategories = ref(categories)
const selectedDifficulties = ref(['入门', '进阶', '高级'])

// 方法
const getCategoryColor = (category: string) => {
  const colors = {
    '领域': '#67C23A',
    '漏洞': '#F56C6C',
    '技能': '#409EFF',
    '工具': '#E6A23C'
  }
  return colors[category] || '#909399'
}

const handleCategoryChange = () => {
  store.setFilters({
    categories: selectedCategories.value,
    difficulties: selectedDifficulties.value
  })
}

const handleDifficultyChange = () => {
  store.setFilters({
    categories: selectedCategories.value,
    difficulties: selectedDifficulties.value
  })
}

const resetFilters = () => {
  selectedCategories.value = [...categories]
  selectedDifficulties.value = ['入门', '进阶', '高级']
  handleCategoryChange()
}
</script>

<style scoped>
.filters {
  display: flex;
  flex-direction: column;
  gap: 16px;
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
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}
</style> 