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

    <!-- 课程详情对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="currentCourse?.title"
      width="60%"
      destroy-on-close
    >
      <div class="course-details" v-if="currentCourse">
        <h3>课程简介</h3>
        <p>{{ currentCourse.description }}</p>

        <h3>课程大纲</h3>
        <div class="course-outline">
          <el-collapse>
            <el-collapse-item v-for="(section, index) in currentCourse.sections" :key="index" :title="section.title">
              <p>{{ section.description }}</p>
              <div class="section-materials" v-if="section.materials && section.materials.length">
                <div v-for="(material, mIndex) in section.materials" :key="mIndex" class="material-item">
                  <el-icon><Document /></el-icon>
                  <span>{{ material.title }}</span>
                  <el-button link type="primary" @click="openMaterial(material)">
                    查看
                  </el-button>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>

        <h3>学习目标</h3>
        <ul>
          <li v-for="(objective, index) in currentCourse.objectives" :key="index">
            {{ objective }}
          </li>
        </ul>

        <h3>课程要求</h3>
        <ul>
          <li v-for="(prerequisite, index) in currentCourse.prerequisites" :key="index">
            {{ prerequisite }}
          </li>
        </ul>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="startLearning(currentCourse)">
            {{ currentCourse?.isCompleted ? '复习课程' : '开始学习' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
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
  objectives: string[]
  materials: { type: string; title: string; url: string }[]
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
        path: '/courses/web-security-intro',
        objectives: [
          '理解Web安全的基本概念',
          '了解常见的Web安全威胁',
          '掌握基本的安全测试方法'
        ],
        materials: [
          { 
            id: 'web-basic-1',
            type: 'video',
            title: 'Web安全基础概念',
            description: '介绍Web安全的基本概念和重要性',
            url: '/materials/videos/web-security-basics.mp4',
            duration: '45分钟'
          },
          { 
            id: 'web-basic-2',
            type: 'document',
            title: '安全测试指南',
            description: '详细的Web安全测试方法和流程',
            url: '/materials/docs/security-guide.pdf',
            pages: 25
          },
          {
            id: 'web-basic-3',
            type: 'quiz',
            title: '基础概念测试',
            description: '测试对Web安全基础概念的理解',
            questionCount: 10
          },
          {
            id: 'web-basic-4',
            type: 'lab',
            title: '基础安全实验',
            description: '通过实验加深对Web安全的理解',
            difficulty: 'easy',
            estimatedTime: '30分钟'
          },
          {
            id: 'web-basic-5',
            type: 'code',
            title: '安全编码示例',
            description: '常见的安全编码实践示例',
            language: 'javascript',
            difficulty: 'easy'
          }
        ]
      },
      {
        id: 2,
        title: '安全测试环境搭建',
        description: '学习配置基本的Web安全测试环境',
        duration: '3小时',
        difficulty: 'easy',
        isCompleted: true,
        isLocked: false,
        path: '/courses/security-env-setup',
        objectives: [
          '搭建本地测试环境',
          '配置常用安全工具',
          '了解基本的测试方法'
        ],
        materials: [
          { type: 'video', title: '环境搭建教程', url: '/materials/env-setup.mp4' },
          { type: 'document', title: '工具配置手册', url: '/materials/tools-setup.pdf' }
        ]
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
        title: 'SQL注入攻防',
        description: '深入理解SQL注入漏洞原理和防御方法',
        duration: '4小时',
        difficulty: 'medium',
        isCompleted: true,
        isLocked: false,
        path: '/courses/sql-injection',
        objectives: [
          '理解SQL注入的原理',
          '掌握常见的注入技术',
          '学习有效的防御措施'
        ],
        materials: [
          {
            id: 'sql-1',
            type: 'video',
            title: 'SQL注入原理详解',
            description: '深入讲解SQL注入的原理和类型',
            url: '/materials/videos/sql-injection-theory.mp4',
            duration: '60分钟'
          },
          {
            id: 'sql-2',
            type: 'document',
            title: 'SQL注入防御指南',
            description: '全面的SQL注入防御策略和最佳实践',
            url: '/materials/docs/sql-injection-defense.pdf',
            pages: 35
          },
          {
            id: 'sql-3',
            type: 'lab',
            title: 'SQL注入实验环境',
            description: '动手实践SQL注入攻防',
            difficulty: 'medium',
            estimatedTime: '45分钟'
          },
          {
            id: 'sql-4',
            type: 'code',
            title: 'SQL注入防御代码',
            description: '各种编程语言的SQL注入防御代码示例',
            language: 'multiple',
            difficulty: 'medium'
          },
          {
            id: 'sql-5',
            type: 'quiz',
            title: 'SQL注入知识测试',
            description: '测试对SQL注入知识的掌握程度',
            questionCount: 15
          }
        ]
      },
      {
        id: 4,
        title: 'XSS跨站脚本攻防',
        description: '学习XSS漏洞的类型和防护方法',
        duration: '3小时',
        difficulty: 'medium',
        isCompleted: false,
        isLocked: false,
        path: '/courses/xss',
        objectives: [
          '理解XSS的不同类型',
          '掌握XSS攻击技术',
          '学习XSS防御方法'
        ],
        materials: [
          {
            id: 'xss-1',
            type: 'video',
            title: 'XSS攻击类型详解',
            description: '详细介绍各种XSS攻击类型',
            url: '/materials/videos/xss-types.mp4',
            duration: '55分钟'
          },
          {
            id: 'xss-2',
            type: 'document',
            title: 'XSS防御白皮书',
            description: '系统的XSS防御策略指南',
            url: '/materials/docs/xss-defense-whitepaper.pdf',
            pages: 42
          },
          {
            id: 'xss-3',
            type: 'lab',
            title: 'XSS攻防实验',
            description: '实践不同类型的XSS攻防',
            difficulty: 'medium',
            estimatedTime: '50分钟'
          },
          {
            id: 'xss-4',
            type: 'code',
            title: 'XSS过滤器实现',
            description: '实现一个基础的XSS过滤器',
            language: 'javascript',
            difficulty: 'medium'
          },
          {
            id: 'xss-5',
            type: 'quiz',
            title: 'XSS综合测试',
            description: '全面测试XSS相关知识',
            questionCount: 20
          }
        ]
      },
      {
        id: 5,
        title: 'CSRF攻防实战',
        description: '深入了解CSRF攻击原理和防御措施',
        duration: '3小时',
        difficulty: 'medium',
        isCompleted: false,
        isLocked: false,
        path: '/courses/csrf',
        objectives: [
          '理解CSRF攻击原理',
          '掌握CSRF利用方法',
          '学习有效防御措施'
        ],
        materials: [
          { type: 'video', title: 'CSRF攻击原理', url: '/materials/csrf-basics.mp4' },
          { type: 'document', title: 'CSRF防御指南', url: '/materials/csrf-defense.pdf' },
          { type: 'lab', title: 'CSRF实验', url: '/labs/csrf-lab' }
        ]
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
        path: '/courses/pentest-methodology',
        objectives: [
          '掌握渗透测试流程',
          '学习信息收集��术',
          '了解漏洞利用方法',
          '编写测试报告'
        ],
        materials: [
          { type: 'video', title: '渗透测试方法论', url: '/materials/pentest-methodology.mp4' },
          { type: 'document', title: '渗透测试手册', url: '/materials/pentest-manual.pdf' },
          { type: 'lab', title: '渗透测试实验', url: '/labs/pentest-lab' }
        ]
      },
      {
        id: 7,
        title: '高级漏洞挖掘',
        description: '复杂漏洞的发现与利用技术',
        duration: '8小时',
        difficulty: 'hard',
        isCompleted: false,
        isLocked: true,
        path: '/courses/advanced-exploitation',
        objectives: [
          '学习漏洞挖掘技术',
          '掌握高级利用方法',
          '了解漏洞分析流程'
        ],
        materials: [
          { type: 'video', title: '高级漏洞挖掘', url: '/materials/advanced-vuln.mp4' },
          { type: 'document', title: '漏洞分析指南', url: '/materials/vuln-analysis.pdf' },
          { type: 'lab', title: '漏洞挖掘实验', url: '/labs/vuln-lab' }
        ]
      },
      {
        id: 8,
        title: '安全开发实践',
        description: '安全编码和代码审计技术',
        duration: '6小时',
        difficulty: 'hard',
        isCompleted: false,
        isLocked: true,
        path: '/courses/secure-development',
        objectives: [
          '掌握安全编码规范',
          '学习代码审计技术',
          '了解安全开发流程'
        ],
        materials: [
          { type: 'video', title: '安全开发基础', url: '/materials/secure-dev.mp4' },
          { type: 'document', title: '代码审计指南', url: '/materials/code-audit.pdf' },
          { type: 'lab', title: '代码审计实验', url: '/labs/code-audit-lab' }
        ]
      }
    ]
  },
  {
    title: '实战演练',
    description: '综合性的安全实战训练',
    icon: OpportunityIcon,
    progress: 0,
    isCompleted: false,
    courses: [
      {
        id: 9,
        title: 'CTF实战训练',
        description: '通过CTF比赛提升实战能力',
        duration: '8小时',
        difficulty: 'hard',
        isCompleted: false,
        isLocked: true,
        path: '/courses/ctf-training',
        objectives: [
          '了解CTF比赛形式',
          '掌握解题技巧',
          '提升实战能力'
        ],
        materials: [
          { type: 'video', title: 'CTF入门指南', url: '/materials/ctf-guide.mp4' },
          { type: 'document', title: 'CTF题目合集', url: '/materials/ctf-challenges.pdf' },
          { type: 'lab', title: 'CTF训练环境', url: '/labs/ctf-lab' }
        ]
      },
      {
        id: 10,
        title: '应急响应演练',
        description: '网络安全事件应急处理',
        duration: '6小时',
        difficulty: 'hard',
        isCompleted: false,
        isLocked: true,
        path: '/courses/incident-response',
        objectives: [
          '掌握应急响应流程',
          '学习事件分析方法',
          '了解取证技术'
        ],
        materials: [
          { type: 'video', title: '应急响应基础', url: '/materials/incident-response.mp4' },
          { type: 'document', title: '应急手册', url: '/materials/incident-manual.pdf' },
          { type: 'lab', title: '应急响应实验', url: '/labs/incident-lab' }
        ]
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

const dialogVisible = ref(false)
const currentCourse = ref<any>(null)

// 处理课程点击
const handleCourseClick = (course: Course) => {
  if (course.isLocked) {
    ElMessage.warning('请先完成前置课程')
    return
  }
  currentCourse.value = course
  dialogVisible.value = true
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

// 打开学习材料
const openMaterial = (material: any) => {
  // 根据材料类型打开不同的查看器
  if (material.type === 'video') {
    window.open(material.url, '_blank')
  } else if (material.type === 'document') {
    window.open(material.url, '_blank')
  }
}

// 开始学习课程
const startLearning = (course: Course) => {
  dialogVisible.value = false
  router.push(`/learning-path/courses/${course.id}`)
}
</script>

<style lang="scss" scoped>
.learning-path {
  min-height: 100vh;
  position: relative;
  background: #1e1e2d;
  color: #e1e1e1;
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
  background: #2b2b3d;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);

  .path-title {
    font-size: 32px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 12px;
  }

  .path-description {
    font-size: 16px;
    color: #a1a1b5;
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
  background: #2b2b3d;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid #3f3f5f;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  }

  &.is-completed {
    border-left: 4px solid #409EFF;
    background: linear-gradient(to right, rgba(64, 158, 255, 0.1) 0%, #2b2b3d 8%);
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
  background: #252538;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #3f3f5f;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    background: #2f2f45;
  }

  &.is-completed {
    background: linear-gradient(to right, rgba(64, 158, 255, 0.1), #252538);
    border-color: #409EFF;
  }

  &.is-locked {
    opacity: 0.75;
    border-style: dashed;
    background: #252538;
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
      color: #a1a1b5;
      margin-bottom: 8px;
      line-height: 1.5;
    }

    .course-meta {
      display: flex;
      gap: 16px;
      font-size: 13px;
      color: #7171a6;
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
    background: #2b2b3d;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    border: 1px solid #3f3f5f;

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
    border-top: 1px solid #3f3f5f;

    .stat-item {
      display: flex;
      justify-content: space-between;
      margin-bottom: 12px;
      padding: 8px 12px;
      background: #252538;
      border-radius: 6px;

      .label {
        color: #a1a1b5;
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
      background: #252538;
      border-radius: 8px;
      transition: all 0.3s ease;

      &:hover {
        background: #2f2f45;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
      }

      .el-avatar {
        margin-right: 12px;
        border: 2px solid #3f3f5f;
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
          color: #a1a1b5;
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

.course-details {
  padding: 20px;
  background: #1e1e2d;

  h3 {
    font-size: 18px;
    color: #ffffff;
    margin-bottom: 16px;
    padding-left: 12px;
    border-left: 4px solid #409EFF;
  }

  .course-outline {
    margin-bottom: 30px;

    .el-collapse {
      border: none;
      background: transparent;
      
      :deep(.el-collapse-item__header) {
        font-size: 16px;
        color: #ffffff;
        font-weight: bold;
        background: #2b2b3d;
        border-bottom: 1px solid #3f3f5f;
      }

      :deep(.el-collapse-item__content) {
        padding: 16px;
        background: #252538;
        color: #a1a1b5;
      }
    }

    .course-section {
      padding: 8px 0;
      color: #a1a1b5;

      h4 {
        font-size: 14px;
        margin: 0;
        font-weight: normal;
      }
    }
  }

  .course-objectives,
  .course-prerequisites {
    margin-bottom: 30px;

    ul {
      list-style: none;
      padding: 0;
      margin: 0;

      li {
        position: relative;
        padding: 8px 0 8px 24px;
        color: #a1a1b5;

        &::before {
          content: '';
          position: absolute;
          left: 0;
          top: 16px;
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: #409EFF;
        }
      }
    }
  }
}

:deep(.el-dialog) {
  background: #1e1e2d;
  border-radius: 8px;
  
  .el-dialog__header {
    padding: 20px;
    margin: 0;
    border-bottom: 1px solid #3f3f5f;
    
    .el-dialog__title {
      font-size: 18px;
      font-weight: bold;
      color: #ffffff;
    }
  }

  .el-dialog__body {
    padding: 0;
    background: #1e1e2d;
  }

  .el-dialog__footer {
    padding: 16px 20px;
    border-top: 1px solid #3f3f5f;
    background: #1e1e2d;
  }
}
</style> 