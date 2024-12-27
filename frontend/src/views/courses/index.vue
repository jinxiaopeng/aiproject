<template>
  <div class="courses-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1>探索安全课程</h1>
          <p>从基础到高级，系统学习网络安全知识</p>
        </div>
        <div class="header-stats">
            <div class="stat-item">
            <div class="stat-value">{{ courseStats.totalCourses }}</div>
              <div class="stat-label">精品课程</div>
            </div>
            <div class="stat-item">
            <div class="stat-value">{{ courseStats.totalStudents }}</div>
              <div class="stat-label">学习人数</div>
            </div>
            <div class="stat-item">
            <div class="stat-value">{{ courseStats.averageRating }}</div>
              <div class="stat-label">平均评分</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
        <!-- 分类导航 -->
        <div class="category-nav">
        <div class="nav-header">
          <h2>课程分类</h2>
        </div>
        <div class="category-list">
          <div
            v-for="category in courseCategories"
            :key="category.key"
            class="category-item"
            :class="{ active: selectedCategory === category.key }"
            @click="handleCategoryChange(category.key)"
          >
            <el-icon><component :is="category.icon" /></el-icon>
            <span>{{ category.label }}</span>
            <span class="course-count">{{ getCategoryCount(category.key) }}</span>
          </div>
        </div>
          </div>
          
      <!-- 课程列表区域 -->
      <div class="course-content">
        <!-- 筛选工具栏 -->
        <div class="toolbar">
          <div class="filter-group">
            <el-select v-model="selectedDifficulty" placeholder="难度" clearable>
              <el-option
                v-for="diff in courseDifficulties"
                :key="diff.key"
                :label="diff.label"
                :value="diff.key"
              >
                <span :style="{ color: diff.color }">{{ diff.label }}</span>
              </el-option>
            </el-select>
            <el-select v-model="sortBy" placeholder="排序" clearable>
              <el-option label="最新" value="newest" />
              <el-option label="最热" value="popular" />
              <el-option label="评分" value="rating" />
            </el-select>
          </div>
          <div class="search-group">
            <el-input
              v-model="searchQuery"
              placeholder="搜索课程..."
              clearable
              prefix-icon="Search"
            />
          </div>
        </div>

        <!-- 课程列表 -->
        <div class="all-courses">
          <h2>{{ selectedCategory ? getCategoryLabel(selectedCategory) : '全部课程' }}</h2>
          <div class="course-grid">
            <CourseCard
              v-for="course in filteredCourses"
              :key="course.id"
              :course="course"
              @click="viewCourse(course)"
              @start="startCourse"
              @continue="continueCourse"
            />
      </div>
    </div>

        <!-- 推荐课程 -->
        <div v-if="!selectedCategory && !searchQuery" class="featured-courses">
          <h2>推荐课程</h2>
          <div class="course-grid">
            <CourseCard
              v-for="course in featuredCourses"
              :key="course.id"
              :course="course"
              @click="viewCourse(course)"
              @start="startCourse"
              @continue="continueCourse"
            />
            </div>
          </div>
          
        <!-- 分页 -->
        <div class="pagination">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[12, 24, 36, 48]"
            :total="totalCourses"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import CourseCard from './components/CourseCard.vue'
import { 
  courseCategories, 
  courseDifficulties, 
  featuredCourses, 
  allCourses,
  courseStats 
} from './mock/data'
import type { Course } from '@/types/course'

const router = useRouter()

// 状态管理
const selectedCategory = ref('')
const selectedDifficulty = ref('')
const sortBy = ref('newest')
const searchQuery = ref('')
const currentPage = ref(1)
const pageSize = ref(12)

