<template>
  <div class="course-list">
    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索课程..."
        class="search-input"
        :prefix-icon="Search"
        clearable
        @input="handleSearch"
      />
      <el-select
        v-model="filterLevel"
        placeholder="难度等级"
        class="filter-select"
        clearable
      >
        <el-option label="入门" value="beginner" />
        <el-option label="中级" value="intermediate" />
        <el-option label="高级" value="advanced" />
      </el-select>
      <el-select
        v-model="filterCategory"
        placeholder="课程分类"
        class="filter-select"
        clearable
      >
        <el-option label="Web安全" value="web" />
        <el-option label="系统安全" value="system" />
        <el-option label="网络安全" value="network" />
        <el-option label="密码学" value="crypto" />
      </el-select>
    </div>

    <!-- 课程列表 -->
    <div class="course-grid">
      <el-row :gutter="20">
        <el-col 
          v-for="course in filteredCourses" 
          :key="course.id" 
          :xs="24" 
          :sm="12" 
          :md="8" 
          :lg="6"
        >
          <el-card class="course-card" :body-style="{ padding: '0px' }">
            <div class="course-image">
              <img :src="course.cover" :alt="course.title">
              <div class="course-level" :class="course.level">
                {{ getLevelText(course.level) }}
              </div>
            </div>
            <div class="course-info">
              <h3 class="course-title">{{ course.title }}</h3>
              <p class="course-description">{{ course.description }}</p>
              <div class="course-meta">
                <div class="meta-item">
                  <el-icon><User /></el-icon>
                  <span>{{ course.students }}人学习</span>
                </div>
                <div class="meta-item">
                  <el-icon><Timer /></el-icon>
                  <span>{{ course.duration }}</span>
                </div>
              </div>
              <div class="course-footer">
                <div class="rating">
                  <el-rate
                    v-model="course.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                  />
                </div>
                <el-button 
                  type="primary" 
                  @click="handleEnrollCourse(course)"
                >
                  立即学习
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 加载更多 -->
    <div v-if="hasMore" class="load-more">
      <el-button 
        :loading="loading" 
        @click="loadMore"
      >
        加载更多
      </el-button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Search, User, Timer } from '@element-plus/icons-vue'

interface Course {
  id: number
  title: string
  description: string
  cover: string
  level: 'beginner' | 'intermediate' | 'advanced'
  category: string
  students: number
  duration: string
  rating: number
}

export default defineComponent({
  name: 'CourseList',
  components: {
    Search,
    User,
    Timer
  },
  setup() {
    const router = useRouter()
    const searchQuery = ref('')
    const filterLevel = ref('')
    const filterCategory = ref('')
    const loading = ref(false)
    const hasMore = ref(true)
    
    // 模拟课程数据
    const courses = ref<Course[]>([
      {
        id: 1,
        title: 'Web安全基础入门',
        description: '从零开始学习Web安全，掌握基本概念和常见漏洞',
        cover: '/images/courses/web-basic.jpg',
        level: 'beginner',
        category: 'web',
        students: 1234,
        duration: '12小时',
        rating: 4.5
      },
      {
        id: 2,
        title: '渗透测试实战',
        description: '系统学习渗透测试方法论和实战技巧',
        cover: '/images/courses/pentest.jpg',
        level: 'intermediate',
        category: 'system',
        students: 890,
        duration: '16小时',
        rating: 4.8
      },
      {
        id: 3,
        title: '网络攻防进阶',
        description: '深入学习网络安全攻防技术',
        cover: '/images/courses/network.jpg',
        level: 'advanced',
        category: 'network',
        students: 567,
        duration: '20小时',
        rating: 4.7
      },
      {
        id: 4,
        title: '密码学原理与应用',
        description: '探索现代密码学原理及其在安全领域的应用',
        cover: '/images/courses/crypto.jpg',
        level: 'intermediate',
        category: 'crypto',
        students: 432,
        duration: '14小时',
        rating: 4.6
      }
    ])
    
    // 过滤课程
    const filteredCourses = computed(() => {
      return courses.value.filter(course => {
        const matchQuery = course.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          course.description.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchLevel = !filterLevel.value || course.level === filterLevel.value
        const matchCategory = !filterCategory.value || course.category === filterCategory.value
        
        return matchQuery && matchLevel && matchCategory
      })
    })
    
    // 获取难度等级文本
    const getLevelText = (level: string) => {
      const levelMap = {
        beginner: '入门',
        intermediate: '中级',
        advanced: '高级'
      }
      return levelMap[level as keyof typeof levelMap]
    }
    
    // 搜索处理
    const handleSearch = () => {
      // TODO: 实现搜索逻辑
    }
    
    // 加载更多
    const loadMore = async () => {
      try {
        loading.value = true
        // TODO: 实现加载更多逻辑
        await new Promise(resolve => setTimeout(resolve, 1000))
        hasMore.value = false
      } finally {
        loading.value = false
      }
    }
    
    // 报名课程
    const handleEnrollCourse = (course: Course) => {
      router.push(`/course/${course.id}`)
    }
    
    return {
      searchQuery,
      filterLevel,
      filterCategory,
      loading,
      hasMore,
      filteredCourses,
      Search,
      getLevelText,
      handleSearch,
      loadMore,
      handleEnrollCourse
    }
  }
})
</script>

<style scoped>
.course-list {
  padding: 20px;
}

.filter-section {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.search-input {
  width: 300px;
}

.filter-select {
  width: 160px;
}

.course-grid {
  margin-bottom: 24px;
}

.course-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.course-card:hover {
  transform: translateY(-5px);
}

.course-image {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.course-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.course-level {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 4px 8px;
  border-radius: 4px;
  color: #fff;
  font-size: 12px;
}

.course-level.beginner {
  background-color: var(--success-color);
}

.course-level.intermediate {
  background-color: var(--warning-color);
}

.course-level.advanced {
  background-color: var(--error-color);
}

.course-info {
  padding: 16px;
}

.course-title {
  margin: 0 0 8px;
  font-size: 16px;
  font-weight: 500;
  color: var(--text-color);
}

.course-description {
  margin: 0 0 16px;
  font-size: 14px;
  color: var(--text-color-secondary);
  height: 40px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.course-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  font-size: 13px;
  color: var(--text-color-secondary);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.course-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.rating {
  font-size: 12px;
}

.load-more {
  text-align: center;
  margin-top: 24px;
}

@media (max-width: 768px) {
  .filter-section {
    flex-direction: column;
  }
  
  .search-input,
  .filter-select {
    width: 100%;
  }
}
</style> 