<template>
  <div class="course-detail">
    <!-- 课程基本信息 -->
    <div class="course-header">
      <div class="course-info">
        <div class="course-cover">
          <img :src="course?.cover_url || '/default-course.jpg'" :alt="course?.title">
        </div>
        <div class="course-meta">
          <h1>{{ course?.title }}</h1>
          <p class="description">{{ course?.description }}</p>
          
          <div class="meta-items">
            <div class="meta-item">
              <el-icon><User /></el-icon>
              <span>{{ course?.student_count || 0 }}人学习</span>
            </div>
            <div class="meta-item">
              <el-icon><Timer /></el-icon>
              <span>{{ getTotalDuration() }}分钟</span>
            </div>
            <div class="meta-item">
              <el-tag :type="getDifficultyType(course?.difficulty)">
                {{ getDifficultyLabel(course?.difficulty) }}
              </el-tag>
            </div>
          </div>
          
          <div class="course-actions">
            <template v-if="course?.progress !== undefined">
              <el-progress
                :percentage="course.progress"
                :format="format => \`学习进度: \${format}%\`"
                :status="course.progress === 100 ? 'success' : ''"
              />
              <el-button type="primary" @click="continueLearning">继续学习</el-button>
            </template>
            <template v-else>
              <el-button type="primary" @click="startLearning">开始学习</el-button>
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- 课程内容 -->
    <div class="course-content">
      <el-tabs v-model="activeTab" class="course-tabs">
        <el-tab-pane label="课程大纲" name="outline">
          <div class="course-outline">
            <div v-for="chapter in course?.chapters" :key="chapter.id" class="chapter">
              <div class="chapter-header" @click="toggleChapter(chapter.id)">
                <div class="chapter-title">
                  <span>{{ chapter.title }}</span>
                  <div class="chapter-meta">
                    <span>
                      <el-icon><VideoPlay /></el-icon>
                      {{ chapter.duration }}分钟
                    </span>
                    <template v-if="chapter.progress !== undefined">
                      <el-tag :type="chapter.progress === 100 ? 'success' : 'warning'" size="small">
                        {{ chapter.progress === 100 ? '已完成' : '进行中' }}
                      </el-tag>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="课程介绍" name="intro">
          <div class="course-intro">
            <h2>课程目标</h2>
            <ul class="course-objectives">
              <li v-for="(objective, index) in courseObjectives" :key="index">
                {{ objective }}
              </li>
            </ul>
            
            <h2>适合人群</h2>
            <ul class="target-audience">
              <li v-for="(audience, index) in targetAudience" :key="index">
                {{ audience }}
              </li>
            </ul>
            
            <h2>课程特色</h2>
            <div class="course-features">
              <el-card v-for="(feature, index) in courseFeatures" :key="index">
                <template #header>
                  <div class="feature-header">
                    <el-icon>
                      <component :is="feature.icon" />
                    </el-icon>
                    <span>{{ feature.title }}</span>
                  </div>
                </template>
                <div class="feature-content">
                  {{ feature.description }}
                </div>
              </el-card>
            </div>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="讲师介绍" name="instructor">
          <div class="instructor-info" v-if="course?.instructor">
            <el-card>
              <div class="instructor-header">
                <el-avatar
                  :size="64"
                  :src="course.instructor.avatar"
                  :alt="course.instructor.username"
                />
                <div class="instructor-meta">
                  <h3>{{ course.instructor.username }}</h3>
                  <p>{{ course.instructor.bio || '暂无介绍' }}</p>
                </div>
              </div>
            </el-card>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="学习评价" name="comments">
          <div class="course-comments">
            <!-- 评分统计 -->
            <div class="rating-stats" v-if="course?.rating">
              <div class="rating-overview">
                <div class="rating-score">
                  <span class="score">{{ course.rating.toFixed(1) }}</span>
                  <el-rate v-model="course.rating" disabled />
                </div>
                <div class="rating-count">
                  共 {{ course.student_count || 0 }} 人评价
                </div>
              </div>
            </div>
            
            <!-- 评论列表 -->
            <div class="comments-list">
              <el-empty v-if="!comments.length" description="暂无评价" />
              <div v-else class="comment-item" v-for="comment in comments" :key="comment.id">
                <div class="comment-header">
                  <el-avatar :size="32" :src="comment.user.avatar">
                    {{ comment.user.username.charAt(0) }}
                  </el-avatar>
                  <div class="comment-meta">
                    <span class="username">{{ comment.user.username }}</span>
                    <el-rate v-if="comment.rating" v-model="comment.rating" disabled />
                  </div>
                  <span class="comment-time">{{ formatDate(comment.created_at) }}</span>
                </div>
                <div class="comment-content">
                  {{ comment.content }}
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  User,
  Timer,
  VideoPlay,
  Aim,
  Monitor,
  Reading
} from '@element-plus/icons-vue'
import * as courseApi from '@/api/course'
import type { Course, CourseComment } from '@/types/course'
import { formatDate } from '@/utils/date'

const route = useRoute()
const router = useRouter()
const courseId = Number(route.params.id)

const course = ref<Course | null>(null)
const comments = ref<CourseComment[]>([])
const activeTab = ref('outline')
const activeChapters = ref<number[]>([])

// 课程目标
const courseObjectives = [
  '掌握Web安全基础知识和核心概念',
  '学习常见Web漏洞的原理和防护方法',
  '实践渗透测试和安全评估技能',
  '了解最新的Web安全威胁和防御技术'
]

