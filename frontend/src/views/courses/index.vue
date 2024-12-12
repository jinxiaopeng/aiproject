<template>
  <div class="cyber-courses">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="cyber-container">
        <div class="header-content text-center">
          <h1 class="main-title">探索网络安全的世界</h1>
          <p class="subtitle">从基础到进阶的专业课程，助你成为网络安全专家</p>
          
          <!-- 统计数据 -->
          <div class="stats-bar">
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

    <!-- 搜索和分类导航 -->
    <div class="nav-section">
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
          
          <!-- 热门搜索 -->
          <div class="hot-searches">
            <span class="label">热门搜索：</span>
            <span 
              v-for="tag in hotSearches" 
              :key="tag"
              class="hot-tag"
              @click="handleTagClick(tag)"
            >
              {{ tag }}
            </span>
          </div>
        </div>

        <!-- 分类导航 -->
        <div class="category-nav">
          <div class="nav-list">
            <span 
              v-for="category in categories" 
              :key="category.value"
              :class="['nav-item', { active: currentCategory === category.value }]"
              @click="handleCategoryChange(category.value)"
            >
              {{ category.label }}
            </span>
          </div>
          
          <!-- 难度筛选 -->
          <div class="difficulty-filter">
            <span 
              v-for="level in difficulties" 
              :key="level.value"
              :class="['level-tag', { active: currentDifficulty === level.value }]"
              @click="handleDifficultyChange(level.value)"
            >
              {{ level.label }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <div class="cyber-container">
        <!-- 推荐课程 -->
        <section class="featured-section" v-if="featuredCourses.length">
          <h2 class="section-title text-center">推荐课程</h2>
          <div class="featured-grid">
            <CourseCard
              v-for="course in featuredCourses"
              :key="course.id"
              :course="course"
              @click="viewCourseDetail"
              @start="startLearning"
              @continue="continueLearning"
            />
          </div>
        </section>

        <!-- 全部课程 -->
        <section class="all-courses-section">
          <div class="section-header">
            <h2 class="section-title text-center">全部课程</h2>
            <div class="sort-options">
              <el-radio-group v-model="sortBy" @change="handleSortChange">
                <el-radio-button label="newest">最新</el-radio-button>
                <el-radio-button label="popular">最热</el-radio-button>
                <el-radio-button label="rating">评分</el-radio-button>
              </el-radio-group>
            </div>
          </div>
          
          <CourseList
            :courses="courses"
            :loading="loading"
            :total="total"
            @view="viewCourseDetail"
            @start="startLearning"
            @continue="continueLearning"
            @page-change="handlePageChange"
            @size-change="handleSizeChange"
          />
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import CourseCard from './components/CourseCard.vue'
import CourseList from './components/CourseList.vue'

const router = useRouter()
const loading = ref(false)
const courses = ref<any[]>([])
const total = ref(0)
const sortBy = ref('newest')
const searchQuery = ref('')
const currentCategory = ref('all')
const currentDifficulty = ref('')

// 热门搜索
const hotSearches = [
  'Web安全入门',
  'XSS攻防',
  'SQL注入',
  '渗透测试',
  'CTF实战'
]

// 分类选项
const categories = [
  { label: '全部课程', value: 'all' },
  { label: 'Web安全', value: 'web' },
  { label: '系统安全', value: 'system' },
  { label: '网络安全', value: 'network' },
  { label: '密码学', value: 'crypto' },
  { label: '安全开发', value: 'secure_dev' }
]

// 难度等级
const difficulties = [
  { label: '入门', value: 'beginner' },
  { label: '初级', value: 'elementary' },
  { label: '中级', value: 'intermediate' },
  { label: '高级', value: 'advanced' }
]

// 模拟数据
const mockCourses = [
  {
    id: 1,
    title: 'Web安全基础入门',
    description: '学习Web安全的基本概念和常见漏洞原理',
    cover_url: '/images/courses/course1.jpg',
    difficulty: 'beginner',
    student_count: 1234,
    duration: 120,
    lessons: 12,
    rating: 4.5,
    featured: true,
    teacher: {
      name: '张教授',
      avatar: '/images/avatars/teacher1.jpg'
    }
  },
  {
    id: 2,
    title: 'XSS跨站脚本攻击与防御',
    description: '深入理解XSS漏洞的原理和防御方法',
    cover_url: '/images/courses/course2.jpg',
    difficulty: 'intermediate',
    student_count: 856,
    duration: 180,
    lessons: 15,
    rating: 4.8,
    progress: 45,
    teacher: {
      name: '李老师',
      avatar: '/images/avatars/teacher2.jpg'
    }
  },
  {
    id: 3,
    title: 'SQL注入高级利用技巧',
    description: '掌握SQL注入的高级利用方法和防御策略',
    cover_url: '/images/courses/course3.jpg',
    difficulty: 'advanced',
    student_count: 567,
    duration: 240,
    lessons: 20,
    rating: 4.9,
    featured: true,
    teacher: {
      name: '王教授',
      avatar: '/images/avatars/teacher3.jpg'
    }
  }
]

// 推荐课程
const featuredCourses = computed(() => {
  return mockCourses.filter(course => course.featured)
})

// 统计数据
const totalCourses = computed(() => mockCourses.length)
const totalStudents = computed(() => {
  return mockCourses.reduce((total, course) => total + (course.student_count || 0), 0)
})
const averageRating = computed(() => {
  const ratings = mockCourses.filter(course => course.rating)
  if (!ratings.length) return 0
  const sum = ratings.reduce((total, course) => total + course.rating!, 0)
  return (sum / ratings.length).toFixed(1)
})

// 获取课程列表
const fetchCourses = async () => {
  loading.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 500))
    courses.value = mockCourses
    total.value = mockCourses.length
  } catch (error) {
    ElMessage.error('获取课程列表失败')
    console.error('Failed to fetch courses:', error)
  } finally {
    loading.value = false
  }
}

