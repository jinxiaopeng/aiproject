<!-- 课时进度跟踪组件 -->
<template>
  <div class="lesson-progress">
    <div class="progress-header">
      <div class="progress-info">
        <div class="progress-status" :class="progress.status">
          {{ statusText }}
        </div>
        <div class="progress-time">
          学习时长：{{ formatDuration(progress.learningTime) }}
        </div>
      </div>
      <div class="progress-actions">
        <el-button 
          type="primary" 
          :icon="isPlaying ? 'Pause' : 'VideoPlay'"
          @click="togglePlay"
        >
          {{ isPlaying ? '暂停' : '继续学习' }}
        </el-button>
        <el-button 
          type="success" 
          icon="Check"
          @click="completeLesson"
          :disabled="progress.status === 'completed'"
        >
          完成学习
        </el-button>
      </div>
    </div>

    <div class="progress-bar">
      <div class="progress-track">
        <div 
          class="progress-fill" 
          :style="{ width: `${progress.progress}%` }"
          :class="{ 'completed': progress.status === 'completed' }"
        >
          <span class="progress-text">{{ progress.progress.toFixed(1) }}%</span>
        </div>
      </div>
    </div>

    <div class="learning-timeline">
      <div class="timeline-item" v-for="record in learningRecords" :key="record.id">
        <div class="timeline-icon" :class="record.action">
          <i :class="getActionIcon(record.action)"></i>
        </div>
        <div class="timeline-content">
          <div class="timeline-action">{{ getActionText(record.action) }}</div>
          <div class="timeline-time">{{ formatDate(record.createdAt) }}</div>
          <div class="timeline-duration" v-if="record.duration">
            持续时间：{{ formatDuration(record.duration) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, onUnmounted } from 'vue'
import type { LessonProgress, LearningRecord } from '@/api/progress'
import progressApi from '@/api/progress'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'

export default defineComponent({
  name: 'LessonProgress',
  props: {
    lessonId: {
      type: Number,
      required: true
    },
    progress: {
      type: Object as () => LessonProgress,
      required: true
    }
  },
  emits: ['update:progress'],
  setup(props, { emit }) {
    const isPlaying = ref(false)
    const startTime = ref<number>(0)
    const learningRecords = ref<LearningRecord[]>([])
    let timer: number | null = null

    const statusText = computed(() => {
      const statusMap = {
        not_started: '未开始',
        in_progress: '学习中',
        completed: '已完成'
      }
      return statusMap[props.progress.status] || '未知状态'
    })

    const formatDuration = (minutes: number) => {
      const hours = Math.floor(minutes / 60)
      const mins = minutes % 60
      return hours > 0 ? `${hours}小时${mins}分钟` : `${mins}分钟`
    }

    const formatDate = (dateStr: string) => {
      return dayjs(dateStr).format('YYYY-MM-DD HH:mm:ss')
    }

    const getActionIcon = (action: string) => {
      const iconMap = {
        start: 'fas fa-play',
        pause: 'fas fa-pause',
        resume: 'fas fa-play',
        complete: 'fas fa-check'
      }
      return iconMap[action] || 'fas fa-circle'
    }

    const getActionText = (action: string) => {
      const textMap = {
        start: '开始学习',
        pause: '暂停学习',
        resume: '继续学习',
        complete: '完成学习'
      }
      return textMap[action] || action
    }

    const recordLearningAction = async (action: string, duration = 0) => {
      try {
        const record: LearningRecord = {
          action,
          position: 0, // 如果是视频课程，这里可以记录播放位置
          duration
        }
        const response = await progressApi.recordLearningProgress(props.lessonId, record)
        emit('update:progress', response.data)
        return response.data
      } catch (error) {
        ElMessage.error('记录学习进度失败')
        console.error('记录学习进度失败:', error)
      }
    }

    const startTimer = () => {
      if (timer) return
      startTime.value = Date.now()
      timer = window.setInterval(() => {
        // 每分钟更新一次学习时长
        const duration = Math.floor((Date.now() - startTime.value) / 60000)
        if (duration > 0) {
          recordLearningAction('update', duration)
          startTime.value = Date.now()
        }
      }, 60000) // 每分钟检查一次
    }

    const stopTimer = () => {
      if (timer) {
        window.clearInterval(timer)
        timer = null
      }
      if (startTime.value) {
        const duration = Math.floor((Date.now() - startTime.value) / 60000)
        if (duration > 0) {
          recordLearningAction('pause', duration)
        }
        startTime.value = 0
      }
    }

    const togglePlay = async () => {
      if (isPlaying.value) {
        await recordLearningAction('pause')
        stopTimer()
      } else {
        const action = props.progress.status === 'not_started' ? 'start' : 'resume'
        await recordLearningAction(action)
        startTimer()
      }
      isPlaying.value = !isPlaying.value
    }

    const completeLesson = async () => {
      if (isPlaying.value) {
        stopTimer()
        isPlaying.value = false
      }
      await recordLearningAction('complete')
      ElMessage.success('恭喜你完成本课时的学习！')
    }

    onMounted(() => {
      if (props.progress.status === 'not_started') {
        recordLearningAction('start')
      }
    })

    onUnmounted(() => {
      if (isPlaying.value) {
        stopTimer()
      }
    })

    return {
      isPlaying,
      learningRecords,
      statusText,
      formatDuration,
      formatDate,
      getActionIcon,
      getActionText,
      togglePlay,
      completeLesson
    }
  }
})
</script>

<style scoped>
.lesson-progress {
  background: var(--el-bg-color);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.progress-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.progress-status {
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 14px;
}

.progress-status.not_started {
  background: var(--el-color-info-light-9);
  color: var(--el-color-info);
}

.progress-status.in_progress {
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.progress-status.completed {
  background: var(--el-color-success-light-9);
  color: var(--el-color-success);
}

.progress-time {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.progress-actions {
  display: flex;
  gap: 12px;
}

.progress-bar {
  margin-bottom: 20px;
}

.progress-track {
  background: var(--el-color-info-light-8);
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--el-color-primary);
  border-radius: 4px;
  transition: width 0.3s ease;
  position: relative;
}

.progress-fill.completed {
  background: var(--el-color-success);
}

.progress-text {
  position: absolute;
  right: 0;
  top: -20px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.learning-timeline {
  margin-top: 20px;
  border-top: 1px solid var(--el-border-color-light);
  padding-top: 20px;
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
}

.timeline-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  color: white;
}

.timeline-icon.start,
.timeline-icon.resume {
  background: var(--el-color-primary);
}

.timeline-icon.pause {
  background: var(--el-color-warning);
}

.timeline-icon.complete {
  background: var(--el-color-success);
}

.timeline-content {
  flex: 1;
}

.timeline-action {
  font-size: 14px;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
}

.timeline-time,
.timeline-duration {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}
</style> 