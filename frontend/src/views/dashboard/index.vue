<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 学习进度 -->
      <el-col :span="8">
        <el-card class="progress-card">
          <template #header>
            <div class="card-header">
              <span>学习进度</span>
            </div>
          </template>
          <el-progress
            type="circle"
            :percentage="learningProgress"
            :stroke-width="10"
            :width="150"
          >
            <template #default="{ percentage }">
              <span class="progress-value">{{ percentage }}%</span>
              <span class="progress-label">完成进度</span>
            </template>
          </el-progress>
        </el-card>
      </el-col>

      <!-- 最近活动 -->
      <el-col :span="8">
        <el-card class="activity-card">
          <template #header>
            <div class="card-header">
              <span>最近活动</span>
            </div>
          </template>
          <el-timeline>
            <el-timeline-item
              v-for="(activity, index) in recentActivities"
              :key="index"
              :timestamp="activity.time"
              :type="activity.type"
            >
              {{ activity.content }}
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>

      <!-- 技能雷达 -->
      <el-col :span="8">
        <el-card class="skills-card">
          <template #header>
            <div class="card-header">
              <span>技能分布</span>
            </div>
          </template>
          <div class="radar-chart" ref="radarChart"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 课程进度 -->
    <el-row :gutter="20" class="course-progress">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>课程进度</span>
            </div>
          </template>
          <el-table :data="courseProgress" style="width: 100%">
            <el-table-column prop="name" label="课程名称" />
            <el-table-column prop="progress" label="进度" width="200">
              <template #default="{ row }">
                <el-progress :percentage="row.progress" />
              </template>
            </el-table-column>
            <el-table-column prop="lastStudy" label="最后学习时间" width="200" />
            <el-table-column label="操作" width="150">
              <template #default="{ row }">
                <el-button type="primary" link @click="continueLearning(row.id)">
                  继续学习
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const router = useRouter()
const radarChart = ref<HTMLElement | null>(null)

// 模拟数据
const learningProgress = ref(68)
const recentActivities = ref([
  {
    content: '完成了"SQL注入基础"课程',
    time: '2024-01-10 14:30',
    type: 'success'
  },
  {
    content: '开始学习"XSS攻击防御"',
    time: '2024-01-09 16:20',
    type: 'primary'
  },
  {
    content: '提交了实验报告',
    time: '2024-01-08 10:45',
    type: 'info'
  }
])

const courseProgress = ref([
  {
    id: 1,
    name: 'Web安全基础',
    progress: 100,
    lastStudy: '2024-01-10 14:30'
  },
  {
    id: 2,
    name: 'XSS攻击防御',
    progress: 45,
    lastStudy: '2024-01-09 16:20'
  },
  {
    id: 3,
    name: '密码学基础',
    progress: 0,
    lastStudy: '-'
  }
])

// 初始化雷达图
const initRadarChart = () => {
  if (!radarChart.value) return

  const chart = echarts.init(radarChart.value)
  const option = {
    radar: {
      indicator: [
        { name: 'Web安全', max: 100 },
        { name: '密码学', max: 100 },
        { name: '网络安全', max: 100 },
        { name: '系统安全', max: 100 },
        { name: '安全开发', max: 100 }
      ],
      splitArea: {
        areaStyle: {
          color: ['rgba(255, 255, 255, 0.05)']
        }
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.2)'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      }
    },
    series: [{
      type: 'radar',
      data: [{
        value: [80, 60, 70, 50, 65],
        name: '技能分布',
        areaStyle: {
          color: 'rgba(64, 158, 255, 0.2)'
        },
        lineStyle: {
          color: '#409EFF'
        },
        itemStyle: {
          color: '#409EFF'
        }
      }]
    }]
  }
  chart.setOption(option)

  // 监听窗口大小变化
  window.addEventListener('resize', () => chart.resize())
}

// 继续学习
const continueLearning = (courseId: number) => {
  router.push(`/courses/${courseId}`)
}

onMounted(() => {
  initRadarChart()
})
</script>

<style lang="scss" scoped>
.dashboard {
  padding: 20px;
}

.el-row {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  span {
    font-size: 16px;
    font-weight: 500;
    color: #fff;
  }
}

.progress-card {
  text-align: center;
  
  .progress-value {
    display: block;
    font-size: 28px;
    font-weight: bold;
    color: #409EFF;
  }
  
  .progress-label {
    display: block;
    font-size: 14px;
    color: #909399;
    margin-top: 5px;
  }
}

.activity-card {
  :deep(.el-timeline) {
    padding-left: 0;
  }
  
  :deep(.el-timeline-item__content) {
    color: #fff;
  }
  
  :deep(.el-timeline-item__timestamp) {
    color: rgba(255, 255, 255, 0.7);
  }
}

.skills-card {
  .radar-chart {
    height: 300px;
  }
}

:deep(.el-card) {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  
  .el-card__header {
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
}

:deep(.el-table) {
  background: transparent;
  
  &::before {
    display: none;
  }
  
  th, td {
    background: transparent;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }
  
  th {
    color: rgba(255, 255, 255, 0.7);
    font-weight: normal;
  }
  
  td {
    color: #fff;
  }
  
  tr:hover > td {
    background: rgba(255, 255, 255, 0.05);
  }
}
</style> 