// 处理搜索
const handleSearch = () => {
  fetchCourses()
}

const handleTagClick = (tag: string) => {
  searchQuery.value = tag
  handleSearch()
}

// 处理分类变化
const handleCategoryChange = (category: string) => {
  currentCategory.value = category
  fetchCourses()
}

// 处理难度变化
const handleDifficultyChange = (difficulty: string) => {
  currentDifficulty.value = currentDifficulty.value === difficulty ? '' : difficulty
  fetchCourses()
}

// 处理排序变化
const handleSortChange = () => {
  fetchCourses()
}

// 查看课程详情
const viewCourseDetail = (courseId: number) => {
  router.push(`/courses/${courseId}`)
}

// 开始学习
const startLearning = (courseId: number) => {
  router.push(`/courses/${courseId}/learn/1`)
}

// 继续学习
const continueLearning = (courseId: number) => {
  const course = courses.value.find(c => c.id === courseId)
  if (course) {
    router.push(`/courses/${courseId}/learn/1`)
  }
}

// 处理分页
const handlePageChange = (page: number) => {
  fetchCourses()
}

const handleSizeChange = (size: number) => {
  fetchCourses()
}

onMounted(() => {
  fetchCourses()
})
</script>

<style lang="scss" scoped>
.cyber-courses {
  min-height: 100vh;
  background: linear-gradient(to bottom, #1a1f3c, #0c1023);
  color: #fff;
}

.text-center {
  text-align: center;
}

.page-header {
  padding: 60px 0;
  
  .header-content {
    max-width: 800px;
    margin: 0 auto;
    
    .main-title {
      font-size: 3rem;
      font-weight: 700;
      margin: 0 0 1.5rem;
      background: linear-gradient(to right, #fff, #64ffda);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
      font-size: 1.25rem;
      color: rgba(255, 255, 255, 0.8);
      margin: 0 0 3rem;
    }
    
    .stats-bar {
      display: flex;
      justify-content: center;
      gap: 4rem;
      
      .stat-item {
        text-align: center;
        
        .stat-value {
          font-size: 2.5rem;
          font-weight: 600;
          color: #64ffda;
          line-height: 1.2;
        }
        
        .stat-label {
          font-size: 1rem;
          color: rgba(255, 255, 255, 0.6);
          margin-top: 0.5rem;
        }
      }
    }
  }
}

.nav-section {
  background: rgba(255, 255, 255, 0.02);
  border-top: 1px solid rgba(255, 255, 255, 0.05);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  padding: 2rem 0;
  
  .search-box {
    max-width: 600px;
    margin: 0 auto 2rem;
    
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
  
  .category-nav {
    .nav-list {
      display: flex;
      justify-content: center;
      gap: 3rem;
      margin-bottom: 2rem;
      
      .nav-item {
        font-size: 1.1rem;
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
    
    .difficulty-filter {
      display: flex;
      justify-content: center;
      gap: 1rem;
      
      .level-tag {
        padding: 0.5rem 1.5rem;
        border-radius: 4px;
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
        cursor: pointer;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.05);
        
        &:hover {
          background: rgba(255, 255, 255, 0.1);
          color: #fff;
        }
        
        &.active {
          background: var(--el-color-primary);
          color: #fff;
        }
      }
    }
  }
}

.main-content {
  padding: 4rem 0;
  
  .section-title {
    font-size: 2.25rem;
    font-weight: 600;
    margin: 0 0 3rem;
    background: linear-gradient(to right, #fff, #64ffda);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .featured-section {
    margin-bottom: 6rem;
    
    .featured-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 2rem;
    }
  }
  
  .all-courses-section {
    .section-header {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 3rem;
      
      .sort-options {
        margin-top: 1.5rem;
        
        :deep(.el-radio-button__inner) {
          background: transparent;
          border-color: rgba(255, 255, 255, 0.1);
          color: rgba(255, 255, 255, 0.7);
          
          &:hover {
            color: #fff;
            border-color: rgba(255, 255, 255, 0.2);
          }
        }
        
        :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
          background: var(--el-color-primary);
          border-color: var(--el-color-primary);
          color: #fff;
          box-shadow: none;
        }
      }
    }
  }
}

.cyber-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

@media (max-width: 1024px) {
  .page-header {
    padding: 40px 0;
    
    .header-content {
      .main-title {
        font-size: 2.5rem;
      }
      
      .stats-bar {
        gap: 2rem;
        
        .stat-item {
          .stat-value {
            font-size: 2rem;
          }
        }
      }
    }
  }
  
  .nav-section {
    .category-nav {
      .nav-list {
        gap: 2rem;
        overflow-x: auto;
        padding-bottom: 1rem;
        
        &::-webkit-scrollbar {
          display: none;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 30px 0;
    
    .header-content {
      .main-title {
        font-size: 2rem;
      }
      
      .subtitle {
        font-size: 1.1rem;
      }
      
      .stats-bar {
        flex-wrap: wrap;
        gap: 2rem;
        
        .stat-item {
          flex: 1;
          min-width: 120px;
        }
      }
    }
  }
  
  .nav-section {
    padding: 1.5rem 0;
    
    .search-box {
      margin-bottom: 1.5rem;
      
      .hot-searches {
        .hot-tag {
          display: inline-block;
          margin: 0.5rem;
          
          &::after {
            display: none;
          }
        }
      }
    }
    
    .category-nav {
      .difficulty-filter {
        flex-wrap: wrap;
        
        .level-tag {
          flex: 1;
          text-align: center;
        }
      }
    }
  }
  
  .main-content {
    padding: 3rem 0;
    
    .section-title {
      font-size: 1.75rem;
      margin-bottom: 2rem;
    }
    
    .featured-section {
      margin-bottom: 4rem;
    }
  }
}
</style> 