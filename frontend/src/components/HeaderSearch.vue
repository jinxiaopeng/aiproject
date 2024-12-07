<template>
  <div class="header-search">
    <el-popover
      v-model:visible="showSearchResults"
      placement="bottom-start"
      :width="400"
      trigger="click"
      popper-class="search-popover"
      @show="handlePopoverShow"
      @hide="handlePopoverHide"
    >
      <template #reference>
        <el-input
          v-model="searchKeyword"
          class="search-input"
          placeholder="搜索课程/实验/知识..."
          :prefix-icon="Search"
          @input="handleSearch"
          @focus="handleFocus"
          @keydown.down.prevent="handleKeyDown"
          @keydown.up.prevent="handleKeyUp"
          @keydown.enter="handleEnterKey"
          @keydown.esc="showSearchResults = false"
        />
      </template>

      <div class="search-results" v-loading="loading">
        <template v-if="searchKeyword && !loading">
          <div v-if="results.length > 0">
            <div v-for="(group, category) in groupedResults" :key="category" class="result-group">
              <div class="category-title">{{ categoryTitles[category] }}</div>
              <div
                v-for="(item, index) in group"
                :key="item.id"
                class="result-item"
                :class="{ 'is-active': isActiveResult(category, index) }"
                @click="handleResultClick(item)"
                @mouseenter="activeCategory = category; activeIndex = index"
              >
                <el-icon :size="16" class="item-icon">
                  <component :is="getCategoryIcon(category)" />
                </el-icon>
                <div class="item-content">
                  <div class="item-title">{{ item.title }}</div>
                  <div class="item-desc">{{ item.description }}</div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="no-results">
            <el-empty description="未找到相关内容" />
          </div>
        </template>
        <template v-else-if="!searchKeyword">
          <div v-if="searchHistory.length > 0" class="search-history">
            <div class="history-header">
              <span class="history-title">搜索历史</span>
              <el-button
                type="text"
                size="small"
                @click="clearHistory"
                class="clear-history"
              >
                清空历史
              </el-button>
            </div>
            <div class="history-list">
              <div
                v-for="(item, index) in searchHistory"
                :key="index"
                class="history-item"
                @click="quickSearch(item)"
              >
                <el-icon><Timer /></el-icon>
                <span>{{ item }}</span>
                <el-icon
                  class="delete-icon"
                  @click.stop="removeHistoryItem(index)"
                >
                  <Close />
                </el-icon>
              </div>
            </div>
          </div>
          <div class="search-placeholder">
            <div class="placeholder-title">搜索建议</div>
            <div class="quick-searches">
              <el-tag
                v-for="tag in quickSearchTags"
                :key="tag"
                class="quick-search-tag"
                @click="quickSearch(tag)"
              >
                {{ tag }}
              </el-tag>
            </div>
          </div>
        </template>
      </div>

      <div v-if="loading" class="loading-indicator">
        <el-icon class="loading-icon" :size="24"><Loading /></el-icon>
        <span>正在搜索...</span>
      </div>
    </el-popover>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Reading, Monitor, Share, Timer, Close, Loading } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { debounce } from 'lodash-es'

const HISTORY_KEY = 'search_history'
const MAX_HISTORY = 10

const router = useRouter()
const searchKeyword = ref('')
const showSearchResults = ref(false)
const loading = ref(false)
const results = ref<any[]>([])
const activeCategory = ref('')
const activeIndex = ref(-1)
const searchHistory = ref<string[]>([])

// 从localStorage加载搜索历史
const loadSearchHistory = () => {
  const history = localStorage.getItem(HISTORY_KEY)
  if (history) {
    searchHistory.value = JSON.parse(history)
  }
}

// 保存搜索历史到localStorage
const saveSearchHistory = () => {
  localStorage.setItem(HISTORY_KEY, JSON.stringify(searchHistory.value))
}

// 添加搜索历史
const addToHistory = (keyword: string) => {
  if (!keyword.trim()) return
  const index = searchHistory.value.indexOf(keyword)
  if (index > -1) {
    searchHistory.value.splice(index, 1)
  }
  searchHistory.value.unshift(keyword)
  if (searchHistory.value.length > MAX_HISTORY) {
    searchHistory.value.pop()
  }
  saveSearchHistory()
}

// 删除单个历史记录
const removeHistoryItem = (index: number) => {
  searchHistory.value.splice(index, 1)
  saveSearchHistory()
}

// 清空搜索历史
const clearHistory = () => {
  searchHistory.value = []
  saveSearchHistory()
}

