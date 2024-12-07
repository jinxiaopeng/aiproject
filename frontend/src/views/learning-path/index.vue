<template>
  <div class="learning-path">
    <DynamicBackground />
    
    <div class="learning-path-container">
      <div class="path-header">
        <h1 class="path-title">Web安全学习路径</h1>
        <p class="path-description">
          根据难度和知识体系划分的学习路线，帮助你系统地学习Web安全知识
        </p>
      </div>

      <div class="path-content">
        <div class="path-timeline">
          <div v-for="(phase, index) in learningPhases" 
               :key="index" 
               class="path-phase"
               :class="{ 'is-completed': phase.isCompleted }"
          >
            <div class="phase-header">
              <div class="phase-icon">
                <el-icon><component :is="phase.icon" /></el-icon>
              </div>
              <div class="phase-info">
                <h3 class="phase-title">{{ phase.title }}</h3>
                <p class="phase-desc">{{ phase.description }}</p>
              </div>
              <div class="phase-progress">
                <el-progress 
                  type="circle" 
                  :percentage="phase.progress"
                  :stroke-width="4"
                  :width="40"
                  :show-text="false"
                  :color="progressColor"
                />
                <span class="progress-text">{{ phase.progress }}%</span>
              </div>
            </div>

            <div class="phase-content">
              <div v-for="(course, courseIndex) in phase.courses" 
                   :key="courseIndex"
                   class="course-item"
                   :class="{ 
                     'is-completed': course.isCompleted,
                     'is-locked': course.isLocked
                   }"
                   @click="handleCourseClick(course)"
              >
                <div class="course-icon">
                  <el-icon v-if="course.isCompleted"><component :is="CheckIcon" /></el-icon>
                  <el-icon v-else-if="course.isLocked"><component :is="LockIcon" /></el-icon>
                  <el-icon v-else><component :is="DocumentIcon" /></el-icon>
                </div>
                <div class="course-info">
                  <h4 class="course-title">{{ course.title }}</h4>
                  <p class="course-desc">{{ course.description }}</p>
                  <div class="course-meta">
                    <span class="duration">
                      <el-icon><component :is="TimerIcon" /></el-icon>
                      {{ course.duration }}
                    </span>
                    <span class="difficulty" :class="course.difficulty">
                      <el-icon><component :is="OpportunityIcon" /></el-icon>
                      {{ difficultyText[course.difficulty] }}
                    </span>
                  </div>
                </div>
                <el-button 
                  class="course-action"
                  :type="course.isCompleted ? 'success' : 'primary'"
                  :disabled="course.isLocked"
                  @click.stop="handleCourseAction(course)"
                >
                  {{ getCourseActionText(course) }}
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <div class="path-sidebar">
          <div class="progress-card">
            <h3>总体进度</h3>
            <el-progress 
              type="dashboard"
              :percentage="totalProgress"
              :stroke-width="6"
              :width="120"
              :color="progressColor"
            />
            <div class="progress-stats">
              <div class="stat-item">
                <span class="label">已完成课程</span>
                <span class="value">{{ completedCourses }}/{{ totalCourses }}</span>
              </div>
              <div class="stat-item">
                <span class="label">学习时长</span>
                <span class="value">{{ totalDuration }}</span>
              </div>
            </div>
          </div>

          <div class="achievement-card">
            <h3>最近成就</h3>
            <div class="achievement-list">
              <div v-for="(achievement, index) in recentAchievements" 
                   :key="index"
                   class="achievement-item"
              >
                <el-avatar :size="40" :src="achievement.icon" />
                <div class="achievement-info">
                  <h4>{{ achievement.title }}</h4>
                  <p>{{ achievement.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DynamicBackground from '@/components/DynamicBackground.vue'
import {
  Check as CheckIcon,
  Lock as LockIcon,
  Document as DocumentIcon,
  Timer as TimerIcon,
  Connection as OpportunityIcon,
  Location as GuideIcon,
  Setting as OperationIcon,
  Trophy as TrophyIcon
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import type { ProgressFn } from 'element-plus'

interface Course {
  id: number
  title: string
  description: string
  duration: string
  difficulty: 'easy' | 'medium' | 'hard'
  isCompleted: boolean
  isLocked: boolean
  path: string
}

interface Phase {
  title: string
  description: string
  icon: string
  progress: number
  isCompleted: boolean
  courses: Course[]
}

const router = useRouter()

// 难度文本映射
const difficultyText = {
  easy: '入门',
  medium: '进阶',
  hard: '高级'
}

// 进度条颜色
const progressColor = computed<ProgressFn>(() => (percentage: number) => {
  if (percentage < 50) return '#909399'
  if (percentage < 100) return '#409EFF'
  return '#67C23A'
})

// 学习阶段数据
const learningPhases = ref<Phase[]>([
  {
    title: '基础入门',
    description: 'Web安全基础知识和工具使用',
    icon: GuideIcon,
    progress: 100,
    isCompleted: true,
    courses: [
      {
        id: 1,
        title: 'Web安全概述',
        description: '了解Web安全的基本概念和重要性',
        duration: '2小时',
        difficulty: 'easy',
        isCompleted: true,
        isLocked: false,
        path: '/courses/web-security-intro'
      },
      {
        id: 2,
        title: '常见工具使用',
        description: '学习基本的Web安全测试工具',
        duration: '3小时',
        difficulty: 'easy',
        isCompleted: true,
        isLocked: false,
        path: '/courses/security-tools'
      }
    ]
  },
  {
    title: '漏洞原理',
    description: '常见Web安全漏洞原理和防护',
    icon: OperationIcon,
    progress: 60,
    isCompleted: false,
    courses: [
      {
        id: 3,
        title: 'SQL注入基础',
        description: '理解SQL注入漏洞的原理和利用方式',
        duration: '4小时',
        difficulty: 'medium',
        isCompleted: true,
        isLocked: false,
        path: '/courses/sql-injection'
      },
      {
        id: 4,
        title: 'XSS跨站脚本',
        description: '学习XSS漏洞的类型和防护方法',
        duration: '3小时',
        difficulty: 'medium',
        isCompleted: false,
        isLocked: false,
        path: '/courses/xss'
      },
      {
        id: 5,
        title: 'CSRF攻击',
        description: '了解CSRF攻击的原理和防御措施',
        duration: '2小时',
        difficulty: 'medium',
        isCompleted: false,
        isLocked: false,
        path: '/courses/csrf'
      }
    ]
  },
  {
    title: '高级技术',
    description: '深入的Web安全技术和实战方法',
    icon: TrophyIcon,
    progress: 0,
    isCompleted: false,
    courses: [
      {
        id: 6,
        title: '渗透测试方法论',
        description: '系统的渗透测试方法和流程',
        duration: '6小时',
        difficulty: 'hard',
        isCompleted: false,
        isLocked: true,
        path: '/courses/pentest-methodology'
      },
      {
        id: 7,
        title: '高级漏洞利用',
        description: '复杂漏洞的发现与利用技术',
        duration: '8小时',
        difficulty: 'hard',
        isCompleted: false,
        isLocked: true,
        path: '/courses/advanced-exploitation'
      }
    ]
  }
])

// 最近成就数据
const recentAchievements = ref([
  {
    icon: '/icons/achievement-basic.png',
    title: '入门成就',
    description: '完成基础入门阶段的所有课程'
  },
  {
    icon: '/icons/achievement-sql.png',
    title: 'SQL注入专家',
    description: '完成SQL注入相关的所有练习'
  }
])

// 计算总进度
const totalProgress = computed(() => {
  const total = learningPhases.value.reduce((sum, phase) => sum + phase.courses.length, 0)
  const completed = learningPhases.value.reduce((sum, phase) => 
    sum + phase.courses.filter(course => course.isCompleted).length, 0
  )
  return Math.round((completed / total) * 100)
})

// 计算完成的课程数量
const completedCourses = computed(() => 
  learningPhases.value.reduce((sum, phase) => 
    sum + phase.courses.filter(course => course.isCompleted).length, 0
  )
)

// 计算总课程数量
const totalCourses = computed(() => 
  learningPhases.value.reduce((sum, phase) => sum + phase.courses.length, 0)
)

// 计算总学习时长
const totalDuration = computed(() => {
  const hours = learningPhases.value.reduce((sum, phase) => 
    sum + phase.courses.reduce((courseSum, course) => 
      courseSum + parseInt(course.duration), 0
    ), 0
  )
  return `${hours}小时`
})

// 处理课程点击
const handleCourseClick = (course: Course) => {
  if (course.isLocked) {
    ElMessage.warning('请先完成前置课程')
    return
  }
  router.push(`/learning-path/courses/${course.id}`)
}

// 获取课程操作按钮文本
const getCourseActionText = (course: Course) => {
  if (course.isCompleted) return '复习'
  if (course.isLocked) return '未解锁'
  return '开始学习'
}

// 学习进度持久化
const saveProgress = (courseId: number) => {
  const progress = localStorage.getItem('learningProgress') 
    ? JSON.parse(localStorage.getItem('learningProgress') || '{}')
    : {}
  progress[courseId] = true
  localStorage.setItem('learningProgress', JSON.stringify(progress))
}

const loadProgress = () => {
  const progress = localStorage.getItem('learningProgress')
    ? JSON.parse(localStorage.getItem('learningProgress') || '{}')
    : {}
  
  learningPhases.value.forEach(phase => {
    phase.courses.forEach(course => {
      if (progress[course.id]) {
        course.isCompleted = true
      }
    })
  })
}

// 解锁逻辑
const checkAndUnlockCourses = () => {
  learningPhases.value.forEach((phase, phaseIndex) => {
    if (phaseIndex === 0) {
      phase.courses.forEach(course => course.isLocked = false)
      return
    }

    const previousPhase = learningPhases.value[phaseIndex - 1]
    const previousPhaseCompleted = previousPhase.courses.every(course => course.isCompleted)
    
    phase.courses.forEach(course => {
      course.isLocked = !previousPhaseCompleted
    })
  })
}

// 课程完成处理
const completeCourse = (course: Course) => {
  course.isCompleted = true
  saveProgress(course.id)
  
  // 更新阶段进度
  learningPhases.value.forEach(phase => {
    const completedCount = phase.courses.filter(c => c.isCompleted).length
    phase.progress = Math.round((completedCount / phase.courses.length) * 100)
    phase.isCompleted = phase.progress === 100
  })
  
  checkAndUnlockCourses()
  ElMessage.success('课程完成！')
}

// 初始化
onMounted(() => {
  loadProgress()
  checkAndUnlockCourses()
})

// 修改课程操作处理
const handleCourseAction = (course: Course) => {
  if (course.isLocked) return
  
  if (!course.isCompleted) {
    router.push(`/learning-path/courses/${course.id}`)
  } else {
    // 复习模式
    router.push({
      path: `/learning-path/courses/${course.id}`,
      query: { mode: 'review' }
    })
  }
}
</script>

<style lang="scss" scoped>
.learning-path {
  min-height: 100vh;
  position: relative;
}

.learning-path-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.path-header {
  margin-bottom: 32px;
  text-align: center;
  padding: 40px 0;
  background: rgba(42, 60, 84, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);

  .path-title {
    font-size: 32px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 12px;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
  }

  .path-description {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.8);
    max-width: 600px;
    margin: 0 auto;
  }
}

.path-content {
  display: flex;
  gap: 24px;
}

.path-timeline {
  flex: 1;
}

.path-phase {
  background: rgba(42, 60, 84, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
  }

  &.is-completed {
    border-left: 4px solid #409EFF;
    background: linear-gradient(to right, rgba(64, 158, 255, 0.1) 0%, rgba(42, 60, 84, 0.6) 8%);
  }
}

.phase-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;

  .phase-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);

    .el-icon {
      font-size: 24px;
      color: #409EFF;
    }
  }

  .phase-info {
    flex: 1;

    .phase-title {
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 4px;
      color: #ffffff;
      display: flex;
      align-items: center;
    }

    .phase-desc {
      font-size: 14px;
      color: rgba(255, 255, 255, 0.8);
      line-height: 1.5;
    }
  }
}

