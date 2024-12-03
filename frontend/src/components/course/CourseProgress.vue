<!-- 课程进度组件 -->
<template>
  <div class="course-progress">
    <div class="progress-header">
      <h3>学习进度</h3>
      <div class="progress-status" :class="progress.status">
        {{ statusText }}
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

    <div class="progress-stats">
      <div class="stat-item">
        <div class="stat-label">已完成课时</div>
        <div class="stat-value">{{ progress.completedLessons }}/{{ progress.totalLessons }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-label">学习时长</div>
        <div class="stat-value">{{ formatDuration(progress.learningTime) }}</div>
      </div>
    </div>

    <div class="progress-timeline" v-if="showTimeline">
      <div class="timeline-item">
        <div class="timeline-icon" :class="{ active: progress.startedAt }">
          <i class="fas fa-play"></i>
        </div>
        <div class="timeline-content">
          <div class="timeline-title">开始学习</div>
          <div class="timeline-time" v-if="progress.startedAt">
            {{ formatDate(progress.startedAt) }}
          </div>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-icon" :class="{ active: progress.completedAt }">
          <i class="fas fa-check"></i>
        </div>
        <div class="timeline-content">
          <div class="timeline-title">完成课程</div>
          <div class="timeline-time" v-if="progress.completedAt">
            {{ formatDate(progress.completedAt) }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'
import type { CourseProgress } from '@/api/progress'
import dayjs from 'dayjs'

export default defineComponent({
  name: 'CourseProgress',
  props: {
    progress: {
      type: Object as () => CourseProgress,
      required: true
    },
    showTimeline: {
      type: Boolean,
      default: true
    }
  },
  setup(props) {
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
      return dayjs(dateStr).format('YYYY-MM-DD HH:mm')
    }

    return {
      statusText,
      formatDuration,
      formatDate
    }
  }
})
</script>

<style scoped>
.course-progress {
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

.progress-header h3 {
  margin: 0;
  font-size: 18px;
  color: var(--el-text-color-primary);
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

.progress-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin-bottom: 4px;
}

.stat-value {
  font-size: 16px;
  color: var(--el-text-color-primary);
  font-weight: bold;
}

.progress-timeline {
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
  background: var(--el-color-info-light-8);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.timeline-icon.active {
  background: var(--el-color-primary);
  color: white;
}

.timeline-content {
  flex: 1;
}

.timeline-title {
  font-size: 14px;
  color: var(--el-text-color-primary);
  margin-bottom: 4px;
}

.timeline-time {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}
</style> 