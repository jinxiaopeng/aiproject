<template>
  <div class="course-list">
    <div class="page-header">
      <h2>课程中心</h2>
      <div class="search-box">
        <el-input
          v-model="searchQuery"
          placeholder="搜索课程..."
          prefix-icon="Search"
          clearable
          @input="handleSearch"
        />
      </div>
    </div>

    <div class="filter-section">
      <el-radio-group v-model="currentCategory" @change="handleCategoryChange">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button label="web">Web安全</el-radio-button>
        <el-radio-button label="system">系统安全</el-radio-button>
        <el-radio-button label="crypto">密码学</el-radio-button>
      </el-radio-group>
    </div>

    <div class="course-grid" v-loading="loading">
      <el-empty v-if="!loading && courses.length === 0" description="暂无课程" />
      
      <el-row :gutter="20">
        <el-col 
          v-for="course in courses" 
          :key="course.id" 
          :xs="24" 
          :sm="12" 
          :md="8" 
          :lg="6"
        >
          <el-card class="course-card" shadow="hover">
            <img :src="course.cover" class="course-cover" />
            <div class="course-info">
              <h3 class="course-title">{{ course.title }}</h3>
              <p class="course-desc">{{ course.description }}</p>
              <div class="course-meta">
                <span>
                  <el-icon><User /></el-icon>
                  {{ course.studentCount }}人学习
                </span>
                <span>
                  <el-icon><Clock /></el-icon>
                  {{ course.duration }}
                </span>
              </div>
              <div class="course-footer">
                <el-button 
                  type="primary" 
                  @click="handleEnrollCourse(course.id)"
                >开始学习</el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <div class="pagination" v-if="total > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[12, 24, 36, 48]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, Clock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

interface Course {
  id: number
  title: string
  description: string
  cover: string
  studentCount: number
  duration: string
}

export default defineComponent({
  name: 'CourseList',
  components: {
    User,
    Clock
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const courses = ref<Course[]>([])
    const total = ref(0)
    const currentPage = ref(1)
    const pageSize = ref(12)
    const searchQuery = ref('')
    const currentCategory = ref('')

    // 模拟数据
    const mockCourses: Course[] = [
      {
        id: 1,
        title: 'Web安全基础入门',
        description: '从零开始学习Web安全，掌握基本漏洞原理与防护方法',
        cover: 'https://via.placeholder.com/300x200',
        studentCount: 1234,
        duration: '24课时'
      },
      {
        id: 2,
        title: '系统安全实战',
        description: '深入学习系统安全，实践渗透测试技术',
        cover: 'https://via.placeholder.com/300x200',
        studentCount: 890,
        duration: '36课时'
      }
    ]

    const loadCourses = () => {
      loading.value = true
      // 模拟API请求
      setTimeout(() => {
        courses.value = mockCourses
        total.value = mockCourses.length
        loading.value = false
      }, 1000)
    }

    const handleSearch = () => {
      currentPage.value = 1
      loadCourses()
    }

    const handleCategoryChange = () => {
      currentPage.value = 1
      loadCourses()
    }

    const handleSizeChange = (val: number) => {
      pageSize.value = val
      loadCourses()
    }

    const handleCurrentChange = (val: number) => {
      currentPage.value = val
      loadCourses()
    }

    const handleEnrollCourse = (courseId: number) => {
      router.push(`/courses/${courseId}`)
    }

    onMounted(() => {
      loadCourses()
    })

    return {
      loading,
      courses,
      total,
      currentPage,
      pageSize,
      searchQuery,
      currentCategory,
      handleSearch,
      handleCategoryChange,
      handleSizeChange,
      handleCurrentChange,
      handleEnrollCourse
    }
  }
})
</script>

<style scoped>
.course-list {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.search-box {
  width: 300px;
}

.filter-section {
  margin-bottom: 24px;
}

.course-grid {
  min-height: 400px;
}

.course-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.course-card:hover {
  transform: translateY(-5px);
}

.course-cover {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
}

.course-info {
  padding: 12px 0;
}

.course-title {
  margin: 0 0 8px;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.course-desc {
  margin: 0 0 12px;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  height: 42px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  color: #999;
  font-size: 13px;
  margin-bottom: 12px;
}

.course-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.course-footer {
  text-align: center;
}

.pagination {
  margin-top: 24px;
  text-align: center;
}
</style> 