// 计算属性
const filteredCourses = computed(() => {
  let courses = [...allCourses]

  // 分类筛选
  if (selectedCategory.value) {
    courses = courses.filter(course => course.category === selectedCategory.value)
  }

  // 难度筛选
  if (selectedDifficulty.value) {
    courses = courses.filter(course => course.difficulty === selectedDifficulty.value)
  }

  // 搜索筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    courses = courses.filter(course => 
      course.title.toLowerCase().includes(query) ||
      course.description.toLowerCase().includes(query)
    )
  }

  // 排序
  switch (sortBy.value) {
    case 'newest':
      courses.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      break
    case 'popular':
      courses.sort((a, b) => b.student_count - a.student_count)
      break
    case 'rating':
      courses.sort((a, b) => b.rating - a.rating)
      break
  }
  
  return courses
})

const totalCourses = computed(() => filteredCourses.value.length)

// 方法
const handleCategoryChange = (category: string) => {
  selectedCategory.value = category
  currentPage.value = 1
}

const getCategoryCount = (category: string) => {
  return allCourses.filter(course => course.category === category).length
}

const getCategoryLabel = (categoryKey: string) => {
  const category = courseCategories.find(c => c.key === categoryKey)
  return category ? category.label : ''
}

const viewCourse = (course: Course) => {
  console.log('Viewing course:', course.id)
  router.push(`/courses/${course.id}`)
}

const startCourse = (courseId: number) => {
  console.log('Starting course:', courseId)
  router.push(`/courses/${courseId}/learn`)
}

const continueCourse = (courseId: number) => {
  console.log('Continuing course:', courseId)
  router.push(`/courses/${courseId}/learn`)
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
}
</script>

<style lang="scss" scoped>
.courses-page {
  min-height: 100vh;
  background: #0a1930;
  color: #fff;
  padding: 0;
}

.page-header {
  padding: 30px 0;
  background: linear-gradient(to right, #1a365d, #2d3748);
  
  .header-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .header-text {
      h1 {
        font-size: 2rem;
        margin: 0 0 0.5rem;
        background: linear-gradient(to right, #fff, #63b3ed);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
      p {
        font-size: 1rem;
        color: #a0aec0;
        margin: 0;
      }
    }

    .header-stats {
      display: flex;
      gap: 1.5rem;
      
      .stat-item {
        text-align: center;
        
        .stat-value {
          font-size: 1.75rem;
          font-weight: 600;
          color: #63b3ed;
        }
        
        .stat-label {
          font-size: 0.85rem;
          color: #a0aec0;
          margin-top: 0.25rem;
        }
      }
    }
  }
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 15px 10px;
  display: flex;
  gap: 15px;
}

.category-nav {
  width: 180px;
  flex-shrink: 0;

  .nav-header {
    margin-bottom: 12px;

    h2 {
      font-size: 1.25rem;
      margin: 0;
          color: #fff;
    }
  }

  .category-list {
      display: flex;
    flex-direction: column;
    gap: 4px;

    .category-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 6px;
        cursor: pointer;
        transition: all 0.3s ease;
      color: #a0aec0;
        
        &:hover {
          background: rgba(255, 255, 255, 0.1);
          color: #fff;
        }
        
        &.active {
        background: #2b6cb0;
          color: #fff;
        }

      .course-count {
        margin-left: auto;
        font-size: 0.85rem;
        color: #718096;
      }
    }
  }
}

.course-content {
  flex: 1;

  .toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    .filter-group {
      display: flex;
      gap: 10px;
    }

    .search-group {
      width: 250px;
    }
  }

  h2 {
    font-size: 1.25rem;
    margin: 0 0 16px;
            color: #fff;
  }
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.featured-courses {
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

@media (max-width: 1024px) {
  .main-content {
    flex-direction: column;
  }

    .category-nav {
    width: 100%;
    margin-bottom: 20px;

    .category-list {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
      gap: 8px;
    }
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 20px 0;
    
    .header-content {
      flex-direction: column;
      text-align: center;
      gap: 20px;

      .header-text {
        h1 {
          font-size: 1.75rem;
        }
      }
    }
  }

  .toolbar {
    flex-direction: column;
    gap: 10px;

    .filter-group,
    .search-group {
      width: 100%;
    }
  }
}
</style> 