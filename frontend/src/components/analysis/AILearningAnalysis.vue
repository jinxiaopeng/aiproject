<template>
  <div class="ai-learning-analysis">
    <el-card class="analysis-card">
      <template #header>
        <div class="card-header">
          <h3>AI 学习分析</h3>
          <el-button type="primary" @click="refreshAnalysis" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新分析
          </el-button>
        </div>
      </template>

      <!-- 学习状态概览 -->
      <div class="analysis-overview">
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="metric-item">
              <h4>学习效率</h4>
              <el-progress
                type="dashboard"
                :percentage="metrics.efficiency"
                :color="getMetricColor(metrics.efficiency)"
              />
              <p class="metric-desc">{{ getEfficiencyDesc }}</p>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="metric-item">
              <h4>知识掌握</h4>
              <el-progress
                type="dashboard"
                :percentage="metrics.mastery"
                :color="getMetricColor(metrics.mastery)"
              />
              <p class="metric-desc">{{ getMasteryDesc }}</p>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="metric-item">
              <h4>学习投入</h4>
              <el-progress
                type="dashboard"
                :percentage="metrics.engagement"
                :color="getMetricColor(metrics.engagement)"
              />
              <p class="metric-desc">{{ getEngagementDesc }}</p>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- AI 建议 -->
      <div class="ai-suggestions">
        <h4>学习建议</h4>
        <el-timeline>
          <el-timeline-item
            v-for="suggestion in aiSuggestions"
            :key="suggestion.id"
            :type="suggestion.type"
            :color="suggestion.color"
            :timestamp="suggestion.timestamp"
            :hollow="suggestion.hollow"
          >
            <h5>{{ suggestion.title }}</h5>
            <p>{{ suggestion.content }}</p>
            <div class="suggestion-actions">
              <el-button 
                link 
                type="primary" 
                size="small"
                @click="showSuggestionDetail(suggestion)"
              >
                <el-icon><InfoFilled /></el-icon>
                查看详情
              </el-button>
            </div>
          </el-timeline-item>
        </el-timeline>
      </div>

      <!-- 建议详情对话框 -->
      <el-dialog
        v-model="detailDialogVisible"
        :title="selectedSuggestion?.title"
        width="600px"
        destroy-on-close
      >
        <div class="suggestion-detail" v-if="selectedSuggestion">
          <div class="detail-section">
            <h4>建议内容</h4>
            <p>{{ selectedSuggestion.content }}</p>
          </div>
          <div class="detail-section">
            <h4>具体行动建议</h4>
            <el-timeline>
              <el-timeline-item
                v-for="(action, index) in getDetailedActions(selectedSuggestion)"
                :key="index"
                :type="action.type"
              >
                <h5>{{ action.title }}</h5>
                <p>{{ action.content }}</p>
                <el-button 
                  v-if="action.link" 
                  type="primary" 
                  link
                  size="small"
                  @click="handleActionClick(action)"
                >
                  {{ action.linkText }}
                  <el-icon class="el-icon--right"><ArrowRight /></el-icon>
                </el-button>
              </el-timeline-item>
            </el-timeline>
          </div>
          <div class="detail-section">
            <h4>预期效果</h4>
            <el-card shadow="never" class="expected-results">
              <template #header>
                <div class="card-header">
                  <span>完成建议后的预期提升</span>
                </div>
              </template>
              <div class="results-list">
                <div class="result-item" v-for="(result, index) in getExpectedResults(selectedSuggestion)" :key="index">
                  <el-icon :class="result.type"><component :is="result.icon" /></el-icon>
                  <span>{{ result.content }}</span>
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </el-dialog>

      <!-- 技能雷达图 -->
      <div class="skill-analysis">
        <h4>技能分布</h4>
        <div ref="radarChartRef" class="radar-chart"></div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import { 
  Refresh, 
  InfoFilled, 
  ArrowRight,
  TrendCharts,
  Medal,
  Promotion
} from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

// 分析指标
const metrics = ref({
  efficiency: 75,
  mastery: 68,
  engagement: 82
})

// AI 建议
const aiSuggestions = ref([
  {
    id: 1,
    type: 'success',
    color: '#67C23A',
    hollow: true,
    timestamp: '今日',
    title: '学习方法建议',
    content: '你的学习效率较高，建议继续保持当前的学习节奏。可以尝试在完成课程后做知识总结，加深理解。'
  },
  {
    id: 2,
    type: 'warning',
    color: '#E6A23C',
    hollow: true,
    timestamp: '今日',
    title: '知识巩固建议',
    content: '在Web安全基础模块中，建议重点复习CSRF和XSS相关内容，这些是你的薄弱环节。'
  },
  {
    id: 3,
    type: 'info',
    color: '#909399',
    hollow: true,
    timestamp: '今日',
    title: '技能提升建议',
    content: '可以尝试参与更多实战练习，提高渗透测试的实践能力。推荐完成"Web漏洞挖掘"进阶课程。'
  }
])

// 加载状态
const loading = ref(false)