// 快速搜索标签
const quickSearchTags = [
  'SQL注入',
  'XSS攻击',
  'CSRF防护',
  '密码学基础',
  'Web安全',
  '渗透测试'
]

// 分类标题映射
const categoryTitles = {
  courses: '课程',
  labs: '实验',
  knowledge: '知识'
}

// 获取分类图标
const getCategoryIcon = (category: string) => {
  const iconMap: Record<string, any> = {
    courses: Reading,
    labs: Monitor,
    knowledge: Share
  }
  return iconMap[category]
}

// 对搜索结果进行分组
const groupedResults = computed(() => {
  return results.value.reduce((groups: Record<string, any[]>, item) => {
    if (!groups[item.category]) {
      groups[item.category] = []
    }
    groups[item.category].push(item)
    return groups
  }, {})
})

// 判断是否是当前激活的结果项
const isActiveResult = (category: string, index: number) => {
  return activeCategory.value === category && activeIndex.value === index
}

// 获取所有结果项的扁平列表
const flatResults = computed(() => {
  const flat: { category: string; index: number; item: any }[] = []
  Object.entries(groupedResults.value).forEach(([category, items]) => {
    items.forEach((item, index) => {
      flat.push({ category, index, item })
    })
  })
  return flat
})

// 处理键盘向下导航
const handleKeyDown = () => {
  const total = flatResults.value.length
  if (total === 0) return

  let currentIndex = -1
  for (let i = 0; i < total; i++) {
    if (isActiveResult(flatResults.value[i].category, flatResults.value[i].index)) {
      currentIndex = i
      break
    }
  }

  const nextIndex = currentIndex === total - 1 ? 0 : currentIndex + 1
  const next = flatResults.value[nextIndex]
  activeCategory.value = next.category
  activeIndex.value = next.index
}

// 处理键盘向上导航
const handleKeyUp = () => {
  const total = flatResults.value.length
  if (total === 0) return

  let currentIndex = -1
  for (let i = 0; i < total; i++) {
    if (isActiveResult(flatResults.value[i].category, flatResults.value[i].index)) {
      currentIndex = i
      break
    }
  }

  const prevIndex = currentIndex <= 0 ? total - 1 : currentIndex - 1
  const prev = flatResults.value[prevIndex]
  activeCategory.value = prev.category
  activeIndex.value = prev.index
}

// 处理回车键
const handleEnterKey = () => {
  const activeResult = flatResults.value.find(
    r => isActiveResult(r.category, r.index)
  )
  
  if (activeResult) {
    handleResultClick(activeResult.item)
  } else if (results.value.length > 0) {
    handleResultClick(results.value[0])
  }
}

// 模拟搜索API调用
const searchAPI = async (keyword: string) => {
  // 这里替换为实际的API调用
  await new Promise(resolve => setTimeout(resolve, 500))
  return [
    {
      id: 1,
      category: 'courses',
      title: 'Web安全基础课程',
      description: '介绍Web安全的基本概念和防护方法',
      path: '/courses/1'
    },
    {
      id: 2,
      category: 'labs',
      title: 'SQL注入实验',
      description: '动手实践SQL注入攻击与防御',
      path: '/labs/2'
    },
    {
      id: 3,
      category: 'knowledge',
      title: 'XSS攻击原理',
      description: '深入理解XSS攻击的原理和防御措施',
      path: '/knowledge/3'
    }
  ].filter(item => 
    item.title.toLowerCase().includes(keyword.toLowerCase()) ||
    item.description.toLowerCase().includes(keyword.toLowerCase())
  )
}

// 防抖处理的搜索函数
const handleSearch = debounce(async () => {
  if (!searchKeyword.value) {
    results.value = []
    return
  }

  loading.value = true
  try {
    results.value = await searchAPI(searchKeyword.value)
    // 重置选中状态
    activeCategory.value = results.value[0]?.category || ''
    activeIndex.value = 0
  } catch (error) {
    console.error('搜索失败:', error)
    ElMessage.error('搜索失败，请稍后重试')
    results.value = []
  } finally {
    loading.value = false
  }
}, 300)

// 处理搜索结果点击
const handleResultClick = (item: any) => {
  addToHistory(searchKeyword.value)
  router.push(item.path)
  showSearchResults.value = false
  searchKeyword.value = ''
}

// 快速搜索
const quickSearch = (tag: string) => {
  searchKeyword.value = tag
  handleSearch()
}

// 处理搜索框获得焦点
const handleFocus = () => {
  showSearchResults.value = true
  if (!activeCategory.value && results.value.length > 0) {
    activeCategory.value = results.value[0].category
    activeIndex.value = 0
  }
}

