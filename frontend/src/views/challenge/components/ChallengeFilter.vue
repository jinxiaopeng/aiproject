<template>
  <div class="challenge-filter cyber-filter">
    <!-- 搜索框 -->
    <div class="search-box">
      <el-input
        v-model="searchQuery"
        placeholder="搜索靶场..."
        clearable
        @input="handleFilterChange"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- 分类过滤器 -->
    <div class="filter-section">
      <h3>分类</h3>
      <div class="tag-group">
        <el-tag
          v-for="category in categories"
          :key="category.value"
          :type="selectedCategories.includes(category.value) ? '' : 'info'"
          :effect="selectedCategories.includes(category.value) ? 'dark' : 'plain'"
          class="filter-tag"
          @click="toggleCategory(category.value)"
        >
          {{ category.label }}
        </el-tag>
      </div>
    </div>

    <!-- 难度过滤器 -->
    <div class="filter-section">
      <h3>难度</h3>
      <div class="tag-group">
        <el-tag
          v-for="level in difficultyLevels"
          :key="level.value"
          :type="getDifficultyType(level.value)"
          :effect="selectedDifficulty === level.value ? 'dark' : 'plain'"
          class="filter-tag"
          @click="toggleDifficulty(level.value)"
        >
          {{ level.label }}
        </el-tag>
      </div>
    </div>

    <!-- 状态过滤器 -->
    <div class="filter-section">
      <h3>状态</h3>
      <div class="tag-group">
        <el-tag
          v-for="status in statusOptions"
          :key="status.value"
          :type="selectedStatus === status.value ? 'success' : 'info'"
          :effect="selectedStatus === status.value ? 'dark' : 'plain'"
          class="filter-tag"
          @click="toggleStatus(status.value)"
        >
          {{ status.label }}
        </el-tag>
      </div>
    </div>

    <!-- 重置按钮 -->
    <div class="filter-actions">
      <el-button 
        type="primary" 
        :icon="Refresh"
        @click="resetFilters"
      >
        重置筛选
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Search, Refresh } from '@element-plus/icons-vue'

// 定义过滤器的数据结构
interface FilterState {
  categories: string[]
  difficulty: string | null
  status: string | null
  search: string
}

// Props 定义
interface Props {
  initialFilters?: Partial<FilterState>
}

const props = withDefaults(defineProps<Props>(), {
  initialFilters: () => ({})
})

// Emits
const emit = defineEmits<{
  (e: 'filter-change', filters: FilterState): void
}>()

// 搜索查询
const searchQuery = ref('')

// 分类选项
const categories = [
  { label: 'Web安全', value: 'web' },
  { label: '系统安全', value: 'system' },
  { label: '密码学', value: 'crypto' },
  { label: '逆向工程', value: 'reverse' },
  { label: '二进制', value: 'binary' },
  { label: '移动安全', value: 'mobile' }
]

// 难度等级
const difficultyLevels = [
  { label: '入门', value: 'beginner' },
  { label: '简单', value: 'easy' },
  { label: '中等', value: 'medium' },
  { label: '困难', value: 'hard' },
  { label: '专家', value: 'expert' }
]

// 状态选项
const statusOptions = [
  { label: '全部', value: 'all' },
  { label: '未开始', value: 'not_started' },
  { label: '进行中', value: 'in_progress' },
  { label: '已完成', value: 'completed' }
]

// 选中的过滤条件
const selectedCategories = ref<string[]>([])
const selectedDifficulty = ref<string | null>(null)
const selectedStatus = ref<string | null>('all')

// 获取难度标签类型
const getDifficultyType = (difficulty: string): string => {
  const types: Record<string, string> = {
    beginner: 'info',
    easy: 'success',
    medium: 'warning',
    hard: 'danger',
    expert: 'danger'
  }
  return types[difficulty] || 'info'
}

// 切换分类
const toggleCategory = (category: string) => {
  const index = selectedCategories.value.indexOf(category)
  if (index === -1) {
    selectedCategories.value.push(category)
  } else {
    selectedCategories.value.splice(index, 1)
  }
  handleFilterChange()
}

// 切换难度
const toggleDifficulty = (difficulty: string) => {
  selectedDifficulty.value = selectedDifficulty.value === difficulty ? null : difficulty
  handleFilterChange()
}

// 切换状态
const toggleStatus = (status: string) => {
  selectedStatus.value = selectedStatus.value === status ? null : status
  handleFilterChange()
}

// 重置过滤器
const resetFilters = () => {
  searchQuery.value = ''
  selectedCategories.value = []
  selectedDifficulty.value = null
  selectedStatus.value = 'all'
  handleFilterChange()
}

// 处理过滤器变化
const handleFilterChange = () => {
  emit('filter-change', {
    categories: selectedCategories.value,
    difficulty: selectedDifficulty.value,
    status: selectedStatus.value,
    search: searchQuery.value
  })
}

// 监听初始过滤器变化
watch(() => props.initialFilters, (newFilters) => {
  if (newFilters.categories) {
    selectedCategories.value = newFilters.categories
  }
  if (newFilters.difficulty) {
    selectedDifficulty.value = newFilters.difficulty
  }
  if (newFilters.status) {
    selectedStatus.value = newFilters.status
  }
  if (newFilters.search) {
    searchQuery.value = newFilters.search
  }
}, { immediate: true })
</script>

<style scoped lang="scss">
.cyber-filter {
  padding: 20px;
  background: rgba(16, 16, 24, 0.95);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 255, 157, 0.1);

  .search-box {
    margin-bottom: 20px;

    :deep(.el-input) {
      .el-input__wrapper {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--border-color);
        box-shadow: none;

        &:hover, &:focus {
          border-color: var(--primary-color);
        }
      }

      .el-input__inner {
        color: var(--text-color);
        
        &::placeholder {
          color: var(--text-secondary);
        }
      }
    }
  }

  .filter-section {
    margin-bottom: 20px;

    h3 {
      color: var(--text-color);
      font-size: 16px;
      margin-bottom: 12px;
      font-weight: 500;
    }

    .tag-group {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;

      .filter-tag {
        cursor: pointer;
        transition: all 0.3s ease;
        
        &:hover {
          transform: translateY(-2px);
        }
      }
    }
  }

  .filter-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;

    .el-button {
      background: var(--primary-color);
      border: none;
      
      &:hover {
        background: var(--primary-hover);
        transform: translateY(-2px);
      }
    }
  }

  &:hover {
    border-color: var(--primary-color);
    box-shadow: 0 0 30px rgba(0, 255, 157, 0.2);
  }
}

// 响应式布局
@media (max-width: 768px) {
  .cyber-filter {
    .tag-group {
      .filter-tag {
        margin-bottom: 8px;
      }
    }
  }
}
</style> 