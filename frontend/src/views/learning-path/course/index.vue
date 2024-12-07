<template>
  <div class="course-detail">
    <DynamicBackground />
    
    <div class="course-container">
      <div class="course-header">
        <div class="header-content">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/learning-path' }">学路径</el-breadcrumb-item>
            <el-breadcrumb-item>{{ courseData.title }}</el-breadcrumb-item>
          </el-breadcrumb>
          
          <h1 class="course-title">{{ courseData.title }}</h1>
          <p class="course-desc">{{ courseData.description }}</p>
          
          <div class="course-meta">
            <span class="meta-item">
              <el-icon><Timer /></el-icon>
              {{ courseData.duration }}
            </span>
            <span class="meta-item">
              <el-icon><Connection /></el-icon>
              {{ difficultyText[courseData.difficulty] }}
            </span>
            <span v-if="isReviewMode" class="meta-item review-badge">
              <el-icon><Refresh /></el-icon>
              复习模式
            </span>
          </div>
        </div>
      </div>

      <div class="course-content">
        <el-row :gutter="24">
          <el-col :span="18">
            <div class="content-section">
              <div class="section-header">
                <h2>课程内容</h2>
              </div>
              
              <div class="section-content">
                <div v-for="(section, index) in courseData.sections" 
                     :key="index"
                     class="course-section"
                >
                  <div class="section-title">
                    <span class="section-number">{{ index + 1 }}</span>
                    <h3>{{ section.title }}</h3>
                  </div>
                  
                  <div class="section-desc">{{ section.description }}</div>
                  
                  <div class="section-materials">
                    <div v-for="(material, mIndex) in section.materials"
                         :key="mIndex"
                         class="material-item"
                    >
                      <el-icon><Document /></el-icon>
                      <span>{{ material.title }}</span>
                      <el-button 
                        link 
                        type="primary" 
                        @click="openMaterial(material)"
                      >
                        查看
                      </el-button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="content-section">
              <div class="section-header">
                <h2>实验环境</h2>
              </div>
              
              <div class="section-content">
                <div class="lab-environment">
                  <div class="lab-info">
                    <h3>{{ courseData.lab.title }}</h3>
                    <p>{{ courseData.lab.description }}</p>
                  </div>
                  
                  <div class="lab-actions">
                    <el-button 
                      type="primary" 
                      :icon="Setting"
                      @click="startLab"
                    >
                      启动实验环境
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </el-col>

          <el-col :span="6">
            <div class="content-section">
              <div class="section-header">
                <h2>学习进度</h2>
              </div>
              
              <div class="progress-content">
                <el-progress 
                  type="circle"
                  :percentage="courseProgress"
                  :stroke-width="6"
                  :width="120"
                />
                
                <div class="progress-stats">
                  <div class="stat-item">
                    <span class="label">已完成章节</span>
                    <span class="value">{{ completedSections }}/{{ totalSections }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="label">实验进度</span>
                    <span class="value">{{ labProgress }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="content-section">
              <div class="section-header">
                <h2>学习目标</h2>
              </div>
              
              <div class="objectives-content">
                <el-checkbox-group v-model="completedObjectives">
                  <div v-for="(objective, index) in courseData.objectives"
                       :key="index"
                       class="objective-item"
                  >
                    <el-checkbox :label="index">{{ objective }}</el-checkbox>
                  </div>
                </el-checkbox-group>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DynamicBackground from '@/components/DynamicBackground.vue'
import { 
  Timer,
  Connection,
  Document,
  Setting,
  Refresh
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

// 判断是否为复习模式
const isReviewMode = computed(() => route.query.mode === 'review')

// 难度文本映射
const difficultyText = {
  easy: '入门',
  medium: '进阶',
  hard: '高级'
}

// 模拟课程数据
const courseData = ref({
  id: 1,
  title: 'Web安全基础入门',
  description: '了解Web安全的基本概念，掌握常见的Web安全威胁和防护方法。',
  duration: '2小时',
  difficulty: 'easy',
  sections: [
    {
      title: 'Web安全概述',
      description: '介绍Web安全的重要性和基本概念',
      materials: [
        { title: 'Web安全基础概念', type: 'video', url: '/materials/web-security-basics.mp4' },
        { title: 'Web安全发展历程', type: 'document', url: '/materials/security-history.pdf' }
      ]
    },
    {
      title: '常见Web安全威胁',
      description: '了解主要的Web安全威胁类型',
      materials: [
        { title: '常见攻击方式分析', type: 'video', url: '/materials/common-attacks.mp4' },
        { title: '案例分析报告', type: 'document', url: '/materials/case-study.pdf' }
      ]
    }
  ],
  lab: {
    title: 'Web安全基础实验环境',
    description: '通过实际操作了解基本的Web安全概念和工具使用方法',
    status: 'ready'
  },
  objectives: [
    '理解Web安全的基本概念和重要性',
    '掌握常见的Web安全威胁类型',
    '学会使用基本的Web安全测试工具',
    '了解基本的安全防护措施'
  ]
})

// 进度相关
const completedSections = ref(0)
const totalSections = computed(() => courseData.value.sections.length)
const labProgress = ref(0)
const completedObjectives = ref<number[]>([])

const courseProgress = computed(() => {
  const totalItems = totalSections.value + 1 // sections + lab
  const completed = completedSections.value + (labProgress.value === 100 ? 1 : 0)
  return Math.round((completed / totalItems) * 100)
})

// 处理学习材料
const openMaterial = (material: any) => {
  // 这里应该根据material.type来决定如何打开材料
  // 可以是打开视频播放器、PDF查看器等
  ElMessage.success(`正在打开: ${material.title}`)
}

// 处理实验环境
const startLab = () => {
  ElMessage.success('正在启动实验环境，请稍候...')
  // 这里应该调用后端API来启动实验环境
}

// 加载课程数据
const loadCourseData = async () => {
  try {
    // 这里应该从API获取课程数据
    // const response = await getCourseDetail(route.params.id)
    // courseData.value = response.data
    
    // 加载进度
    const progress = localStorage.getItem(`course-${courseData.value.id}-progress`)
    if (progress) {
      const savedProgress = JSON.parse(progress)
      completedSections.value = savedProgress.completedSections
      labProgress.value = savedProgress.labProgress
      completedObjectives.value = savedProgress.completedObjectives
    }
  } catch (error) {
    ElMessage.error('加载课程数据失败')
  }
}

// 保存进度
const saveProgress = () => {
  const progress = {
    completedSections: completedSections.value,
    labProgress: labProgress.value,
    completedObjectives: completedObjectives.value
  }
  localStorage.setItem(`course-${courseData.value.id}-progress`, JSON.stringify(progress))
}

// 初始化
onMounted(() => {
  loadCourseData()
})
</script>

<style lang="scss" scoped>
.course-detail {
  min-height: 100vh;
  position: relative;
}

.course-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.course-header {
  margin-bottom: 32px;
  padding: 40px;
  background: rgba(42, 60, 84, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);

  .header-content {
    max-width: 800px;
    margin: 0 auto;
  }

  .course-title {
    font-size: 32px;
    font-weight: bold;
    color: #ffffff;
    margin: 20px 0 12px;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
  }

  .course-desc {
    font-size: 16px;
    color: rgba(255, 255, 255, 0.8);
    margin-bottom: 20px;
    line-height: 1.6;
  }

  .course-meta {
    display: flex;
    gap: 24px;
    
    .meta-item {
      display: flex;
      align-items: center;
      gap: 8px;
      color: rgba(255, 255, 255, 0.8);
      font-size: 14px;

      .el-icon {
        color: #409EFF;
      }
    }

    .review-badge {
      background: rgba(64, 158, 255, 0.2);
      padding: 4px 12px;
      border-radius: 12px;
      border: 1px solid #409EFF;
    }
  }
}

.content-section {
  background: rgba(42, 60, 84, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;

  .section-header {
    padding: 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);

    h2 {
      font-size: 18px;
      font-weight: bold;
      color: #ffffff;
      margin: 0;
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

  .section-content {
    padding: 20px;
  }
}

.course-section {
  padding: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  margin-bottom: 16px;

  &:last-child {
    margin-bottom: 0;
  }

  .section-title {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;

    .section-number {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background: #409EFF;
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      font-weight: bold;
    }

    h3 {
      font-size: 16px;
      font-weight: bold;
      color: #ffffff;
      margin: 0;
    }
  }

  .section-desc {
    color: rgba(255, 255, 255, 0.8);
    font-size: 14px;
    margin-bottom: 16px;
    padding-left: 36px;
  }
}

.material-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  margin-bottom: 8px;
  margin-left: 36px;

  &:last-child {
    margin-bottom: 0;
  }

  .el-icon {
    color: #409EFF;
  }

  span {
    flex: 1;
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
  }
}

.lab-environment {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;

  .lab-info {
    margin-bottom: 20px;

    h3 {
      font-size: 16px;
      font-weight: bold;
      color: #ffffff;
      margin-bottom: 8px;
    }

    p {
      color: rgba(255, 255, 255, 0.8);
      font-size: 14px;
      line-height: 1.6;
    }
  }
}

.progress-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;

  .progress-stats {
    margin-top: 24px;
    width: 100%;

    .stat-item {
      display: flex;
      justify-content: space-between;
      margin-bottom: 12px;
      padding: 8px 12px;
      background: rgba(255, 255, 255, 0.05);
      border-radius: 6px;

      .label {
        color: rgba(255, 255, 255, 0.8);
      }

      .value {
        color: #409EFF;
        font-weight: bold;
      }
    }
  }
}

.objectives-content {
  padding: 20px;

  .objective-item {
    margin-bottom: 12px;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

:deep(.el-breadcrumb) {
  color: rgba(255, 255, 255, 0.8);

  .el-breadcrumb__item {
    .el-breadcrumb__inner {
      color: rgba(255, 255, 255, 0.8);
      
      &:hover {
        color: #409EFF;
      }
    }

    &:last-child {
      .el-breadcrumb__inner {
        color: #ffffff;
      }
    }
  }
}

:deep(.el-checkbox) {
  --el-checkbox-checked-bg-color: #409EFF;
  --el-checkbox-checked-input-border-color: #409EFF;
  --el-checkbox-checked-text-color: rgba(255, 255, 255, 0.9);
  --el-checkbox-text-color: rgba(255, 255, 255, 0.9);
  --el-checkbox-input-border-color: rgba(255, 255, 255, 0.3);

  .el-checkbox__label {
    color: rgba(255, 255, 255, 0.9);
  }
}

@media screen and (max-width: 768px) {
  .course-header {
    padding: 24px;

    .course-title {
      font-size: 24px;
    }

    .course-meta {
      flex-wrap: wrap;
      gap: 16px;
    }
  }

  .el-col-18 {
    width: 100%;
  }

  .el-col-6 {
    width: 100%;
  }
}
</style> 