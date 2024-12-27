<template>
  <div class="career-path-planner">
    <div class="planner-header">
      <h3>职业路径规划</h3>
      <p>输入目标职业，获取推荐的学习路径</p>
    </div>

    <div class="input-section">
      <el-input
        v-model="careerInput"
        placeholder="输入目标职业（如：渗透测试工程师）"
        clearable
        @keyup.enter="generatePath"
      >
        <template #append>
          <el-button @click="generatePath" :loading="loading">
            生成路径
          </el-button>
        </template>
      </el-input>
    </div>

    <!-- 预设职业选项 -->
    <div class="preset-careers">
      <el-tag
        v-for="career in presetCareers"
        :key="career"
        class="preset-tag"
        @click="selectPreset(career)"
      >
        {{ career }}
      </el-tag>
    </div>

    <!-- 学习路径展示 -->
    <div v-if="learningPath.length" class="path-display">
      <div class="path-header">
        <h4>推荐学习路径</h4>
        <div class="path-info">
          <el-tag size="small" type="info">预计学习时长: {{ estimatedTime }}</el-tag>
          <el-tag size="small" type="warning">难度: {{ pathDifficulty }}</el-tag>
        </div>
      </div>

      <el-timeline>
        <el-timeline-item
          v-for="(stage, index) in learningPath"
          :key="index"
          :type="getTimelineItemType(stage.difficulty)"
          :color="getTimelineItemColor(stage.difficulty)"
        >
          <div class="timeline-content">
            <h5>{{ stage.name }}</h5>
            <p class="stage-description">{{ stage.description }}</p>
            <div class="stage-tags">
              <el-tag size="small" type="info">{{ stage.difficulty }}</el-tag>
              <el-tag 
                size="small" 
                v-for="tag in stage.tags" 
                :key="tag"
                class="stage-tag"
              >
                {{ tag }}
              </el-tag>
            </div>
            <div class="key-points" v-if="stage.keyPoints?.length">
              <p class="key-points-title">关键知识点：</p>
              <ul>
                <li v-for="point in stage.keyPoints" :key="point">{{ point }}</li>
              </ul>
            </div>
          </div>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { CareerPathStage } from '../types/career'
import { generateCareerPath } from '../services/careerPath'
import { ElMessage } from 'element-plus'

const careerInput = ref('')
const loading = ref(false)
const learningPath = ref<CareerPathStage[]>([])
const estimatedTime = ref('6-8个月')
const pathDifficulty = ref('中等')

// 预设职业选项
const presetCareers = [
  '渗透测试工程师',
  '安全开发工程师',
  '安全运维工程师',
  '安全研究员',
  '应急响应工程师'
]

// 选择预设职业
const selectPreset = (career: string) => {
  careerInput.value = career
  generatePath()
}

// 生成学习路径
const generatePath = async () => {
  if (!careerInput.value) {
    ElMessage.warning('请输入目标职业')
    return
  }
  
  loading.value = true
  try {
    const result = await generateCareerPath(careerInput.value)
    learningPath.value = result.path
    estimatedTime.value = result.estimatedTime
    pathDifficulty.value = result.difficulty
    ElMessage.success('学习路径生成成功')
  } catch (error) {
    console.error('生成路径失败:', error)
    ElMessage.error(error instanceof Error ? error.message : '生成路径失败，请稍后重试')
    learningPath.value = []
  } finally {
    loading.value = false
  }
}

// 获取时间线项的类型
const getTimelineItemType = (difficulty: string) => {
  switch (difficulty.toLowerCase()) {
    case '入门': return 'primary'
    case '基础': return 'success'
    case '进阶': return 'warning'
    case '高级': return 'danger'
    default: return 'info'
  }
}

// 获取时间线项的颜色
const getTimelineItemColor = (difficulty: string) => {
  switch (difficulty.toLowerCase()) {
    case '入门': return '#409EFF'
    case '基础': return '#67C23A'
    case '进阶': return '#E6A23C'
    case '高级': return '#F56C6C'
    default: return '#909399'
  }
}
</script>

<style scoped>
.career-path-planner {
  padding: 20px;
  background: var(--el-bg-color);
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.planner-header {
  margin-bottom: 20px;
}

.planner-header h3 {
  margin: 0;
  font-size: 24px;
  color: var(--el-text-color-primary);
}

.planner-header p {
  margin: 8px 0 0;
  color: var(--el-text-color-secondary);
}

.input-section {
  margin-bottom: 16px;
}

.preset-careers {
  margin-bottom: 24px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.preset-tag {
  cursor: pointer;
  transition: all 0.3s;
}

.preset-tag:hover {
  transform: translateY(-2px);
}

.path-display {
  margin-top: 24px;
}

.path-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.path-header h4 {
  margin: 0;
  font-size: 18px;
  color: var(--el-text-color-primary);
}

.path-info {
  display: flex;
  gap: 8px;
}

.timeline-content {
  padding: 12px;
  background: var(--el-bg-color-page);
  border-radius: 4px;
  border: 1px solid var(--el-border-color-light);
}

.timeline-content h5 {
  margin: 0 0 8px;
  font-size: 16px;
  color: var(--el-text-color-primary);
}

.stage-description {
  margin: 8px 0;
  color: var(--el-text-color-regular);
  font-size: 14px;
}

.stage-tags {
  margin: 8px 0;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.stage-tag {
  background-color: var(--el-color-info-light-9);
}

.key-points {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--el-border-color-lighter);
}

.key-points-title {
  margin: 0 0 8px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.key-points ul {
  margin: 0;
  padding-left: 20px;
  color: var(--el-text-color-regular);
}

.key-points li {
  margin: 4px 0;
}
</style> 