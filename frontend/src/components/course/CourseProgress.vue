<!-- 课程进度组件 -->
<template>
  <div class="course-progress">
    <!-- 总体进度 -->
    <div class="progress-overview">
      <el-progress
        type="circle"
        :percentage="progress.progress"
        :status="progressStatus"
        :width="120"
      >
        <template #default="{ percentage }">
          <div class="progress-info">
            <span class="percentage">{{ percentage }}%</span>
            <span class="status-text">{{ statusText }}</span>
          </div>
        </template>
      </el-progress>

      <div class="progress-stats">
        <div class="stat-item">
          <div class="stat-value">{{ progress.completed_lessons }}</div>
          <div class="stat-label">已完成课时</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ progress.total_lessons }}</div>
          <div class="stat-label">总课时</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ formatDuration(progress.learning_time) }}</div>
          <div class="stat-label">学习时长</div>
        </div>
      </div>
    </div>

    <!-- 等级信息 -->
    <div v-if="userLevel" class="level-info">
      <div class="level-header">
        <div class="level-title">
          <span class="level-text">Level {{ userLevel.level }}</span>
          <el-tag size="small" type="success">{{ getLevelTitle(userLevel.level) }}</el-tag>
        </div>
        <div class="points-info">
          {{ userLevel.current_points }} / {{ userLevel.next_level_points }} 积分
        </div>
      </div>

      <el-progress
        :percentage="levelProgress"
        :format="formatLevelProgress"
        :stroke-width="10"
        class="level-progress"
      />

      <div class="level-rewards">
        <div class="reward-item" v-for="reward in levelRewards" :key="reward.level">
          <el-avatar
            :size="40"
            :src="reward.icon"
            :class="{ 'locked': userLevel.level < reward.level }"
          />
          <div class="reward-info">
            <div class="reward-name">{{ reward.name }}</div>
            <div class="reward-desc">{{ reward.description }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 学习路径 -->
    <div class="learning-path">
      <h3>学习路径</h3>
      <el-steps :active="activeStep" finish-status="success" direction="vertical">
        <el-step
          v-for="(step, index) in learningSteps"
          :key="index"
          :title="step.title"
          :description="step.description"
        >
          <template #icon>
            <el-icon v-if="index < activeStep">
              <Check />
            </el-icon>
            <el-icon v-else-if="index === activeStep">
              <Loading />
            </el-icon>
          </template>
        </el-step>
      </el-steps>
    </div>

    <!-- 成就展示 -->
    <div class="achievements">
      <h3>获得的成就</h3>
      <div class="achievement-list">
        <el-tooltip
          v-for="achievement in achievements"
          :key="achievement.id"
          :content="achievement.description"
          placement="top"
        >
          <div
            class="achievement-item"
            :class="{ 'locked': !achievement.unlocked }"
          >
            <el-avatar
              :size="50"
              :src="achievement.icon"
              :class="{ 'grayscale': !achievement.unlocked }"
            />
            <span class="achievement-name">{{ achievement.name }}</span>
          </div>
        </el-tooltip>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Check, Loading } from '@element-plus/icons-vue'
import type { CourseProgress, UserLevel } from '@/api/progress'

// Props
const props = defineProps<{
  progress: CourseProgress
  userLevel?: UserLevel
}>()

// 计算属性
const progressStatus = computed(() => {
  const progress = props.progress.progress
  if (progress === 100) return 'success'
  if (progress >= 60) return 'warning'
  return ''
})

const statusText = computed(() => {
  const progress = props.progress.progress
  if (progress === 100) return '已完成'
  if (progress >= 60) return '进行中'
  return '未开始'
})

const levelProgress = computed(() => {
  if (!props.userLevel) return 0
  return (props.userLevel.current_points / props.userLevel.next_level_points) * 100
})

const activeStep = computed(() => {
  return Math.floor((props.progress.progress / 100) * learningSteps.length)
})

// 等级奖励
const levelRewards = [
  {
    level: 1,
    name: '初学者',
    description: '完成第一课程',
    icon: '/rewards/beginner.png'
  },
  {
    level: 5,
    name: '学习达人',
    description: '完成5门课程',
    icon: '/rewards/master.png'
  },
  {
    level: 10,
    name: '知识专家',
    description: '完成10门课程',
    icon: '/rewards/expert.png'
  }
]

// 学习路径
const learningSteps = [
  {
    title: '开始学习',
    description: '观看课程介绍视频'
  },
  {
    title: '基础知识',
    description: '完成基础理论学习'
  },
  {
    title: '实践练习',
    description: '完成相关练习题'
  },
  {
    title: '项目实战',
    description: '完成实战项目'
  },
  {
    title: '课程测验',
    description: '通过课程测验'
  }
]

// 成就列表
const achievements = [
  {
    id: 1,
    name: '第一步',
    description: '完成第一节课',
    icon: '/achievements/first-step.png',
    unlocked: true
  },
  {
    id: 2,
    name: '勤奋学习',
    description: '连续学习7天',
    icon: '/achievements/diligent.png',
    unlocked: false
  },
  {
    id: 3,
    name: '完美成绩',
    description: '测验满分',
    icon: '/achievements/perfect.png',
    unlocked: false
  }
]

// 方法
const formatDuration = (minutes: number) => {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return hours > 0 ? `${hours}小时${mins}分钟` : `${mins}分钟`
}

const formatLevelProgress = (percentage: number) => {
  if (!props.userLevel) return ''
  return `${props.userLevel.current_points}/${props.userLevel.next_level_points}`
}

const getLevelTitle = (level: number) => {
  if (level >= 10) return '专家'
  if (level >= 5) return '进阶'
  return '新手'
}
</script>

<style scoped>
.course-progress {
  padding: 24px;
}

.progress-overview {
  display: flex;
  align-items: center;
  gap: 48px;
  margin-bottom: 32px;
}

.progress-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.percentage {
  font-size: 24px;
  font-weight: 500;
  line-height: 1.2;
}

.status-text {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.progress-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin-top: 4px;
}

.level-info {
  background-color: var(--el-fill-color-light);
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 32px;
}

.level-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.level-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.level-text {
  font-size: 18px;
  font-weight: 500;
}

.points-info {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.level-progress {
  margin-bottom: 24px;
}

.level-rewards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.reward-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background-color: var(--el-bg-color);
  border-radius: 4px;
}

.reward-info {
  flex: 1;
}

.reward-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.reward-desc {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.locked {
  opacity: 0.5;
}

.learning-path {
  margin-bottom: 32px;
}

.learning-path h3 {
  margin: 0 0 16px;
}

.achievements {
  margin-bottom: 32px;
}

.achievements h3 {
  margin: 0 0 16px;
}

.achievement-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
}

.achievement-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background-color: var(--el-fill-color-light);
  border-radius: 8px;
  transition: all 0.3s ease;
}

.achievement-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--el-box-shadow-light);
}

.achievement-name {
  font-size: 14px;
  text-align: center;
}

.grayscale {
  filter: grayscale(100%);
}
</style> 