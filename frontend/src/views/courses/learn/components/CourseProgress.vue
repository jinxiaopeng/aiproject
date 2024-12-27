<template>
  <div class="course-progress">
    <div class="progress-header">
      <h3>学习进度</h3>
      <div class="overall-progress">
        <el-progress
          :percentage="totalProgress"
          :format="formatPercentage"
          :stroke-width="8"
          status="success"
        />
      </div>
    </div>

    <div class="progress-stats">
      <div class="stat-item">
        <div class="label">已学习时长</div>
        <div class="value">{{ formatDuration(totalWatchTime) }}</div>
      </div>
      <div class="stat-item">
        <div class="label">完成章节</div>
        <div class="value">{{ completedChapters }}/{{ totalChapters }}</div>
      </div>
      <div class="stat-item">
        <div class="label">学习天数</div>
        <div class="value">{{ studyDays }}天</div>
      </div>
    </div>

    <div class="milestone-list">
      <h4>学习里程碑</h4>
      <div class="milestones">
        <div
          v-for="milestone in milestones"
          :key="milestone.id"
          class="milestone-item"
          :class="{ completed: milestone.completed }"
        >
          <el-icon :size="20">
            <component :is="milestone.completed ? 'CircleCheckFilled' : 'Clock'" />
          </el-icon>
          <div class="milestone-info">
            <div class="title">{{ milestone.title }}</div>
            <div class="description">{{ milestone.description }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { CircleCheckFilled, Clock } from '@element-plus/icons-vue'

interface Milestone {
  id: number
  title: string
  description: string
  completed: boolean
}

const props = defineProps<{
  courseId: number
  chapterId: number
  totalDuration: number
  currentTime: number
}>()

// 学习进度数据
const totalWatchTime = ref(0)
const studyDays = ref(1)
const milestones = ref<Milestone[]>([
  {
    id: 1,
    title: '开始学习',
    description: '观看第一个视频',
    completed: true
  },
  {
    id: 2,
    title: '完成第一章',
    description: '完整观看第一章的所有内容',
    completed: false
  },
  {
    id: 3,
    title: '记录笔记',
    description: '添加第一条学习笔记',
    completed: false
  },
  {
    id: 4,
    title: '参与讨论',
    description: '发表第一条评论',
    completed: false
  },
  {
    id: 5,
    title: '完成课程',
    description: '完成所有章节的学习',
    completed: false
  }
])

// 计算总进度
const totalProgress = computed(() => {
  return Math.min(100, Math.round((props.currentTime / props.totalDuration) * 100))
})

// 计算完成的章节数
const completedChapters = computed(() => {
  // TODO: 从本地存储获取完成的章节数
  return 0
})

const totalChapters = computed(() => {
  // TODO: 从父组件获取总章节数
  return 5
})

// 格式化百分比
const formatPercentage = (percentage: number) => {
  return percentage === 100 ? '已完成' : `${percentage}%`
}

// 格式化时长
const formatDuration = (seconds: number) => {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  
  if (h > 0) {
    return `${h}小时${m}分钟`
  }
  return `${m}分钟`
}

// 从本地存储加载进度数据
const loadProgressData = () => {
  const savedProgress = localStorage.getItem(
    `course-${props.courseId}-progress`
  )
  if (savedProgress) {
    const data = JSON.parse(savedProgress)
    totalWatchTime.value = data.totalWatchTime || 0
    studyDays.value = data.studyDays || 1
  }
}

// 保存进度数据到本地存储
const saveProgressData = () => {
  localStorage.setItem(
    `course-${props.courseId}-progress`,
    JSON.stringify({
      totalWatchTime: totalWatchTime.value,
      studyDays: studyDays.value
    })
  )
}

// 更新学习时长
const updateWatchTime = () => {
  totalWatchTime.value += 1
  saveProgressData()
}

// 初始化
loadProgressData()

// 每秒更新学习时长
setInterval(updateWatchTime, 1000)
</script>

<style lang="scss" scoped>
.course-progress {
  margin-top: 2rem;
  padding: 1rem;
  background: var(--el-bg-color-page);
  border-radius: 8px;
  
  .progress-header {
    margin-bottom: 1.5rem;
    
    h3 {
      margin: 0 0 1rem;
      font-size: 1.2rem;
      color: var(--el-text-color-primary);
    }
  }
  
  .progress-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
    
    .stat-item {
      text-align: center;
      padding: 1rem;
      background: var(--el-bg-color);
      border-radius: 4px;
      border: 1px solid var(--el-border-color-light);
      
      .label {
        color: var(--el-text-color-secondary);
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
      }
      
      .value {
        font-size: 1.2rem;
        font-weight: 500;
        color: var(--el-color-primary);
      }
    }
  }
  
  .milestone-list {
    h4 {
      margin: 0 0 1rem;
      font-size: 1.1rem;
      color: var(--el-text-color-primary);
    }
    
    .milestones {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }
    
    .milestone-item {
      display: flex;
      align-items: flex-start;
      gap: 0.75rem;
      padding: 0.75rem;
      background: var(--el-bg-color);
      border-radius: 4px;
      border: 1px solid var(--el-border-color-light);
      
      .el-icon {
        margin-top: 0.25rem;
        color: var(--el-text-color-secondary);
      }
      
      &.completed {
        background: var(--el-color-success-light-9);
        border-color: var(--el-color-success-light-5);
        
        .el-icon {
          color: var(--el-color-success);
        }
        
        .title {
          color: var(--el-color-success);
        }
      }
      
      .milestone-info {
        flex: 1;
        
        .title {
          font-weight: 500;
          margin-bottom: 0.25rem;
        }
        
        .description {
          font-size: 0.9rem;
          color: var(--el-text-color-secondary);
        }
      }
    }
  }
}
</style> 