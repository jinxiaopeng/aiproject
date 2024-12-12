<template>
  <div class="practice-stats">
    <div class="header">
      <h1>训练统计</h1>
      <p>查看你的训练进度和成果</p>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="stats-header">
              <el-icon><Timer /></el-icon>
              <span>总训练时长</span>
            </div>
          </template>
          <div class="stats-content">
            <span class="stats-value">{{ userStats.totalHours || 0 }}</span>
            <span class="stats-label">小时</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="stats-header">
              <el-icon><Flag /></el-icon>
              <span>完成靶场</span>
            </div>
          </template>
          <div class="stats-content">
            <span class="stats-value">{{ userStats.completedCount || 0 }}</span>
            <span class="stats-label">个</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="stats-header">
              <el-icon><Trophy /></el-icon>
              <span>获得积分</span>
            </div>
          </template>
          <div class="stats-content">
            <span class="stats-value">{{ userStats.points || 0 }}</span>
            <span class="stats-label">分</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="stats-header">
              <el-icon><Rank /></el-icon>
              <span>当前排名</span>
            </div>
          </template>
          <div class="stats-content">
            <span class="stats-value">#{{ userStats.rank || '-' }}</span>
            <span class="stats-label">名</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" class="charts-row">
      <!-- 技能雷达图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <h3>技能分布</h3>
            </div>
          </template>
          <div class="chart-content">
            <div ref="skillRadarRef" class="chart"></div>
          </div>
        </el-card>
      </el-col>

      <!-- 训练趋势图 -->
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <h3>训练趋势</h3>
            </div>
          </template>
          <div class="chart-content">
            <div ref="trendLineRef" class="chart"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 训练记录表格 -->
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <h3>训练记录</h3>
          <el-button type="primary" @click="handleExport">导出记录</el-button>
        </div>
      </template>
      <el-table
        :data="trainingRecords"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="labName" label="靶场名称" />
        <el-table-column prop="startTime" label="开始时间">
          <template #default="scope">
            {{ formatDate(scope.row.startTime) }}
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="训练时长">
          <template #default="scope">
            {{ formatDuration(scope.row.duration) }}
          </template>
        </el-table-column>
        <el-table-column prop="score" label="得分" width="100">
          <template #default="scope">
            <span class="score">{{ scope.row.score }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Timer, Flag, Trophy, Rank } from '@element-plus/icons-vue'
import { labApi } from '@/api'
import { formatDate, formatDuration } from '@/utils/date'
import * as echarts from 'echarts'

// 状态变量
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const skillRadarRef = ref()
const trendLineRef = ref()

// 用户统计数据
const userStats = ref({
  totalHours: 0,
  completedCount: 0,
  points: 0,
  rank: '-'
})

// 训练记录数据
const trainingRecords = ref([])

// 获取用户统计数据
const getUserStats = async () => {
  try {
    const response = await labApi.getUserStats()
    userStats.value = response.data
  } catch (error) {
    ElMessage.error('获取统计数据失败')
  }
}

// 获取训练记录
const getTrainingRecords = async () => {
  loading.value = true
  try {
    const response = await labApi.getTrainingRecords({
      page: currentPage.value,
      pageSize: pageSize.value
    })
    trainingRecords.value = response.data.records
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('获取训练记录失败')
  } finally {
    loading.value = false
  }
}

// 初始化技能雷达图
const initSkillRadar = async () => {
  try {
    const response = await labApi.getSkillRadar()
    const chart = echarts.init(skillRadarRef.value)
    
    const option = {
      radar: {
        indicator: [
          { name: 'Web安全', max: 100 },
          { name: '系统安全', max: 100 },
          { name: '网络安全', max: 100 },
          { name: '密码学', max: 100 },
          { name: '逆向工程', max: 100 }
        ]
      },
      series: [{
        type: 'radar',
        data: [{
          value: response.data,
          name: '技能分布',
          areaStyle: {
            color: 'rgba(64, 158, 255, 0.2)'
          },
          lineStyle: {
            color: '#409EFF'
          }
        }]
      }]
    }
    
    chart.setOption(option)
  } catch (error) {
    console.error('初始化技能雷达图失败:', error)
  }
}

// 初始化训练趋势图
const initTrendLine = async () => {
  try {
    const response = await labApi.getProgressTrend()
    const chart = echarts.init(trendLineRef.value)
    
    const option = {
      xAxis: {
        type: 'category',
        data: response.data.dates
      },
      yAxis: {
        type: 'value'
      },
      series: [{
        data: response.data.counts,
        type: 'line',
        smooth: true,
        areaStyle: {
          color: 'rgba(64, 158, 255, 0.2)'
        },
        lineStyle: {
          color: '#409EFF'
        }
      }]
    }
    
    chart.setOption(option)
  } catch (error) {
    console.error('初始化训练趋势图失败:', error)
  }
}

// 导出训练记录
const handleExport = async () => {
  try {
    const response = await labApi.exportTrainingRecords()
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', '训练记录.xlsx')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

// 获取状态标签类型
const getStatusType = (status: string) => {
  const types = {
    completed: 'success',
    running: 'warning',
    stopped: 'info',
    error: 'danger'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string) => {
  const texts = {
    completed: '已完成',
    running: '进行中',
    stopped: '已停止',
    error: '错误'
  }
  return texts[status] || status
}

// 处理分页
const handleSizeChange = (val: number) => {
  pageSize.value = val
  getTrainingRecords()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  getTrainingRecords()
}

// 页面加载时初始化数据
onMounted(() => {
  getUserStats()
  getTrainingRecords()
  initSkillRadar()
  initTrendLine()
})
</script>

<style scoped>
.practice-stats {
  padding: 20px;
}

.header {
  margin-bottom: 24px;
}

.header h1 {
  margin: 0;
  font-size: 24px;
  color: var(--el-text-color-primary);
}

.header p {
  margin: 8px 0 0;
  color: var(--el-text-color-secondary);
}

.stats-row {
  margin-bottom: 24px;
}

.stats-card {
  height: 100%;
}

.stats-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stats-content {
  text-align: center;
}

.stats-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.stats-label {
  margin-left: 4px;
  color: var(--el-text-color-secondary);
}

.charts-row {
  margin-bottom: 24px;
}

.chart-card {
  height: 100%;
}

.chart {
  height: 300px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
}

.table-card {
  margin-bottom: 24px;
}

.score {
  font-weight: bold;
  color: var(--el-color-success);
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>