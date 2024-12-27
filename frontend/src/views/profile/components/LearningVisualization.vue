<template>
  <div class="visualization-container">
    <!-- 统计数字 -->
    <div class="stats-overview">
      <div class="stat-item">
        <div class="stat-value">{{ stats.completedCourses }}/{{ stats.totalCourses }}</div>
        <div class="stat-label">完成课程</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ stats.averageScore }}分</div>
        <div class="stat-label">平均得分</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ formatStudyTime(stats.totalStudyTime) }}</div>
        <div class="stat-label">总学习时长</div>
      </div>
    </div>

    <!-- 技能雷达图 -->
    <el-card class="radar-card">
      <template #header>
        <div class="card-header">
          <h3>技能分布</h3>
          <el-tooltip content="展示各个安全领域的技能掌握程度">
            <el-icon><QuestionFilled /></el-icon>
          </el-tooltip>
        </div>
      </template>
      <div class="chart-container">
        <v-chart class="chart" :option="radarOption" autoresize />
      </div>
    </el-card>

    <!-- 学习时长统计 -->
    <el-card class="stats-card">
      <template #header>
        <div class="card-header">
          <h3>学习时长</h3>
          <el-tooltip content="展示每日学习时间投入">
            <el-icon><QuestionFilled /></el-icon>
          </el-tooltip>
        </div>
      </template>
      <div class="weekly-chart">
        <v-chart class="chart" :option="weeklyOption" autoresize />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { QuestionFilled } from '@element-plus/icons-vue'
import type { EChartsOption } from 'echarts'
import { graphic } from 'echarts/core'

// 学习统计数据
const stats = ref({
  totalCourses: 12,
  completedCourses: 5,
  averageScore: 85,
  totalStudyTime: 3600 * 24, // 秒为单位
  challengesCompleted: 15,
  weeklyStudyTime: [
    { date: '周一', time: 2 },
    { date: '周二', time: 3 },
    { date: '周三', time: 1.5 },
    { date: '周四', time: 4 },
    { date: '周五', time: 2.5 },
    { date: '周六', time: 3.5 },
    { date: '周日', time: 2 }
  ]
})

// 技能数据
const skillData = ref([
  { name: 'Web安全', value: 80 },
  { name: '系统安全', value: 65 },
  { name: '网络安全', value: 70 },
  { name: '密码学', value: 55 },
  { name: '安全开发', value: 60 },
  { name: '移动安全', value: 45 }
])

// 雷达图配置
const radarOption = computed<EChartsOption>(() => ({
  radar: {
    indicator: skillData.value.map(skill => ({
      name: skill.name,
      max: 100
    })),
    splitArea: {
      areaStyle: {
        color: ['rgba(0, 0, 0, 0.1)']
      }
    }
  },
  series: [{
    type: 'radar',
    data: [{
      value: skillData.value.map(skill => skill.value),
      name: '技能掌握度',
      areaStyle: {
        color: new graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(100, 255, 218, 0.5)' },
          { offset: 1, color: 'rgba(100, 255, 218, 0.1)' }
        ])
      },
      lineStyle: {
        color: '#64ffda'
      },
      itemStyle: {
        color: '#64ffda'
      }
    }]
  }]
}))

// 周学习时间图表配置
const weeklyOption = computed<EChartsOption>(() => ({
  tooltip: {
    trigger: 'axis'
  },
  xAxis: {
    type: 'category',
    data: stats.value.weeklyStudyTime.map(item => item.date),
    axisLine: {
      lineStyle: {
        color: '#8892b0'
      }
    }
  },
  yAxis: {
    type: 'value',
    name: '学习时长(小时)',
    axisLine: {
      lineStyle: {
        color: '#8892b0'
      }
    },
    splitLine: {
      lineStyle: {
        color: 'rgba(136, 146, 176, 0.2)'
      }
    }
  },
  series: [{
    data: stats.value.weeklyStudyTime.map(item => item.time),
    type: 'bar',
    itemStyle: {
      color: new graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: '#64ffda' },
        { offset: 1, color: 'rgba(100, 255, 218, 0.3)' }
      ])
    }
  }]
}))

// 格式化学习时间
const formatStudyTime = (seconds: number) => {
  const hours = Math.floor(seconds / 3600)
  return `${hours}小时`
}
</script>

<style lang="scss" scoped>
.visualization-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin: 20px 0;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 10px;
}

.stat-item {
  text-align: center;
  padding: 24px;
  background: var(--el-bg-color);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;

  &:hover {
    transform: translateY(-2px);
  }

  .stat-value {
    font-size: 28px;
    font-weight: bold;
    color: #64ffda;
    margin-bottom: 8px;
  }

  .stat-label {
    color: #8892b0;
    font-size: 14px;
  }
}

.radar-card,
.stats-card {
  background-color: var(--el-bg-color);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color-light);

  h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 500;
    color: var(--el-text-color-primary);
  }
}

.chart-container {
  height: 400px;
  padding: 20px;
}

.chart {
  width: 100%;
  height: 100%;
}

.weekly-chart {
  height: 300px;
  padding: 20px;
}

@media (max-width: 768px) {
  .stats-overview {
    grid-template-columns: repeat(2, 1fr);
  }

  .chart-container,
  .weekly-chart {
    height: 300px;
  }
}

@media (max-width: 480px) {
  .stats-overview {
    grid-template-columns: 1fr;
  }
}
</style> 