<template>
  <div class="course-header">
    <!-- 主标题区域 -->
    <div class="header-main">
      <div class="cyber-container">
        <div class="header-content">
          <div class="text-content">
            <h1>探索网络安全的世界</h1>
            <p class="subtitle">从基础到进阶的专业课程，助你成为网络安全专家</p>
          </div>
          <div class="header-stats">
            <div class="stat-item">
              <div class="stat-value">{{ totalCourses }}</div>
              <div class="stat-label">精品课程</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ totalStudents }}</div>
              <div class="stat-label">学习人数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ averageRating }}</div>
              <div class="stat-label">平均评分</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索和导航区域 -->
    <div class="search-nav">
      <div class="cyber-container">
        <!-- 搜索框 -->
        <div class="search-box">
          <el-input
            v-model="searchQuery"
            placeholder="搜索感兴趣的课程..."
            class="search-input"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>

        <!-- 热门搜索标签 -->
        <div class="hot-tags">
          <span v-for="tag in hotTags" 
                :key="tag"
                class="hot-tag"
                @click="handleTagClick(tag)"
          >
            {{ tag }}
          </span>
        </div>
      </div>
    </div>

    <!-- 分类导航 -->
    <div class="category-nav">
      <div class="cyber-container">
        <div class="nav-main">
          <div class="nav-categories">
            <span 
              v-for="category in categories" 
              :key="category.value"
              :class="['nav-item', { active: activeCategory === category.value }]"
              @click="handleCategoryClick(category.value)"
            >
              {{ category.label }}
            </span>
          </div>
          
          <div class="nav-levels">
            <span 
              v-for="level in levels" 
              :key="level.value"
              :class="['level-item', { active: activeLevel === level.value }]"
              @click="handleLevelClick(level.value)"
            >
              {{ level.label }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'

const props = defineProps<{
  totalCourses: number
  totalStudents: number
  averageRating: number
}>()

const emit = defineEmits<{
  (e: 'search', query: string): void
  (e: 'category-change', category: string): void
  (e: 'level-change', level: string): void
}>()

// 搜索相关
const searchQuery = ref('')
const hotTags = ['Web安全入门', 'XSS攻防', 'SQL注入', '渗透测试', 'CTF实战']

// 分类相关
const activeCategory = ref('all')
const categories = [
  { label: '全部课程', value: 'all' },
  { label: 'Web安全', value: 'web' },
  { label: '系统安全', value: 'system' },
  { label: '网络安全', value: 'network' },
  { label: '密码学', value: 'crypto' },
  { label: '安全开发', value: 'secure_dev' }
]

// 难度等级
const activeLevel = ref('')
const levels = [
  { label: '入门', value: 'beginner' },
  { label: '初级', value: 'elementary' },
  { label: '中级', value: 'intermediate' },
  { label: '高级', value: 'advanced' }
]

// 处理搜索
const handleSearch = () => {
  emit('search', searchQuery.value)
}

const handleTagClick = (tag: string) => {
  searchQuery.value = tag
  handleSearch()
}

// 处理分类点击
const handleCategoryClick = (category: string) => {
  activeCategory.value = category
  emit('category-change', category)
}

// 处理难度点击
const handleLevelClick = (level: string) => {
  activeLevel.value = activeLevel.value === level ? '' : level
  emit('level-change', activeLevel.value)
}
</script>

<style lang="scss" scoped>
.course-header {
  background: linear-gradient(to bottom, #1a1f3c, #0c1023);
  color: #fff;
  
  .header-main {
    padding: 40px 0;
    
    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .text-content {
        h1 {
          font-size: 2.5rem;
          font-weight: 600;
          margin: 0 0 1rem;
          background: linear-gradient(to right, #fff, #64ffda);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        
        .subtitle {
          font-size: 1.1rem;
          color: rgba(255, 255, 255, 0.7);
          margin: 0;
        }
      }
      
      .header-stats {
        display: flex;
        gap: 2rem;
        
        .stat-item {
          text-align: center;
          
          .stat-value {
            font-size: 1.75rem;
            font-weight: 600;
            color: #64ffda;
          }
          
          .stat-label {
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.6);
            margin-top: 0.25rem;
          }
        }
      }
    }
  }
  
  .search-nav {
    padding: 1rem 0;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.02);
    
    .search-box {
      max-width: 600px;
      margin: 0 auto;
      
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
            height: 40px;
            
            &::placeholder {
              color: rgba(255, 255, 255, 0.5);
            }
          }
        }
      }
    }
    
    .hot-tags {
      max-width: 600px;
      margin: 0.75rem auto 0;
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      
      .hot-tag {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.6);
        cursor: pointer;
        transition: all 0.3s ease;
        
        &:hover {
          color: #fff;
        }
        
        &:not(:last-child)::after {
          content: '|';
          margin-left: 0.5rem;
          color: rgba(255, 255, 255, 0.2);
        }
      }
    }
  }
  
  .category-nav {
    background: rgba(0, 0, 0, 0.2);
    padding: 0.5rem 0;
    
    .nav-main {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .nav-categories {
        display: flex;
        gap: 2rem;
        
        .nav-item {
          font-size: 1rem;
          color: rgba(255, 255, 255, 0.7);
          cursor: pointer;
          padding: 0.5rem 0;
          position: relative;
          
          &::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--el-color-primary);
            transform: scaleX(0);
            transition: transform 0.3s ease;
          }
          
          &:hover {
            color: #fff;
          }
          
          &.active {
            color: var(--el-color-primary);
            
            &::after {
              transform: scaleX(1);
            }
          }
        }
      }
      
      .nav-levels {
        display: flex;
        gap: 1rem;
        
        .level-item {
          font-size: 0.9rem;
          color: rgba(255, 255, 255, 0.6);
          cursor: pointer;
          padding: 0.25rem 0.75rem;
          border-radius: 4px;
          transition: all 0.3s ease;
          
          &:hover {
            color: #fff;
            background: rgba(255, 255, 255, 0.1);
          }
          
          &.active {
            color: #fff;
            background: var(--el-color-primary);
          }
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 1024px) {
  .course-header {
    .header-main {
      .header-content {
        flex-direction: column;
        text-align: center;
        gap: 2rem;
        
        .text-content {
          h1 {
            font-size: 2rem;
          }
        }
      }
    }
    
    .category-nav {
      .nav-main {
        flex-direction: column;
        gap: 1rem;
        
        .nav-categories {
          width: 100%;
          overflow-x: auto;
          padding-bottom: 0.5rem;
          
          &::-webkit-scrollbar {
            display: none;
          }
        }
        
        .nav-levels {
          width: 100%;
          justify-content: center;
          flex-wrap: wrap;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .course-header {
    .header-main {
      padding: 30px 0;
      
      .header-content {
        .text-content {
          h1 {
            font-size: 1.75rem;
          }
          
          .subtitle {
            font-size: 1rem;
          }
        }
        
        .header-stats {
          gap: 1.5rem;
          
          .stat-item {
            .stat-value {
              font-size: 1.5rem;
            }
          }
        }
      }
    }
  }
}
</style> 