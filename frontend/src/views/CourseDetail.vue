<template>
  <div class="course-detail">
    <el-row :gutter="24">
      <!-- 课程信息 -->
      <el-col :span="16">
        <el-card class="course-info">
          <div class="course-header">
            <div class="title-section">
              <h1>{{ course.title }}</h1>
              <el-tag :type="difficultyType" class="level-tag">
                {{ difficultyText }}
              </el-tag>
            </div>
            <div class="meta-info">
              <div class="meta-item">
                <el-icon><Clock /></el-icon>
                <span>总时长：{{ course.duration }}分钟</span>
              </div>
              <div class="meta-item">
                <el-icon><User /></el-icon>
                <span>学习人数：{{ course.student_count || 0 }}人</span>
              </div>
              <div class="meta-item">
                <el-icon><Calendar /></el-icon>
                <span>更新时间：{{ formatDate(course.updated_at) }}</span>
              </div>
            </div>
          </div>

          <el-divider />

          <div class="course-description">
            <h3>课程介绍</h3>
            <p>{{ course.description }}</p>
          </div>

          <div class="course-progress" v-if="courseProgress">
            <h3>学习进度</h3>
            <course-progress :progress="courseProgress" />
          </div>
        </el-card>

        <!-- 课程大纲 -->
        <el-card class="course-outline">
          <template #header>
            <div class="card-header">
              <span>课程大纲</span>
              <div class="progress-info">
                已完成 {{ completedLessons }}/{{ totalLessons }} 课时
              </div>
            </div>
          </template>

          <el-collapse v-model="activeChapters">
            <el-collapse-item
              v-for="chapter in chapters"
              :key="chapter.id"
              :title="chapter.title"
              :name="chapter.id"
            >
              <div class="chapter-description" v-if="chapter.description">
                {{ chapter.description }}
              </div>
              
              <div class="lesson-list">
                <div
                  v-for="lesson in getLessonsByChapter(chapter.id)"
                  :key="lesson.id"
                  class="lesson-item"
                  :class="{ completed: isLessonCompleted(lesson.id) }"
                  @click="goToLesson(lesson.id)"
                >
                  <div class="lesson-info">
                    <el-icon :class="getLessonIcon(lesson.id)">
                      <component :is="getLessonTypeIcon(lesson.type)" />
                    </el-icon>
                    <span class="lesson-title">{{ lesson.title }}</span>
                  </div>
                  <div class="lesson-meta">
                    <span class="duration">{{ lesson.duration }}分钟</span>
                    <el-icon v-if="isLessonCompleted(lesson.id)" class="completed-icon">
                      <Check />
                    </el-icon>
                  </div>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </el-col>

      <!-- 侧边栏 -->
      <el-col :span="8">
        <!-- 学习按钮 -->
        <el-card class="action-card">
          <el-button
            type="primary"
            size="large"
            class="start-learning-btn"
            @click="startLearning"
          >
            {{ hasStarted ? '继续学习' : '开始学习' }}
          </el-button>
          
          <div class="course-stats">
            <div class="stat-item">
              <div class="stat-label">总课时</div>
              <div class="stat-value">{{ totalLessons }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">已学习</div>
              <div class="stat-value">{{ completedLessons }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">完成率</div>
              <div class="stat-value">{{ completionRate }}%</div>
            </div>
          </div>
        </el-card>

        <!-- 讲师信息 -->
        <el-card class="teacher-card" v-if="teacher">
          <template #header>
            <div class="card-header">
              <span>讲师信息</span>
            </div>
          </template>
          <div class="teacher-info">
            <el-avatar :size="64" :src="teacher.avatar" />
            <div class="teacher-detail">
              <h4>{{ teacher.name }}</h4>
              <p>{{ teacher.title }}</p>
            </div>
          </div>
          <p class="teacher-bio">{{ teacher.bio }}</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Clock,
  User,
  Calendar,
  Document,
  VideoCamera,
  QuestionFilled,
  Check
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import courseApi from '@/api/course'
import type { CourseDetail, Chapter, Lesson, LearningProgress } from '@/api/course'
import CourseProgress from '@/components/course/CourseProgress.vue'

const route = useRoute()
const router = useRouter()
const courseId = Number(route.params.id)

// 状态
const course = ref<CourseDetail>({
  id: courseId,
  title: '',
  description: '',
  cover_image: '',
  level: 'beginner',
  category: '',
  duration: 0,
  status: 'published',
  created_by: 0,
  created_at: '',
  updated_at: '',
  chapters: [],
  lessons: []
})

const chapters = ref<Chapter[]>([])
const activeChapters = ref<number[]>([])
const courseProgress = ref<LearningProgress | null>(null)

// 教师信息
const teacher = ref({
  name: '张教授',
  title: '网络安全专家',
  avatar: '/avatar.png',
  bio: '从事网络安全教育15年，具有丰富的实战经验。'
})

// 计算属性
const difficultyType = computed(() => {
  const types = {
    beginner: 'success',
    intermediate: 'warning',
    advanced: 'danger'
  }
  return types[course.value.level] || 'info'
})

const difficultyText = computed(() => {
  const texts = {
    beginner: '初级',
    intermediate: '中级',
    advanced: '高级'
  }
  return texts[course.value.level] || '未知'
})

const totalLessons = computed(() => course.value.lessons.length)

const completedLessons = computed(() => {
  if (!courseProgress.value) return 0
  return Math.floor(courseProgress.value.progress * totalLessons.value / 100)
})

const completionRate = computed(() => {
  if (!courseProgress.value) return 0
  return Math.floor(courseProgress.value.progress)
})

const hasStarted = computed(() => {
  return courseProgress.value && courseProgress.value.progress > 0
})

// 方法
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

const getLessonsByChapter = (chapterId: number) => {
  return course.value.lessons.filter(lesson => lesson.chapter_id === chapterId)
}

const isLessonCompleted = (lessonId: number) => {
  if (!courseProgress.value) return false
  // TODO: 实现课时完成状态判断
  return false
}

const getLessonTypeIcon = (type: string) => {
  const icons = {
    text: Document,
    video: VideoCamera,
    quiz: QuestionFilled
  }
  return icons[type as keyof typeof icons] || Document
}

const startLearning = () => {
  const firstLesson = course.value.lessons[0]
  if (firstLesson) {
    router.push(`/learning/${courseId}/lessons/${firstLesson.id}`)
  }
}

const goToLesson = (lessonId: number) => {
  router.push(`/learning/${courseId}/lessons/${lessonId}`)
}

// 加载数据
const loadCourseDetail = async () => {
  try {
    const { data } = await courseApi.getCourseDetail(courseId)
    course.value = data
    chapters.value = data.chapters
    // 默认展开第一个章节
    if (chapters.value.length > 0) {
      activeChapters.value = [chapters.value[0].id]
    }
  } catch (error) {
    ElMessage.error('加载课程详情失败')
  }
}

const loadCourseProgress = async () => {
  try {
    const { data } = await courseApi.updateProgress(courseId, {
      lesson_id: 0,
      progress: 0
    })
    courseProgress.value = data
  } catch (error) {
    console.error('加载课程进度失败:', error)
  }
}

onMounted(() => {
  loadCourseDetail()
  loadCourseProgress()
})
</script>

<style scoped>
.course-detail {
  padding: 24px;
}

.course-info {
  margin-bottom: 24px;
}

.course-header {
  margin-bottom: 24px;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.title-section h1 {
  margin: 0;
  font-size: 24px;
}

.level-tag {
  font-size: 14px;
}

.meta-info {
  display: flex;
  gap: 24px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--el-text-color-secondary);
}

.course-description {
  margin-bottom: 24px;
}

.course-description h3 {
  margin-top: 0;
  margin-bottom: 16px;
}

.course-progress {
  margin-top: 24px;
}

.course-outline {
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.progress-info {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.chapter-description {
  margin-bottom: 16px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.lesson-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.lesson-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.lesson-item:hover {
  background-color: var(--el-fill-color-light);
}

.lesson-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.lesson-title {
  font-size: 14px;
}

.lesson-meta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.duration {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.completed-icon {
  color: var(--el-color-success);
}

.action-card {
  margin-bottom: 24px;
}

.start-learning-btn {
  width: 100%;
  margin-bottom: 24px;
}

.course-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  text-align: center;
}

.stat-item {
  padding: 12px;
  border-radius: 4px;
  background-color: var(--el-fill-color-light);
}

.stat-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-bottom: 4px;
}

.stat-value {
  font-size: 20px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.teacher-card {
  margin-bottom: 24px;
}

.teacher-info {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.teacher-detail h4 {
  margin: 0 0 4px 0;
}

.teacher-detail p {
  margin: 0;
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.teacher-bio {
  margin: 0;
  font-size: 14px;
  color: var(--el-text-color-regular);
  line-height: 1.6;
}
</style> 