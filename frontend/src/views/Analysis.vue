<template>
  <div class="analysis">
    <el-row :gutter="20">
      <!-- 学习概览 -->
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>学习概览</span>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="stat-card">
                <h3>总学习时长</h3>
                <p>{{ totalTime }} 小时</p>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <h3>完成课程</h3>
                <p>{{ completedCourses }} / {{ totalCourses }}</p>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <h3>靶场通过</h3>
                <p>{{ passedLabs }} / {{ totalLabs }}</p>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <h3>技能评分</h3>
                <p>{{ skillScore }} 分</p>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>

      <!-- 技能雷达图 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>技能分布</span>
            </div>
          </template>
          <div class="chart-container">
            <radar-chart :data="skillData" />
          </div>
        </el-card>
      </el-col>

      <!-- 学习进度趋势 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>学习进度趋势</span>
            </div>
          </template>
          <div class="chart-container">
            <line-chart :data="progressData" />
          </div>
        </el-card>
      </el-col>

      <!-- AI建议 -->
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>AI学习建议</span>
            </div>
          </template>
          <div class="ai-suggestions">
            <el-timeline>
              <el-timeline-item
                v-for="(suggestion, index) in aiSuggestions"
                :key="index"
                :type="suggestion.type"
              >
                {{ suggestion.content }}
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue'
import RadarChart from '../components/charts/RadarChart.vue'
import LineChart from '../components/charts/LineChart.vue'

export default defineComponent({
  name: 'Analysis',
  components: {
    RadarChart,
    LineChart
  },
  setup() {
    const totalTime = ref(0)
    const completedCourses = ref(0)
    const totalCourses = ref(0)
    const passedLabs = ref(0)
    const totalLabs = ref(0)
    const skillScore = ref(0)

    const skillData = ref({
      labels: ['Web安全', 'SQL注入', 'XSS', '权限提升', '代码审计'],
      datasets: [{
        data: [80, 70, 90, 60, 75]
      }]
    })

    const progressData = ref({
      labels: ['1月', '2月', '3月', '4月', '5月'],
      datasets: [{
        label: '学习进度',
        data: [30, 45, 60, 75, 85]
      }]
    })

    const aiSuggestions = ref([
      {
        type: 'primary',
        content: '建议加强SQL注入的练习，当前掌握度较低'
      },
      {
        type: 'success',
        content: 'XSS攻防能力表现优秀，可以尝试更高难度的挑战'
      },
      {
        type: 'warning',
        content: '权限提升部分需要更多实战演练'
      }
    ])

    onMounted(async () => {
      // 获取分析数据
      await fetchAnalysisData()
    })

    const fetchAnalysisData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/analysis')
        const data = await response.json()
        // 更新数据
        totalTime.value = data.totalTime
        completedCourses.value = data.completedCourses
        totalCourses.value = data.totalCourses
        passedLabs.value = data.passedLabs
        totalLabs.value = data.totalLabs
        skillScore.value = data.skillScore
      } catch (error) {
        console.error('获取分析数据失败:', error)
      }
    }

    return {
      totalTime,
      completedCourses,
      totalCourses,
      passedLabs,
      totalLabs,
      skillScore,
      skillData,
      progressData,
      aiSuggestions
    }
  }
})
</script>

<style scoped>
.analysis {
  padding: 20px;
}
.stat-card {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 4px;
}
.chart-container {
  height: 300px;
}
.ai-suggestions {
  padding: 20px;
}
</style> 