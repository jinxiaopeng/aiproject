<template>
  <div class="course-detail">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="course-info">
          <template #header>
            <div class="card-header">
              <h2>{{ course.title }}</h2>
              <el-tag :type="difficultyType">{{ difficultyText }}</el-tag>
            </div>
          </template>
          
          <div class="course-description">
            {{ course.description }}
          </div>

          <div class="course-chapters">
            <h3>课程章节</h3>
            <el-collapse v-model="activeChapters">
              <el-collapse-item 
                v-for="chapter in chapters" 
                :key="chapter.id" 
                :title="chapter.title"
                :name="chapter.id"
              >
                <div 
                  v-for="lesson in chapter.lessons" 
                  :key="lesson.id"
                  class="lesson-item"
                  :class="{ 'completed': isLessonCompleted(lesson.id) }"
                  @click="goToLesson(lesson.id)"
                >
                  <div class="lesson-info">
                    <i class="el-icon" :class="getLessonIcon(lesson.id)"></i>
                    <span class="lesson-title">{{ lesson.title }}</span>
                  </div>
                  <div class="lesson-duration">
                    {{ formatDuration(lesson.duration) }}
                  </div>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <CourseProgress 
          v-if="courseProgress"
          :progress="courseProgress"
          class="course-progress-widget"
        />

        <el-card class="course-meta">
          <template #header>
            <div class="card-header">
              <h3>课程信息</h3>
            </div>
          </template>
          
          <div class="meta-item">
            <i class="el-icon-time"></i>
            <span>总时长：{{ formatDuration(course.totalDuration) }}</span>
          </div>
          <div class="meta-item">
            <i class="el-icon-document"></i>
            <span>课时数：{{ course.totalLessons }}课时</span>
          </div>
          <div class="meta-item">
            <i class="el-icon-user"></i>
            <span>学习人数：{{ course.studentCount }}人</span>
          </div>
          <div class="meta-item">
            <i class="el-icon-date"></i>
            <span>更新时间：{{ formatDate(course.updatedAt) }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'
import CourseProgress from '@/components/course/CourseProgress.vue'
import type { CourseProgress as ICourseProgress } from '@/api/progress'
import progressApi from '@/api/progress'

export default defineComponent({
  name: 'CourseDetail',
  components: {
    CourseProgress
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const courseId = Number(route.params.id)

    const course = ref({
      id: courseId,
      title: '',
      description: '',
      difficulty: 1,
      totalDuration: 0,
      totalLessons: 0,
      studentCount: 0,
      updatedAt: '',
    })

    const chapters = ref([])
    const activeChapters = ref([])
    const courseProgress = ref<ICourseProgress | null>(null)

    const difficultyType = computed(() => {
      const types = ['success', 'warning', 'danger']
      return types[course.value.difficulty - 1] || 'info'
    })

    const difficultyText = computed(() => {
      const texts = ['初级', '中级', '高级']
      return texts[course.value.difficulty - 1] || '未知'
    })

    const loadCourseProgress = async () => {
      try {
        const response = await progressApi.getCourseProgress(courseId)
        courseProgress.value = response.data
      } catch (error) {
        console.error('加载课程进度失败:', error)
      }
    }

    const isLessonCompleted = (lessonId: number) => {
      // TODO: 根据课程进度判断课时是否完成
      return false
    }

    const getLessonIcon = (lessonId: number) => {
      if (isLessonCompleted(lessonId)) {
        return 'el-icon-check'
      }
      return 'el-icon-video-play'
    }

    const formatDuration = (minutes: number) => {
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      return hours > 0 ? `${hours}小时${mins}分钟` : `${mins}分钟`
    }

    const formatDate = (dateStr: string) => {
      return dayjs(dateStr).format('YYYY-MM-DD')
    }

    const goToLesson = (lessonId: number) => {
      router.push(`/course/${courseId}/lesson/${lessonId}`)
    }

    onMounted(async () => {
      // TODO: 加载课程详情
      // TODO: 加载课程章节
      await loadCourseProgress()
    })

    return {
      course,
      chapters,
      activeChapters,
      courseProgress,
      difficultyType,
      difficultyText,
      isLessonCompleted,
      getLessonIcon,
      formatDuration,
      formatDate,
      goToLesson
    }
  }
})
</script>

<style scoped>
.course-detail {
  padding: 20px;
}

.course-info {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 24px;
}

.course-description {
  margin: 20px 0;
  line-height: 1.6;
  color: var(--el-text-color-regular);
}

.course-chapters {
  margin-top: 20px;
}

.course-chapters h3 {
  margin-bottom: 16px;
}

.lesson-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.lesson-item:hover {
  background-color: var(--el-color-primary-light-9);
}

.lesson-item.completed {
  color: var(--el-color-success);
}

.lesson-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.lesson-title {
  font-size: 14px;
}

.lesson-duration {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.course-progress-widget {
  margin-bottom: 20px;
}

.course-meta {
  background: var(--el-bg-color);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  color: var(--el-text-color-regular);
}

.meta-item i {
  color: var(--el-text-color-secondary);
}
</style> 