// 适合人群
const targetAudience = [
  '对Web安全感兴趣的初学者',
  '想要提升安全技能的开发人员',
  '从事安全工作的专业人士',
  '准备安全认证考试的考生'
]

// 课程特色
const courseFeatures = [
  {
    icon: 'Aim',
    title: '体系化学习',
    description: '系统性的课程设计，从基础到进阶的完整知识体系'
  },
  {
    icon: 'Monitor',
    title: '实战演练',
    description: '大量实际案例和动手练习，帮助巩固所学知识'
  },
  {
    icon: 'Reading',
    title: '资源丰富',
    description: '提供丰富的学习资料和参考文档，助力深入学习'
  }
]

// 获取课程信息
const fetchCourseDetail = async () => {
  try {
    course.value = await courseApi.getCourse(courseId)
  } catch (error) {
    ElMessage.error('获取课程详情失败')
    console.error('Failed to fetch course detail:', error)
  }
}

// 获取课程评论
const fetchComments = async () => {
  try {
    comments.value = await courseApi.getCourseComments(courseId)
  } catch (error) {
    ElMessage.error('获取评论失败')
    console.error('Failed to fetch comments:', error)
  }
}

// 获取难度标签
const getDifficultyLabel = (difficulty?: string) => {
  const labels: Record<string, string> = {
    beginner: '入门',
    elementary: '初级',
    intermediate: '中级',
    advanced: '高级',
    expert: '专家'
  }
  return difficulty ? labels[difficulty] || difficulty : ''
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
const getTotalDuration = () => {
  if (!course.value?.chapters) return 0
  return course.value.chapters.reduce((total, chapter) => total + (chapter.duration || 0), 0)
}

// 开始学习
const startLearning = () => {
  if (!course.value?.chapters.length) {
    ElMessage.warning('暂无可学习的章节')
    return
  }
  router.push(\`/courses/\${courseId}/learn/\${course.value.chapters[0].id}\`)
}

// 继续学习
const continueLearning = () => {
  if (!course.value?.chapters.length) {
    ElMessage.warning('暂无可学习的章节')
    return
  }
  // TODO: 获取上次学习的章节
  router.push(\`/courses/\${courseId}/learn/\${course.value.chapters[0].id}\`)
}

onMounted(() => {
  fetchCourseDetail()
  fetchComments()
})
</script>

<style lang="scss" scoped>
.course-detail {
  min-height: calc(100vh - 64px);
}

.course-header {
  background: linear-gradient(to bottom, var(--el-color-primary-light-9), #fff);
  padding: 40px 24px;
  
  .course-info {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    gap: 32px;
  }
}

.course-cover {
  width: 320px;
  height: 180px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.course-meta {
  flex: 1;
  
  h1 {
    margin: 0 0 16px;
    font-size: 28px;
    color: var(--el-text-color-primary);
  }
  
  .description {
    margin: 0 0 24px;
    font-size: 16px;
    color: var(--el-text-color-regular);
    line-height: 1.6;
  }
}

.meta-items {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
  
  .meta-item {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--el-text-color-secondary);
  }
}

.course-actions {
  .el-progress {
    margin-bottom: 16px;
  }
}

.course-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.course-outline {
  .chapter-info {
    padding: 8px 0;
  }
  
  .chapter-description {
    margin: 0 0 12px;
    color: var(--el-text-color-regular);
  }
  
  .chapter-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--el-text-color-secondary);
    
    .el-progress {
      width: 120px;
    }
  }
}

.course-intro {
  h2 {
    margin: 32px 0 16px;
    font-size: 20px;
    color: var(--el-text-color-primary);
    
    &:first-child {
      margin-top: 0;
    }
  }
  
  ul {
    margin: 0;
    padding-left: 20px;
    
    li {
      margin-bottom: 8px;
      color: var(--el-text-color-regular);
      
      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}

.course-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  
  .feature-header {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 16px;
    font-weight: 500;
  }
  
  .feature-content {
    color: var(--el-text-color-regular);
  }
}

.instructor-info {
  .instructor-header {
    display: flex;
    gap: 16px;
  }
  
  .instructor-meta {
    h3 {
      margin: 0 0 8px;
      font-size: 18px;
    }
    
    p {
      margin: 0;
      color: var(--el-text-color-regular);
    }
  }
}

.course-comments {
  .rating-stats {
    margin-bottom: 24px;
  }
  
  .rating-overview {
    display: flex;
    align-items: center;
    gap: 24px;
  }
  
  .rating-score {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .score {
      font-size: 32px;
      font-weight: 500;
      color: #ff9900;
    }
  }
  
  .rating-count {
    color: var(--el-text-color-secondary);
  }
  
  .comments-list {
    .comment-item {
      padding: 16px 0;
      border-bottom: 1px solid var(--el-border-color-lighter);
      
      &:last-child {
        border-bottom: none;
      }
    }
    
    .comment-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 8px;
    }
    
    .comment-meta {
      flex: 1;
      
      .username {
        display: block;
        margin-bottom: 4px;
        font-weight: 500;
      }
    }
    
    .comment-time {
      color: var(--el-text-color-secondary);
      font-size: 14px;
    }
    
    .comment-content {
      color: var(--el-text-color-regular);
      line-height: 1.6;
    }
  }
}

@media (max-width: 768px) {
  .course-header {
    padding: 24px 16px;
    
    .course-info {
      flex-direction: column;
    }
    
    .course-cover {
      width: 100%;
      height: 200px;
    }
  }
  
  .course-features {
    grid-template-columns: 1fr;
  }
}
</style> 