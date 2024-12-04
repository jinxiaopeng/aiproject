<template>
  <div class="lesson-detail">
    <el-row :gutter="24">
      <!-- 主要内容区 -->
      <el-col :span="18">
        <!-- 课时内容 -->
        <el-card class="content-card">
          <template #header>
            <div class="content-header">
              <h1>{{ lesson.title }}</h1>
              <div class="lesson-meta">
                <el-tag :type="getTypeTag(lesson.type)">
                  {{ getTypeLabel(lesson.type) }}
                </el-tag>
                <span class="duration">
                  <el-icon><Timer /></el-icon>
                  {{ lesson.duration }}分钟
                </span>
              </div>
            </div>
          </template>

          <!-- 视频播放器 -->
          <div v-if="lesson.type === 'video'" class="video-container">
            <video-player
              v-if="lesson.resources?.video_url"
              :src="lesson.resources.video_url"
              :current-time="lastPosition"
              @timeupdate="handleTimeUpdate"
              @ended="handleVideoEnd"
            />
          </div>

          <!-- 文本内容 -->
          <div v-else-if="lesson.type === 'text'" class="text-content">
            <div v-html="lesson.content"></div>
          </div>

          <!-- 测验内容 -->
          <div v-else-if="lesson.type === 'quiz'" class="quiz-content">
            <quiz-player
              :quiz-data="lesson.content"
              @complete="handleQuizComplete"
            />
          </div>

          <!-- 附件资源 -->
          <div v-if="lesson.resources?.attachments?.length" class="attachments">
            <h3>相关资源</h3>
            <el-divider />
            <div class="attachment-list">
              <div
                v-for="(attachment, index) in lesson.resources.attachments"
                :key="index"
                class="attachment-item"
              >
                <el-icon><Document /></el-icon>
                <a :href="attachment.url" target="_blank">
                  {{ attachment.name }}
                </a>
              </div>
            </div>
          </div>
        </el-card>

        <!-- 笔记区域 -->
        <el-card class="notes-card">
          <template #header>
            <div class="card-header">
              <span>学习笔记</span>
              <div class="actions">
                <el-button
                  v-if="isEditing"
                  type="primary"
                  size="small"
                  @click="saveNote"
                >
                  保存
                </el-button>
                <el-button
                  v-else
                  type="primary"
                  size="small"
                  @click="startEditing"
                >
                  编辑
                </el-button>
              </div>
            </div>
          </template>

          <div class="notes-content">
            <el-input
              v-if="isEditing"
              v-model="noteContent"
              type="textarea"
              :rows="6"
              placeholder="记录你的学习笔记..."
            />
            <div v-else class="note-display" v-html="noteContent"></div>
          </div>
        </el-card>
      </el-col>

      <!-- 侧边栏 -->
      <el-col :span="6">
        <!-- 课程导航 -->
        <el-card class="navigation-card">
          <template #header>
            <div class="card-header">
              <span>课程大纲</span>
              <el-progress
                :percentage="courseProgress"
                :format="progressFormat"
                type="circle"
                :width="40"
              />
            </div>
          </template>

          <el-menu
            :default-active="String(lesson.id)"
            class="lesson-menu"
          >
            <el-sub-menu
              v-for="chapter in chapters"
              :key="chapter.id"
              :index="String(chapter.id)"
            >
              <template #title>
                <span>{{ chapter.title }}</span>
              </template>

              <el-menu-item
                v-for="item in getLessonsByChapter(chapter.id)"
                :key="item.id"
                :index="String(item.id)"
                @click="navigateToLesson(item.id)"
              >
                <div class="lesson-menu-item">
                  <div class="lesson-info">
                    <el-icon>
                      <component :is="getLessonTypeIcon(item.type)" />
                    </el-icon>
                    <span>{{ item.title }}</span>
                  </div>
                  <el-icon
                    v-if="isLessonCompleted(item.id)"
                    class="completed-icon"
                  >
                    <Check />
                  </el-icon>
                </div>
              </el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-card>

        <!-- 学习进度 -->
        <el-card class="progress-card">
          <template #header>
            <div class="card-header">
              <span>学习进度</span>
            </div>
          </template>

          <div class="progress-stats">
            <div class="stat-item">
              <div class="stat-label">已学习时长</div>
              <div class="stat-value">{{ formatDuration(learningTime) }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">完成课时</div>
              <div class="stat-value">{{ completedLessons }}/{{ totalLessons }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Timer,
  Document,
  VideoCamera,
  QuestionFilled,
  Check
} from '@element-plus/icons-vue'
import courseApi from '@/api/course'
import type {
  CourseDetail,
  Chapter,
  Lesson,
  LearningProgress
} from '@/api/course'
import VideoPlayer from '@/components/lesson/VideoPlayer.vue'
import QuizPlayer from '@/components/lesson/QuizPlayer.vue'

const route = useRoute()
const router = useRouter()
const courseId = Number(route.params.courseId)
const lessonId = Number(route.params.lessonId)

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

const lesson = ref<Lesson>({
  id: lessonId,
  course_id: courseId,
  title: '',
  content: '',
  duration: 0,
  order_num: 0,
  type: 'text',
  created_at: '',
  updated_at: ''
})

const chapters = ref<Chapter[]>([])
const courseProgress = ref(0)
const lastPosition = ref(0)
const learningTime = ref(0)
const isEditing = ref(false)
const noteContent = ref('')

// 定时更新进度
let progressTimer: number | null = null

// 计算属性
const completedLessons = computed(() => {
  return course.value.lessons.filter(lesson => isLessonCompleted(lesson.id)).length
})

const totalLessons = computed(() => course.value.lessons.length)

// 方法
const getTypeTag = (type: string) => {
  const tags = {
    text: '',
    video: 'success',
    quiz: 'warning'
  }
  return tags[type as keyof typeof tags] || ''
}

const getTypeLabel = (type: string) => {
  const labels = {
    text: '文本',
    video: '视频',
    quiz: '测验'
  }
  return labels[type as keyof typeof labels] || type
}

const getLessonTypeIcon = (type: string) => {
  const icons = {
    text: Document,
    video: VideoCamera,
    quiz: QuestionFilled
  }
  return icons[type as keyof typeof icons] || Document
}

const getLessonsByChapter = (chapterId: number) => {
  return course.value.lessons.filter(lesson => lesson.chapter_id === chapterId)
}

const isLessonCompleted = (lessonId: number) => {
  // TODO: 实现课时完成状态判断
  return false
}

const formatDuration = (minutes: number) => {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return hours > 0 ? `${hours}小时${mins}分钟` : `${mins}分钟`
}

const progressFormat = (percentage: number) => {
  return `${percentage}%`
}

const navigateToLesson = (lessonId: number) => {
  router.push(`/learning/${courseId}/lessons/${lessonId}`)
}

const handleTimeUpdate = (currentTime: number) => {
  lastPosition.value = currentTime
  updateProgress()
}

const handleVideoEnd = () => {
  updateProgress(100)
}

const handleQuizComplete = (score: number) => {
  updateProgress(100)
}

const updateProgress = async (progress?: number) => {
  try {
    await courseApi.updateProgress(courseId, {
      lesson_id: lessonId,
      progress: progress || calculateProgress()
    })
  } catch (error) {
    console.error('更新进度失败:', error)
  }
}

const calculateProgress = () => {
  if (lesson.value.type === 'video' && lesson.value.duration > 0) {
    return (lastPosition.value / lesson.value.duration) * 100
  }
  return 0
}

const startProgressTracking = () => {
  progressTimer = window.setInterval(() => {
    learningTime.value += 1
    updateProgress()
  }, 60000) // 每分钟更新一次
}

const stopProgressTracking = () => {
  if (progressTimer) {
    window.clearInterval(progressTimer)
    progressTimer = null
  }
}

const startEditing = () => {
  isEditing.value = true
}

const saveNote = async () => {
  try {
    // TODO: 实现保存笔记
    isEditing.value = false
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 加载数据
const loadCourseDetail = async () => {
  try {
    const { data } = await courseApi.getCourseDetail(courseId)
    course.value = data
    chapters.value = data.chapters
  } catch (error) {
    ElMessage.error('加载课程详情失败')
  }
}

const loadLessonDetail = async () => {
  try {
    const { data } = await courseApi.getLessonDetail(courseId, lessonId)
    lesson.value = data
  } catch (error) {
    ElMessage.error('加载课时详情失败')
  }
}

// 生命周期钩子
onMounted(async () => {
  await Promise.all([
    loadCourseDetail(),
    loadLessonDetail()
  ])
  startProgressTracking()
})

onBeforeUnmount(() => {
  stopProgressTracking()
})
</script>

<style scoped>
.lesson-detail {
  padding: 24px;
}

.content-card {
  margin-bottom: 24px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.content-header h1 {
  margin: 0;
  font-size: 24px;
}

.lesson-meta {
  display: flex;
  align-items: center;
  gap: 16px;
}

.duration {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--el-text-color-secondary);
}

.video-container {
  aspect-ratio: 16/9;
  background-color: #000;
  margin-bottom: 24px;
}

.text-content {
  line-height: 1.8;
  color: var(--el-text-color-regular);
}

.attachments {
  margin-top: 24px;
}

.attachments h3 {
  margin: 0;
  font-size: 16px;
}

.attachment-list {
  margin-top: 16px;
}

.attachment-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 0;
}

.attachment-item a {
  color: var(--el-color-primary);
  text-decoration: none;
}

.attachment-item a:hover {
  text-decoration: underline;
}

.notes-card {
  margin-bottom: 24px;
}

.notes-content {
  min-height: 200px;
}

.note-display {
  line-height: 1.8;
  color: var(--el-text-color-regular);
}

.navigation-card {
  margin-bottom: 24px;
}

.lesson-menu {
  border-right: none;
}

.lesson-menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.lesson-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.completed-icon {
  color: var(--el-color-success);
}

.progress-card {
  margin-bottom: 24px;
}

.progress-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.stat-label {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-bottom: 8px;
}

.stat-value {
  font-size: 20px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 