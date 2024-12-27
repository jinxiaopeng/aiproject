<template>
  <div class="search-box">
    <div class="search-input-wrapper">
      <el-input
        v-model="searchQuery"
        placeholder="搜索感兴趣的课程..."
        class="search-input"
        clearable
        @input="handleInput"
        @keyup.enter="handleSearch"
        @clear="handleClear"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      
      <!-- 搜索建议下拉框 -->
      <div v-if="showSuggestions && (suggestions.length > 0 || searchHistory.length > 0)" class="suggestions-dropdown">
        <!-- 搜索建议 -->
        <template v-if="suggestions.length > 0">
          <div class="suggestions-section">
            <div class="section-title">
              <el-icon><Search /></el-icon>
              <span>搜索建议</span>
            </div>
            <div
              v-for="suggestion in suggestions"
              :key="suggestion"
              class="suggestion-item"
              @click="selectSuggestion(suggestion)"
            >
              <el-icon><Search /></el-icon>
              <span v-html="highlightMatch(suggestion)"></span>
            </div>
          </div>
        </template>

        <!-- 搜索历史 -->
        <div v-if="searchHistory.length > 0" class="history-section">
          <div class="section-title">
            <el-icon><Timer /></el-icon>
            <span>搜索历史</span>
            <el-button
              link
              type="primary"
              class="clear-history"
              @click.stop="clearHistory"
            >
              清空历史
            </el-button>
          </div>
          <div
            v-for="item in searchHistory"
            :key="item"
            class="history-item"
            @click="selectHistory(item)"
          >
            <el-icon><Timer /></el-icon>
            <span>{{ item }}</span>
            <el-icon
              class="delete-icon"
              @click.stop="removeHistoryItem(item)"
            >
              <Close />
            </el-icon>
          </div>
        </div>
      </div>
    </div>

    <!-- 热门搜索标签 -->
    <div class="hot-searches">
      <span class="label">热门搜索：</span>
      <span
        v-for="tag in hotSearches"
        :key="tag"
        class="hot-tag"
        @click="selectHotSearch(tag)"
      >
        {{ tag }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { Search, Timer, Close } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const props = defineProps<{
  hotSearches: string[]
}>()

const emit = defineEmits<{
  (e: 'search', query: string): void
}>()

const searchQuery = ref('')
const showSuggestions = ref(false)
const searchHistory = ref<string[]>([])
const router = useRouter()

// 从 localStorage 加载搜索历史
const loadSearchHistory = () => {
  const history = localStorage.getItem('courseSearchHistory')
  if (history) {
    searchHistory.value = JSON.parse(history)
  }
}

// 保存搜索历史到 localStorage
const saveSearchHistory = () => {
  localStorage.setItem('courseSearchHistory', JSON.stringify(searchHistory.value))
}

// 添加搜索历史
const addToHistory = (query: string) => {
  if (!query.trim()) return
  
  // 移除已存在的相同搜索词
  searchHistory.value = searchHistory.value.filter(item => item !== query)
  
  // 添加到历史记录开头
  searchHistory.value.unshift(query)
  
  // 限制���史记录数量为10条
  if (searchHistory.value.length > 10) {
    searchHistory.value.pop()
  }
  
  saveSearchHistory()
}

// 删除单个历史记录
const removeHistoryItem = (item: string) => {
  searchHistory.value = searchHistory.value.filter(i => i !== item)
  saveSearchHistory()
}

// 清空所有历史记录
const clearHistory = () => {
  searchHistory.value = []
  saveSearchHistory()
  ElMessage.success('搜索历史已清空')
}

// 模拟搜索建议
const suggestions = computed(() => {
  if (!searchQuery.value.trim()) return []
  
  // 这里可以根据实际需求调用后端API取建议
  // 现在用热门搜索做简单的模拟
  return props.hotSearches.filter(item =>
    item.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 高亮匹配文本
const highlightMatch = (text: string) => {
  if (!searchQuery.value.trim()) return text
  
  const regex = new RegExp(`(${searchQuery.value})`, 'gi')
  return text.replace(regex, '<span class="highlight">$1</span>')
}

// 处理搜索
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    addToHistory(searchQuery.value)
  }
  emit('search', searchQuery.value)
  showSuggestions.value = false
}

// 处理输入
const handleInput = () => {
  showSuggestions.value = true
  emit('search', searchQuery.value)
}

// 处理清空
const handleClear = () => {
  searchQuery.value = ''
  emit('search', '')
  showSuggestions.value = false
}

// 选择搜索建议
const selectSuggestion = (course: any) => {
  if (typeof course === 'string') {
    // 如果是热门搜索标签
    searchQuery.value = course
    addToHistory(course)
    emit('search', course)
    // 滚动到课程列表
    nextTick(() => {
      const coursesSection = document.querySelector('.all-courses-section')
      if (coursesSection) {
        coursesSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    })
  } else {
    // 如果是课程建议
    searchQuery.value = course.title
    addToHistory(course.title)
    showSuggestions.value = false
    // 直接跳转到课程详情页
    router.push(`/courses/${course.id}`)
  }
}

// 选择历史记录
const selectHistory = (item: string) => {
  searchQuery.value = item
  addToHistory(item)
  emit('search', item)
  showSuggestions.value = false
}

// 点击外部关闭建议框
const handleClickOutside = (event: MouseEvent) => {
  const searchBox = document.querySelector('.search-box')
  if (searchBox && !searchBox.contains(event.target as Node)) {
    showSuggestions.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  loadSearchHistory()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// 处理热门搜索标签点击
const selectHotSearch = (tag: string) => {
  searchQuery.value = tag
  addToHistory(tag)
  showSuggestions.value = true
  // 触发搜索以显示搜索建议
  emit('search', tag)
}
</script>

<style lang="scss" scoped>
.search-box {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
  
  .search-input-wrapper {
    position: relative;
    
    .search-input {
      :deep(.el-input__wrapper) {
        background: rgba(255, 255, 255, 0.1);
        border: none;
        box-shadow: none;
        
        &:hover, &:focus {
          background: rgba(255, 255, 255, 0.15);
        }
        
        .el-input__inner {
          color: #fff;
          height: 50px;
          font-size: 1.1rem;
          
          &::placeholder {
            color: rgba(255, 255, 255, 0.5);
          }
        }
      }
    }
  }
  
  .suggestions-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: #1a1f3c;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    margin-top: 8px;
    padding: 8px 0;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    
    .section-title {
      display: flex;
      align-items: center;
      padding: 8px 16px;
      color: rgba(255, 255, 255, 0.5);
      font-size: 0.9rem;
      
      .el-icon {
        margin-right: 8px;
      }
      
      .clear-history {
        margin-left: auto;
        font-size: 0.9rem;
      }
    }
    
    .suggestion-item,
    .history-item {
      display: flex;
      align-items: center;
      padding: 8px 16px;
      cursor: pointer;
      color: rgba(255, 255, 255, 0.8);
      
      &:hover {
        background: rgba(255, 255, 255, 0.05);
      }
      
      .el-icon {
        margin-right: 8px;
        font-size: 1rem;
      }
      
      .highlight {
        color: var(--el-color-primary);
        font-weight: bold;
      }
    }
    
    .history-item {
      .delete-icon {
        margin-left: auto;
        opacity: 0;
        transition: opacity 0.2s;
      }
      
      &:hover .delete-icon {
        opacity: 1;
      }
    }
  }
  
  .hot-searches {
    margin-top: 1rem;
    text-align: center;
    
    .label {
      color: rgba(255, 255, 255, 0.5);
      margin-right: 1rem;
    }
    
    .hot-tag {
      color: rgba(255, 255, 255, 0.7);
      cursor: pointer;
      transition: all 0.3s ease;
      margin: 0 0.5rem;
      
      &:hover {
        color: #fff;
      }
      
      &:not(:last-child)::after {
        content: '|';
        margin-left: 1rem;
        color: rgba(255, 255, 255, 0.2);
      }
    }
  }
}
</style> 