// 雷达图实例
let chartInstance: echarts.ECharts | null = null
const radarChartRef = ref<HTMLElement | null>(null)

// 计算属性：指标描述
const getEfficiencyDesc = computed(() => {
  const value = metrics.value.efficiency
  if (value >= 80) return '学习效率优秀，继续保持'
  if (value >= 60) return '学习效率良好，可以提升'
  return '学习效率有待提高'
})

const getMasteryDesc = computed(() => {
  const value = metrics.value.mastery
  if (value >= 80) return '知识掌握扎实，继续深入'
  if (value >= 60) return '知识掌握良好，需要巩固'
  return '知识掌握有待加强'
})

const getEngagementDesc = computed(() => {
  const value = metrics.value.engagement
  if (value >= 80) return '学习投入度高，状态优秀'
  if (value >= 60) return '学习投入度良好，可以加强'
  return '学习投入度需要提高'
})

// 获取指标颜色
const getMetricColor = (value: number) => {
  if (value >= 80) return '#67C23A'
  if (value >= 60) return '#E6A23C'
  return '#F56C6C'
}

// 刷新分析
const refreshAnalysis = async () => {
  loading.value = true
  try {
    // TODO: 调用后端API获取最新分析数据
    await new Promise(resolve => setTimeout(resolve, 1000))
    // 模拟更新数据
    metrics.value = {
      efficiency: Math.floor(Math.random() * 30) + 60,
      mastery: Math.floor(Math.random() * 30) + 60,
      engagement: Math.floor(Math.random() * 30) + 60
    }
    initRadarChart()
  } catch (error) {
    console.error('刷新分析失败:', error)
  } finally {
    loading.value = false
  }
}

// 初始化雷达图
const initRadarChart = () => {
  if (!radarChartRef.value) return

  chartInstance = echarts.init(radarChartRef.value)
  const option: EChartsOption = {
    tooltip: {
      trigger: 'item'
    },
    radar: {
      shape: 'circle',
      splitNumber: 4,
      axisName: {
        color: '#8892b0',
        fontSize: 12
      },
      splitArea: {
        areaStyle: {
          color: ['rgba(255, 255, 255, 0.05)', 'rgba(255, 255, 255, 0.1)']
        }
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(136, 146, 176, 0.3)'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(136, 146, 176, 0.3)'
        }
      },
      indicator: [
        { name: 'Web安全', max: 100 },
        { name: '系统安全', max: 100 },
        { name: '网络安全', max: 100 },
        { name: '密码学', max: 100 },
        { name: '安全开发', max: 100 }
      ]
    },
    series: [{
      name: '技能分布',
      type: 'radar',
      data: [{
        value: [80, 65, 70, 60, 75],
        name: '当前水平',
        symbolSize: 6,
        lineStyle: {
          width: 2,
          color: '#64ffda'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(100, 255, 218, 0.3)' },
            { offset: 1, color: 'rgba(100, 255, 218, 0.05)' }
          ])
        },
        label: {
          show: true,
          color: '#8892b0',
          formatter: '{c}%'
        }
      }]
    }]
  }
  chartInstance.setOption(option)
}

// 组件挂载时初始化
onMounted(() => {
  initRadarChart()
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    chartInstance?.resize()
  })
})

// 组件卸载时清理
onUnmounted(() => {
  window.removeEventListener('resize', () => {
    chartInstance?.resize()
  })
  chartInstance?.dispose()
})

// 建议详情相关
const detailDialogVisible = ref(false)
const selectedSuggestion = ref<any>(null)
const router = useRouter()

const showSuggestionDetail = (suggestion: any) => {
  selectedSuggestion.value = suggestion
  detailDialogVisible.value = true
}

const getDetailedActions = (suggestion: any) => {
  switch (suggestion.type) {
    case 'success':
      return [
        {
          type: 'success',
          title: '知识总结',
          content: '每完成一个章节后，使用思维导图或笔记形式总结关键知识点',
          link: false
        },
        {
          type: 'primary',
          title: '实验练习',
          content: '完成相关的实验来加深理解',
          link: true,
          linkText: '查看推荐实验',
          action: 'goToLabs',
          category: 'web-security',
          difficulty: 'beginner'
        }
      ]
    case 'warning':
      return [
        {
          type: 'warning',
          title: '知识巩固',
          content: '建议复习 XSS 和 CSRF 相关内容',
          link: true,
          linkText: '前往复习',
          action: 'goToCourse',
          courseType: 'web-security',
          keyword: 'XSS,CSRF',
          mode: 'review'
        },
        {
          type: 'primary',
          title: '能力测试',
          content: '完成一次 Web 安全基础测试',
          link: true,
          linkText: '开始测试',
          action: 'goToQuiz',
          quizType: 'web-security',
          category: 'basic'
        }
      ]
    case 'info':
      return [
        {
          type: 'primary',
          title: '进阶学习',
          content: '建议学习 Web 漏洞挖掘进阶课程',
          link: true,
          linkText: '查看课程',
          action: 'goToCourse',
          courseType: 'web-security',
          keyword: 'Web漏洞挖掘',
          mode: 'learn'
        },
        {
          type: 'success',
          title: '实战训练',
          content: '在靶场中实践所学知识',
          link: true,
          linkText: '进入靶场',
          action: 'goToLabs',
          category: 'web-security',
          difficulty: 'intermediate'
        }
      ]
    default:
      return []
  }
}

