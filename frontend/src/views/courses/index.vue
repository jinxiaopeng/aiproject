<template>
  <div class="cyber-courses">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="cyber-container">
        <h1>网络安全课程</h1>
        <p class="subtitle">探索前沿的网络安全知识，提升你的安全技能</p>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="cyber-container">
      <!-- 工具栏 -->
      <div class="toolbar">
        <!-- 筛选器 -->
        <div class="filters">
          <el-select
            v-model="filterForm.category"
            placeholder="课程分类"
            clearable
            class="cyber-select"
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
            class="cyber-select"
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
            class="cyber-select"
          >
            <el-option label="最新" value="newest" />
            <el-option label="最热" value="popular" />
            <el-option label="评分" value="rating" />
          </el-select>
        </div>

        <!-- 搜索框 -->
        <div class="search">
          <el-input
            v-model="searchQuery"
            placeholder="搜索课程..."
            class="cyber-input"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
      </div>

      <!-- 课程列表 -->
      <div class="courses-grid" v-loading="loading">
        <el-empty
          v-if="!loading && !courses.length"
          description="暂无课程"
          class="cyber-empty"
        />
        
        <div
          v-for="course in courses"
          :key="course.id"
          class="cyber-card course-card"
        >
          <div class="card-cover">
            <img :src="course.cover_url || '/default-course.jpg'" :alt="course.title">
            <div class="card-overlay">
              <el-tag :type="getDifficultyType(course.difficulty)" class="cyber-tag">
                {{ getDifficultyLabel(course.difficulty) }}
              </el-tag>
              <div class="meta-items">
                <span class="meta-item">
                  <el-icon><User /></el-icon>
                  {{ course.student_count || 0 }}人学习
                </span>
                <span class="meta-item">
                  <el-icon><Timer /></el-icon>
                  {{ formatDuration(getTotalDuration(course)) }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="card-content">
            <h3 class="course-title" :title="course.title">{{ course.title }}</h3>
            <p class="course-description">{{ course.description }}</p>
            
            <div class="course-footer">
              <template v-if="course.progress !== undefined">
                <el-progress
                  :percentage="course.progress"
                  :format="(format) => `学习进度: ${format}%`"
                  :status="course.progress === 100 ? 'success' : ''"
                  class="cyber-progress"
                />
                <el-button
                  class="cyber-btn"
                  @click="continueLearning(course.id)"
                >
                  <el-icon><VideoPlay /></el-icon>
                  继续学习
                </el-button>
              </template>
              <template v-else>
                <div class="course-rating" v-if="course.rating">
                  <el-rate
                    v-model="course.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}"
                  />
                </div>
                <el-button
                  class="cyber-btn"
                  @click="startLearning(course.id)"
                >
                  <el-icon><VideoPlay /></el-icon>
                  开始学习
                </el-button>
              </template>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[12, 24, 36, 48]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          class="cyber-pagination"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, User, Timer, VideoPlay } from '@element-plus/icons-vue'
import * as courseApi from '@/api/course'
import type { Course } from '@/types/course'
import { formatDuration } from '@/utils/date'

const router = useRouter()
const loading = ref(false)
const courses = ref<Course[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const searchQuery = ref('')

// 筛选表单
const filterForm = reactive({
  category: '',
  difficulty: '',
  sort_by: 'newest' as const,
  page: 1,
  limit: 12
})

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

// 获取课程列表
const fetchCourses = async () => {
  loading.value = true
  try {
    const data = await courseApi.getCourses({
      ...filterForm,
      search: searchQuery.value
    })
    courses.value = data
  } catch (error) {
    ElMessage.error('获取课程列表失败，请稍后重试')
    console.error('Failed to fetch courses:', error)
  } finally {
    loading.value = false
  }
}

// 获取难度标签
const getDifficultyLabel = (difficulty?: string) => {
  const found = difficulties.find(d => d.value === difficulty)
  return found ? found.label : difficulty
}

// 获取难度类型
const getDifficultyType = (difficulty?: string) => {
  const types: Record<string, string> = {
    beginner: 'success',
    elementary: 'info',
    intermediate: 'warning',
    advanced: 'danger',
    expert: ''
  }
  return difficulty ? types[difficulty] || '' : ''
}

// 计算总时长
const getTotalDuration = (course: Course) => {
  return course.chapters.reduce((total, chapter) => total + (chapter.duration || 0), 0)
}

// 开始学习
const startLearning = (courseId: number) => {
  router.push(`/courses/${courseId}`)
}

// 继续学习
const continueLearning = (courseId: number) => {
  const course = courses.value.find(c => c.id === courseId)
  if (course && course.chapters.length > 0) {
    // 找到最后学习的章节或第一章
    const lastChapter = course.chapters.find(c => c.progress && c.progress < 100) || course.chapters[0]
    router.push(`/courses/${courseId}/learn/${lastChapter.id}`)
  }
}

// 分页处理
const handleSizeChange = (size: number) => {
  pageSize.value = size
  filterForm.limit = size
  fetchCourses()
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
  filterForm.page = page
  fetchCourses()
}

// 监听筛选条件变化
watch(
  [() => filterForm.category, () => filterForm.difficulty, () => filterForm.sort_by, searchQuery],
  () => {
    currentPage.value = 1
    fetchCourses()
  }
)

onMounted(() => {
  fetchCourses()
})
</script>

<style lang="scss" scoped>
@import '@/styles/cyber-theme.scss';

.cyber-courses {
  min-height: calc(100vh - 64px);
  background-color: var(--cyber-bg);
  color: var(--cyber-text);
}

.page-header {
  background: var(--cyber-bg-light);
  padding: 48px 0;
  margin-bottom: 32px;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, var(--cyber-primary) 0%, transparent 100%);
    opacity: 0.1;
  }
  
  h1 {
    font-size: 36px;
    font-weight: 600;
    margin: 0 0 16px;
    position: relative;
  }
  
  .subtitle {
    font-size: 18px;
    color: var(--cyber-text-secondary);
    margin: 0;
    position: relative;
  }
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  gap: 24px;
  
  .filters {
    display: flex;
    gap: 16px;
    flex: 1;
  }
  
  .search {
    width: 300px;
  }
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.course-card {
  .course-title {
    font-size: 18px;
    font-weight: 500;
    margin: 0 0 12px;
    color: var(--cyber-text);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .course-description {
    font-size: 14px;
    color: var(--cyber-text-secondary);
    margin: 0 0 16px;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
  
  .meta-items {
    display: flex;
    gap: 16px;
    margin-top: 8px;
    
    .meta-item {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 14px;
    }
  }
  
  .course-footer {
    display: flex;
    flex-direction: column;
    gap: 12px;
    
    .course-rating {
      display: flex;
      align-items: center;
      gap: 8px;
    }
  }
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 32px;
  padding-bottom: 32px;
}

@media (max-width: 768px) {
  .page-header {
    padding: 32px 0;
    
    h1 {
      font-size: 28px;
    }
    
    .subtitle {
      font-size: 16px;
    }
  }
  
  .toolbar {
    flex-direction: column;
    
    .filters {
      flex-direction: column;
    }
    
    .search {
      width: 100%;
    }
  }
  
  .courses-grid {
    grid-template-columns: 1fr;
  }
}
</style> 