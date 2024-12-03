<template>
  <div class="lesson-detail">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="lesson-content">
          <template #header>
            <div class="card-header">
              <h2>{{ lesson.title }}</h2>
              <div class="lesson-meta">
                <el-tag>{{ lesson.type }}</el-tag>
                <span class="duration">
                  <i class="el-icon-time"></i>
                  {{ formatDuration(lesson.duration) }}
                </span>
              </div>
            </div>
          </template>

          <div class="content-wrapper">
            <!-- 根据课时类型显示不同的内容 -->
            <div v-if="lesson.type === 'video'" class="video-player">
              <!-- TODO: 集成视频播放器 -->
              <el-empty description="视频加载中..." />
            </div>
            <div v-else-if="lesson.type === 'article'" class="article-content">
              <div v-html="lesson.content"></div>
            </div>
            <div v-else-if="lesson.type === 'lab'" class="lab-environment">
              <!-- TODO: 集成实验环境 -->
              <el-empty description="实验环境准备中..." />
            </div>
          </div>

          <!-- 课时导航 -->
          <div class="lesson-navigation">
            <el-button 
              v-if="navigation.previous"
              type="primary" 
              plain
              @click="goToLesson(navigation.previous.id)"
            >
              <i class="el-icon-arrow-left"></i>
              {{ navigation.previous.title }}
            </el-button>
            <el-button 
              v-if="navigation.next"
              type="primary"
              @click="goToLesson(navigation.next.id)"
            >
              {{ navigation.next.title }}
              <i class="el-icon-arrow-right"></i>
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <!-- 课时进度组件 -->
        <LessonProgress
          v-if="lessonProgress"
          :lesson-id="lessonId"
          :progress="lessonProgress"
          @update:progress="updateProgress"
          class="lesson-progress-widget"
        />

        <!-- 课时笔记 -->
        <el-card class="lesson-notes">
          <template #header>
            <div class="card-header">
              <h3>学习笔记</h3>
              <el-button type="primary" size="small" @click="saveNote">
                保存笔记
              </el-button>
            </div>
          </template>
          
          <el-input
            v-model="noteContent"
            type="textarea"
            :rows="8"
            placeholder="记录你的学习心得..."
          />
        </el-card>

        <!-- 相关资源 -->
        <el-card class="related-resources">
          <template #header>
            <div class="card-header">
              <h3>相关资源</h3>
            </div>
          </template>
          
          <div class="resource-list">
            <div 
              v-for="resource in lesson.resources" 
              :key="resource.id"
              class="resource-item"
            >
              <i :class="getResourceIcon(resource.type)"></i>
              <span class="resource-title">{{ resource.title }}</span>
              <el-button 
                type="primary" 
                link
                size="small"
                @click="downloadResource(resource)"
              >
                下载
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'
import LessonProgress from '@/components/lesson/LessonProgress.vue'
import type { LessonProgress as ILessonProgress } from '@/api/progress'
import progressApi from '@/api/progress'

export default defineComponent({
  name: 'LessonDetail',
  components: {
    LessonProgress
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const lessonId = Number(route.params.lessonId)
    const courseId = Number(route.params.courseId)

    const lesson = ref({
      id: lessonId,
      title: '',
      type: '',
      content: '',
      duration: 0,
      resources: []
    })

    const navigation = ref({
      previous: null,
      next: null,
      total: 0,
      currentIndex: 0
    })

    const lessonProgress = ref<ILessonProgress | null>(null)
    const noteContent = ref('')

    const loadLessonProgress = async () => {
      try {
        const response = await progressApi.getLessonProgress(lessonId)
        lessonProgress.value = response.data
      } catch (error) {
        console.error('加载课时进度失败:', error)
      }
    }

    const updateProgress = (progress: ILessonProgress) => {
      lessonProgress.value = progress
    }

    const formatDuration = (minutes: number) => {
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      return hours > 0 ? `${hours}小时${mins}分钟` : `${mins}分钟`
    }

    const getResourceIcon = (type: string) => {
      const iconMap = {
        pdf: 'el-icon-document',
        video: 'el-icon-video-play',
        code: 'el-icon-code',
        other: 'el-icon-folder'
      }
      return iconMap[type] || 'el-icon-document'
    }

    const downloadResource = (resource: any) => {
      // TODO: 实现资源下载
      ElMessage.success(`开始下载：${resource.title}`)
    }

    const saveNote = async () => {
      // TODO: 实现笔记保存
      ElMessage.success('笔记保存成功')
    }

    const goToLesson = (id: number) => {
      router.push(`/course/${courseId}/lesson/${id}`)
    }

    onMounted(async () => {
      // TODO: 加载课时详情
      // TODO: 加载课时导航信息
      // TODO: 加载课时笔记
      await loadLessonProgress()
    })

    onUnmounted(() => {
      // 在组件卸载时保存学习进度
      if (lessonProgress.value?.status === 'in_progress') {
        progressApi.recordLearningProgress(lessonId, {
          action: 'pause',
          duration: 0
        })
      }
    })

    return {
      lesson,
      navigation,
      lessonProgress,
      noteContent,
      lessonId,
      formatDuration,
      getResourceIcon,
      downloadResource,
      saveNote,
      goToLesson,
      updateProgress
    }
  }
})
</script>

<style scoped>
.lesson-detail {
  padding: 20px;
}

.lesson-content {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2,
.card-header h3 {
  margin: 0;
}

.lesson-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.duration {
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.content-wrapper {
  min-height: 400px;
  margin-bottom: 20px;
}

.lesson-navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--el-border-color-light);
}

.lesson-progress-widget {
  margin-bottom: 20px;
}

.lesson-notes {
  margin-bottom: 20px;
}

.resource-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.resource-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.resource-item:hover {
  background-color: var(--el-color-primary-light-9);
}

.resource-title {
  flex: 1;
  font-size: 14px;
}

.video-player,
.article-content,
.lab-environment {
  min-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style> 