const getExpectedResults = (suggestion: any) => {
  // 根据建议类型返回不同的预期效果
  switch (suggestion.type) {
    case 'success':
      return [
        { type: 'primary', icon: 'TrendCharts', content: '知识掌握度提升 15%' },
        { type: 'success', icon: 'Medal', content: '获得知识总结达人徽章' }
      ]
    case 'warning':
      return [
        { type: 'warning', icon: 'TrendCharts', content: 'Web安全基础分数提升 20%' },
        { type: 'success', icon: 'Promotion', content: '解锁进阶课程学习资格' }
      ]
    case 'info':
      return [
        { type: 'primary', icon: 'TrendCharts', content: '渗透测试技能提升 25%' },
        { type: 'success', icon: 'Medal', content: '获得实战能手徽章' }
      ]
    default:
      return []
  }
}

const handleActionClick = (action: any) => {
  try {
    console.log('Action clicked:', action) // 添加日志
    switch (action.action) {
      case 'goToCourse':
        router.push({
          path: '/courses',
          query: { 
            type: action.courseType || 'all',
            keyword: action.keyword || '',
            mode: action.mode || 'learn'
          }
        })
        break
      case 'goToLabs':
        router.push({
          path: '/challenge',
          query: { 
            category: action.category || 'all',
            difficulty: action.difficulty || 'all'
          }
        })
        break
      default:
        console.warn('未知的行动类型:', action.action)
    }
    detailDialogVisible.value = false
  } catch (error) {
    console.error('导航失败:', error)
    ElMessage.error('导航失败，请稍后重试')
  }
}
</script>

<style lang="scss" scoped>
.ai-learning-analysis {
  .analysis-card {
    margin-bottom: 20px;
    background: var(--el-bg-color);
    border-radius: 8px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 20px;
    border-bottom: 1px solid var(--el-border-color-light);

    h3 {
      margin: 0;
      font-size: 18px;
      font-weight: 500;
      color: var(--el-text-color-primary);
    }

    .el-button {
      .el-icon {
        margin-right: 4px;
      }
    }
  }

  .analysis-overview {
    padding: 20px;
    margin-bottom: 30px;
    background: var(--el-bg-color-page);
    border-radius: 8px;

    .metric-item {
      text-align: center;
      padding: 20px;
      background: var(--el-bg-color);
      border-radius: 8px;
      box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
      }

      h4 {
        margin: 0 0 20px;
        font-size: 16px;
        color: var(--el-text-color-primary);
      }

      .el-progress {
        margin-bottom: 15px;
      }

      .metric-desc {
        margin: 10px 0 0;
        font-size: 14px;
        color: var(--el-text-color-secondary);
        min-height: 40px;
      }
    }
  }

  .ai-suggestions {
    padding: 0 20px 20px;

    h4 {
      margin: 0 0 20px;
      font-size: 16px;
      color: var(--el-text-color-primary);
    }

    .el-timeline-item {
      padding-bottom: 20px;

      h5 {
        margin: 0 0 8px;
        font-size: 15px;
        color: var(--el-text-color-primary);
      }

      p {
        margin: 0;
        font-size: 14px;
        color: var(--el-text-color-secondary);
        line-height: 1.6;
      }
    }
  }

  .skill-analysis {
    padding: 0 20px 20px;

    h4 {
      margin: 0 0 20px;
      font-size: 16px;
      color: var(--el-text-color-primary);
    }

    .radar-chart {
      height: 300px;
      background: var(--el-bg-color);
      border-radius: 8px;
      padding: 20px;
    }
  }
}

@media (max-width: 768px) {
  .ai-learning-analysis {
    .analysis-overview {
      .el-row {
        margin-bottom: -20px;
      }
      .el-col {
        margin-bottom: 20px;
      }
    }
  }
}

.suggestion-actions {
  margin-top: 8px;
  display: flex;
  justify-content: flex-end;
}

.suggestion-detail {
  .detail-section {
    margin-bottom: 24px;

    &:last-child {
      margin-bottom: 0;
    }

    h4 {
      margin: 0 0 16px;
      font-size: 16px;
      color: var(--el-text-color-primary);
      font-weight: 500;
    }

    p {
      margin: 0;
      font-size: 14px;
      color: var(--el-text-color-regular);
      line-height: 1.6;
    }
  }

  .expected-results {
    .card-header {
      font-size: 14px;
      color: var(--el-text-color-secondary);
    }

    .results-list {
      display: flex;
      flex-direction: column;
      gap: 12px;

      .result-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;

        .el-icon {
          font-size: 18px;

          &.primary {
            color: var(--el-color-primary);
          }

          &.success {
            color: var(--el-color-success);
          }

          &.warning {
            color: var(--el-color-warning);
          }
        }
      }
    }
  }
}
</style> 