.course-item {
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: 8px;
  background: rgba(42, 60, 84, 0.4);
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    border-color: rgba(255, 255, 255, 0.2);
    background: rgba(42, 60, 84, 0.6);
  }

  &.is-completed {
    background: linear-gradient(to right, rgba(64, 158, 255, 0.1), rgba(42, 60, 84, 0.4));
    border-color: #409EFF;
  }

  &.is-locked {
    opacity: 0.6;
    border-style: dashed;
  }

  .course-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: 16px;
    transition: all 0.3s ease;

    .el-icon {
      font-size: 20px;
      color: #409EFF;
    }
  }

  .course-info {
    flex: 1;

    .course-title {
      font-size: 16px;
      font-weight: bold;
      margin-bottom: 4px;
      color: #ffffff;
    }

    .course-desc {
      font-size: 14px;
      color: rgba(255, 255, 255, 0.8);
      margin-bottom: 8px;
      line-height: 1.5;
    }

    .course-meta {
      display: flex;
      gap: 16px;
      font-size: 13px;
      color: rgba(255, 255, 255, 0.6);

      .el-icon {
        margin-right: 4px;
        vertical-align: middle;
      }

      .difficulty {
        &.easy { 
          color: #67C23A;
          .el-icon { color: #67C23A; }
        }
        &.medium { 
          color: #E6A23C;
          .el-icon { color: #E6A23C; }
        }
        &.hard { 
          color: #F56C6C;
          .el-icon { color: #F56C6C; }
        }
      }
    }
  }

  .course-action {
    margin-left: 16px;
    min-width: 90px;

    &.el-button--primary {
      background: #409EFF;
      border-color: #409EFF;
      color: #ffffff;

      &:hover {
        background: #66b1ff;
        border-color: #66b1ff;
      }
    }

    &.el-button--success {
      background: #67C23A;
      border-color: #67C23A;

      &:hover {
        background: #85ce61;
        border-color: #85ce61;
      }
    }
  }
}

.path-sidebar {
  width: 320px;

  .progress-card,
  .achievement-card {
    background: rgba(42, 60, 84, 0.6);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);

    h3 {
      font-size: 18px;
      font-weight: bold;
      margin-bottom: 24px;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 8px;

      &::before {
        content: '';
        display: block;
        width: 4px;
        height: 16px;
        background: #409EFF;
        border-radius: 2px;
      }
    }
  }

  .progress-stats {
    margin-top: 24px;
    padding-top: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);

    .stat-item {
      display: flex;
      justify-content: space-between;
      margin-bottom: 12px;
      padding: 8px 12px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 6px;

      .label {
        color: rgba(255, 255, 255, 0.8);
      }

      .value {
        font-weight: bold;
        color: #409EFF;
      }
    }
  }

  .achievement-list {
    .achievement-item {
      display: flex;
      align-items: center;
      margin-bottom: 16px;
      padding: 12px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      transition: all 0.3s ease;

      &:hover {
        border-color: #409EFF;
        box-shadow: 0 4px 12px rgba(0, 255, 157, 0.1);
      }

      .el-avatar {
        margin-right: 12px;
        border: 2px solid rgba(255, 255, 255, 0.1);
      }

      .achievement-info {
        flex: 1;

        h4 {
          font-size: 14px;
          font-weight: bold;
          margin-bottom: 4px;
          color: #ffffff;
        }

        p {
          font-size: 12px;
          color: rgba(255, 255, 255, 0.8);
          line-height: 1.5;
        }
      }
    }
  }
}

:deep(.el-progress-circle__track) {
  stroke: rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-progress-circle__path) {
  stroke: #409EFF !important;
}

:deep(.el-progress-bar__outer) {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-progress-bar__inner) {
  background-color: #409EFF !important;
}

:deep(.el-button) {
  background: rgba(64, 158, 255, 0.1);
  border-color: #409EFF;
  color: #ffffff;

  &:hover {
    background: rgba(64, 158, 255, 0.2);
    border-color: #409EFF;
    color: #ffffff;
  }

  &.el-button--primary {
    background: #409EFF;
    border-color: #409EFF;
    color: #ffffff;

    &:hover {
      background: #66b1ff;
      border-color: #66b1ff;
    }
  }

  &.el-button--success {
    background: #67C23A;
    border-color: #67C23A;

    &:hover {
      background: #85ce61;
      border-color: #85ce61;
    }
  }
}

@media screen and (max-width: 768px) {
  .path-content {
    flex-direction: column;
  }

  .path-sidebar {
    width: 100%;
  }

  .path-header {
    padding: 24px 16px;

    .path-title {
      font-size: 24px;
    }

    .path-description {
      font-size: 14px;
    }
  }
}
</style> 