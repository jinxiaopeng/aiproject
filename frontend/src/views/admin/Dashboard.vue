<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="24" class="statistics">
      <el-col :span="6">
        <el-card shadow="hover" class="statistic-card">
          <template #header>
            <div class="card-header">
              <span>总用户数</span>
              <el-tag type="success" effect="plain" size="small">+12%</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="number">1,234</div>
            <div class="icon">
              <el-icon><User /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover" class="statistic-card">
          <template #header>
            <div class="card-header">
              <span>课程总数</span>
              <el-tag type="warning" effect="plain" size="small">+5%</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="number">56</div>
            <div class="icon">
              <el-icon><Reading /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover" class="statistic-card">
          <template #header>
            <div class="card-header">
              <span>实验总数</span>
              <el-tag type="info" effect="plain" size="small">+8%</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="number">128</div>
            <div class="icon">
              <el-icon><Monitor /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card shadow="hover" class="statistic-card">
          <template #header>
            <div class="card-header">
              <span>今日活跃</span>
              <el-tag type="danger" effect="plain" size="small">+15%</el-tag>
            </div>
          </template>
          <div class="card-content">
            <div class="number">324</div>
            <div class="icon">
              <el-icon><TrendCharts /></el-icon>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="24" class="charts">
      <el-col :span="16">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>用户增长趋势</span>
              <el-radio-group v-model="timeRange" size="small">
                <el-radio-button label="week">本周</el-radio-button>
                <el-radio-button label="month">本月</el-radio-button>
                <el-radio-button label="year">全年</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div class="chart-container">
            <div ref="userGrowthChart" class="chart"></div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card shadow="hover" class="chart-card">
          <template #header>
            <div class="card-header">
              <span>课程分类分布</span>
            </div>
          </template>
          <div class="chart-container">
            <div ref="coursePieChart" class="chart"></div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最新动态 -->
    <el-row :gutter="24" class="activities">
      <el-col :span="12">
        <el-card shadow="hover" class="activity-card">
          <template #header>
            <div class="card-header">
              <span>最新用户</span>
              <el-button type="text">查看全部</el-button>
            </div>
          </template>
          <el-table :data="latestUsers" style="width: 100%" :show-header="false">
            <el-table-column width="50">
              <template #default="scope">
                <el-avatar :size="32" :src="scope.row.avatar">
                  {{ scope.row.username.charAt(0).toUpperCase() }}
                </el-avatar>
              </template>
            </el-table-column>
            <el-table-column prop="username" label="用户名">
              <template #default="scope">
                <div class="user-info">
                  <span class="username">{{ scope.row.username }}</span>
                  <span class="time">{{ scope.row.registerTime }}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column width="100" align="right">
              <template #default="scope">
                <el-tag size="small" :type="scope.row.status === '在线' ? 'success' : 'info'">
                  {{ scope.row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card shadow="hover" class="activity-card">
          <template #header>
            <div class="card-header">
              <span>系统日志</span>
              <el-button type="text">查看全部</el-button>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(log, index) in systemLogs"
              :key="index"
              :type="log.type"
              :timestamp="log.time"
              :size="'small'"
            >
              {{ log.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { User, Reading, Monitor, TrendCharts } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 时间范围选择
const timeRange = ref('week')

// 图表实例
let userGrowthChart: echarts.ECharts | null = null
let coursePieChart: echarts.ECharts | null = null

// 最新用户数据
const latestUsers = ref([
  {
    username: '张三',
    avatar: '',
    registerTime: '2024-01-20 14:23',
    status: '在线'
  },
  {
    username: '李四',
    avatar: '',
    registerTime: '2024-01-20 13:45',
    status: '离线'
  },
  {
    username: '王五',
    avatar: '',
    registerTime: '2024-01-20 12:30',
    status: '在线'
  },
  {
    username: '赵六',
    avatar: '',
    registerTime: '2024-01-20 11:15',
    status: '离线'
  }
])

// 系统日志数据
const systemLogs = ref([
  {
    content: '系统更新完成',
    time: '2024-01-20 14:23',
    type: 'success'
  },
  {
    content: '新用户注册: 张三',
    time: '2024-01-20 13:45',
    type: 'primary'
  },
  {
    content: '警告: 服务器负载过高',
    time: '2024-01-20 12:30',
    type: 'warning'
  },
  {
    content: '系统备份完成',
    time: '2024-01-20 11:15',
    type: 'info'
  }
])

// 初始化用户增长趋势图表
const initUserGrowthChart = () => {
  const chartDom = document.getElementById('userGrowthChart')
  if (!chartDom) return

  userGrowthChart = echarts.init(chartDom)
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '用户数',
        type: 'line',
        smooth: true,
        data: [120, 132, 101, 134, 90, 230, 210],
        areaStyle: {
          opacity: 0.1
        },
        lineStyle: {
          width: 3
        },
        itemStyle: {
          color: '#1890ff'
        }
      }
    ]
  }
  userGrowthChart.setOption(option)
}

// 初始化课程分类分布图表
const initCoursePieChart = () => {
  const chartDom = document.getElementById('coursePieChart')
  if (!chartDom) return

  coursePieChart = echarts.init(chartDom)
  const option = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '课程分类',
        type: 'pie',
        radius: '70%',
        data: [
          { value: 35, name: 'Web安全' },
          { value: 25, name: '系统安全' },
          { value: 20, name: '网络安全' },
          { value: 15, name: '移动安全' },
          { value: 5, name: '其他' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  coursePieChart.setOption(option)
}

// 监听窗口大小变化
const handleResize = () => {
  userGrowthChart?.resize()
  coursePieChart?.resize()
}

onMounted(() => {
  // 延迟一下初始化，确保DOM已经渲染
  setTimeout(() => {
    initUserGrowthChart()
    initCoursePieChart()
  }, 0)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  userGrowthChart?.dispose()
  coursePieChart?.dispose()
})
</script>

<style scoped>
.dashboard {
  padding: 24px;
}

/* 统计卡片样式 */
.statistics {
  margin-bottom: 24px;
}

.statistic-card {
  height: 180px;
  transition: all 0.3s;
}

.statistic-card:hover {
  transform: translateY(-4px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 500;
}

.card-content {
  position: relative;
  height: 100px;
  display: flex;
  align-items: center;
}

.number {
  font-size: 36px;
  font-weight: 600;
  color: #1a1a1a;
}

.icon {
  position: absolute;
  right: 0;
  bottom: 0;
  font-size: 64px;
  opacity: 0.1;
}

/* 图表卡片样式 */
.charts {
  margin-bottom: 24px;
}

.chart-card {
  margin-bottom: 24px;
}

.chart-container {
  height: 400px;
}

.chart {
  width: 100%;
  height: 100%;
}

/* 活动卡片样式 */
.activity-card {
  height: 400px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 14px;
  color: #1a1a1a;
}

.time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

/* Element Plus 样式覆盖 */
:deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-timeline-item__node) {
  background-color: transparent;
}

:deep(.el-timeline-item__wrapper) {
  padding-left: 24px;
}
</style> 