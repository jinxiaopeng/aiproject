<template>
  <div class="course-filter">
    <div class="filter-group">
      <el-select
        v-model="filterForm.category"
        placeholder="课程分类"
        clearable
        class="filter-item"
        @change="handleFilterChange"
      >
        <el-option
          v-for="item in categories"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>

      <el-select
        v-model="filterForm.difficulty"
        placeholder="难度等级"
        clearable
        class="filter-item"
        @change="handleFilterChange"
      >
        <el-option
          v-for="item in difficulties"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
      </el-select>

      <el-select
        v-model="filterForm.sort_by"
        placeholder="排序方式"
        class="filter-item"
        @change="handleFilterChange"
      >
        <el-option label="最新" value="newest" />
        <el-option label="最热" value="popular" />
        <el-option label="评分" value="rating" />
      </el-select>
    </div>

    <div class="search-group">
      <el-input
        v-model="searchQuery"
        placeholder="搜索课程..."
        class="search-input"
        clearable
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { Search } from '@element-plus/icons-vue'

// 分类和难度选项
const categories = [
  { label: 'Web安全', value: 'web' },
  { label: '系统安全', value: 'system' },
  { label: '网络安全', value: 'network' },
  { label: '密码学', value: 'crypto' },
  { label: '安全开发', value: 'secure_dev' }
]

const difficulties = [
  { label: '入门', value: 'beginner' },
  { label: '初级', value: 'elementary' },
  { label: '中级', value: 'intermediate' },
  { label: '高级', value: 'advanced' },
  { label: '专家', value: 'expert' }
]

const emit = defineEmits<{
  (e: 'filter', filters: any): void
  (e: 'search', query: string): void
}>()

// 筛选表单
const filterForm = reactive({
  category: '',
  difficulty: '',
  sort_by: 'newest' as const
})

const searchQuery = ref('')

// 处理筛选变化
const handleFilterChange = () => {
  emit('filter', { ...filterForm })
}

// 处理搜索
const handleSearch = () => {
  emit('search', searchQuery.value)
}
</script>

<style lang="scss" scoped>
.course-filter {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
  
  .filter-group {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;

    .filter-item {
      width: 160px;
      
      :deep(.el-input__wrapper) {
        background: rgba(255, 255, 255, 0.05);
        box-shadow: none;
        border: 1px solid rgba(255, 255, 255, 0.1);
        
        &:hover {
          border-color: rgba(255, 255, 255, 0.2);
        }
        
        &.is-focus {
          border-color: var(--el-color-primary);
        }
      }
      
      :deep(.el-input__inner) {
        color: #fff;
        
        &::placeholder {
          color: rgba(255, 255, 255, 0.5);
        }
      }
    }
  }
  
  .search-group {
    width: 300px;
    
    :deep(.el-input__wrapper) {
      background: rgba(255, 255, 255, 0.05);
      box-shadow: none;
      border: 1px solid rgba(255, 255, 255, 0.1);
      
      &:hover {
        border-color: rgba(255, 255, 255, 0.2);
      }
      
      &.is-focus {
        border-color: var(--el-color-primary);
      }
    }
    
    :deep(.el-input__inner) {
      color: #fff;
      
      &::placeholder {
        color: rgba(255, 255, 255, 0.5);
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .course-filter {
    flex-direction: column;
    
    .filter-group {
      width: 100%;
      
      .filter-item {
        width: 100%;
      }
    }
    
    .search-group {
      width: 100%;
    }
  }
}
</style> 