// 处理弹窗显示
const handlePopoverShow = () => {
  document.addEventListener('click', handleClickOutside)
}

// 处理弹窗隐藏
const handlePopoverHide = () => {
  document.removeEventListener('click', handleClickOutside)
}

// 处理点击外部关闭
const handleClickOutside = (event: MouseEvent) => {
  const popover = document.querySelector('.search-popover')
  const input = document.querySelector('.header-search')
  if (popover && input && 
      !popover.contains(event.target as Node) && 
      !input.contains(event.target as Node)) {
    showSearchResults.value = false
  }
}

onMounted(() => {
  loadSearchHistory()
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style lang="scss" scoped>
.header-search {
  .search-input {
    width: 200px;

    :deep(.el-input__wrapper) {
      background: rgba(10, 25, 47, 0.6);
      border: 1px solid rgba(100, 255, 218, 0.1);
      box-shadow: none !important;
      transition: all 0.3s ease;
      
      &:hover {
        background: rgba(10, 25, 47, 0.8);
        border-color: rgba(100, 255, 218, 0.2);
      }
      
      &:focus-within {
        background: rgba(10, 25, 47, 1);
        border-color: rgba(100, 255, 218, 0.3);
      }
    }

    :deep(.el-input__inner) {
      color: #e6f1ff;
      
      &::placeholder {
        color: #8892b0;
      }
    }

    :deep(.el-input__prefix-inner) {
      color: #8892b0;
    }
  }
}

:deep(.search-popover) {
  padding: 0;
  background: rgba(10, 25, 47, 0.95);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(100, 255, 218, 0.1);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.search-results {
  max-height: 400px;
  overflow-y: auto;
  padding: 12px;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(100, 255, 218, 0.1);
    border-radius: 3px;
    
    &:hover {
      background: rgba(100, 255, 218, 0.2);
    }
  }
}

.result-group {
  & + .result-group {
    margin-top: 16px;
  }

  .category-title {
    color: #8892b0;
    font-size: 12px;
    margin-bottom: 8px;
    padding-left: 8px;
  }
}

.result-item {
  display: flex;
  align-items: flex-start;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover, &.is-active {
    background: rgba(100, 255, 218, 0.05);
  }

  .item-icon {
    margin-right: 12px;
    margin-top: 2px;
    color: #64ffda;
  }

  .item-content {
    flex: 1;
    min-width: 0;

    .item-title {
      color: #e6f1ff;
      font-size: 14px;
      margin-bottom: 4px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .item-desc {
      color: #8892b0;
      font-size: 12px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
}

.search-history {
  margin-bottom: 16px;
  
  .history-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    padding: 0 8px;

    .history-title {
      color: #8892b0;
      font-size: 12px;
    }

    .clear-history {
      color: #64ffda;
      font-size: 12px;
      padding: 0;

      &:hover {
        color: #9effed;
      }
    }
  }

  .history-list {
    .history-item {
      display: flex;
      align-items: center;
      padding: 6px 8px;
      color: #e6f1ff;
      cursor: pointer;
      transition: all 0.3s ease;

      .el-icon {
        font-size: 14px;
        color: #8892b0;
        margin-right: 8px;
      }

      span {
        flex: 1;
        font-size: 13px;
      }

      .delete-icon {
        margin-right: 0;
        opacity: 0;
        transition: opacity 0.3s ease;

        &:hover {
          color: #64ffda;
        }
      }

      &:hover {
        background: rgba(100, 255, 218, 0.05);

        .delete-icon {
          opacity: 1;
        }
      }
    }
  }
}

.search-placeholder {
  padding: 8px;

  .placeholder-title {
    color: #8892b0;
    font-size: 12px;
    margin-bottom: 12px;
  }

  .quick-searches {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;

    .quick-search-tag {
      cursor: pointer;
      background: rgba(10, 25, 47, 0.6);
      border: 1px solid rgba(100, 255, 218, 0.1);
      color: #e6f1ff;
      transition: all 0.3s ease;

      &:hover {
        background: rgba(10, 25, 47, 0.8);
        border-color: rgba(100, 255, 218, 0.2);
      }
    }
  }
}

.no-results {
  padding: 24px 0;
  color: #8892b0;
  text-align: center;
}

:deep(.el-empty) {
  padding: 24px 0;
  
  .el-empty__description {
    color: #8892b0;
  }
}

.loading-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: #64ffda;

  .loading-icon {
    animation: rotate 1s linear infinite;
  }

  span {
    font-size: 14px;
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

:deep(.el-loading-mask) {
  background-color: rgba(10, 25, 47, 0.9);
}
</style> 