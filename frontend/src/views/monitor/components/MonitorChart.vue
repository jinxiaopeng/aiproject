<template>
  <div class="chart-container" v-loading="loading">
    <div class="chart-header">
      <div class="time-range">
        <el-radio-group v-model="timeRange" size="small" @change="handleTimeRangeChange">
          <el-radio-button label="day">今日</el-radio-button>
          <el-radio-button label="week">本周</el-radio-button>
          <el-radio-button label="month">本月</el-radio-button>
        </el-radio-group>
      </div>
      <div class="chart-actions">
        <el-button-group size="small">
          <el-button 
            :type="chartType === 'line' ? 'primary' : ''" 
            @click="chartType = 'line'"
          >
            <el-icon><trend-charts /></el-icon>
          </el-button>
          <el-button 
            :type="chartType === 'bar' ? 'primary' : ''" 
            @click="chartType = 'bar'"
          >
            <el-icon><histogram /></el-icon>
          </el-button>
        </el-button-group>
        <el-button 
          type="primary" 
          :icon="Refresh" 
          circle 
          size="small"
          @click="refreshChart"
        />
      </div>
    </div>

    <div class="chart-content">
      <div ref="chartRef" class="echarts-container"></div>
    </div>

    <div class="chart-footer">
      <div class="legend">
        <div 
          v-for="type in alertTypes" 
          :key="type.value"
          class="legend-item"
          :class="{ disabled: !selectedTypes.includes(type.value) }"
          @click="toggleAlertType(type.value)"
        >
          <span 
            class="color-dot"
            :style="{ backgroundColor: type.color }"
          ></span>
          <span class="label">{{ type.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import {
  TrendCharts as TrendChartsIcon,
  DataLine as HistogramIcon,
  Refresh as RefreshIcon
} from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'

const props = defineProps<{
  timeRange: 'day' | 'week' | 'month'
}>()

const loading = ref(false)
const chartRef = ref<HTMLElement>()
const timeRange = ref('day')
const chartType = ref<'line' | 'bar'>('line')
let chart: echarts.ECharts | null = null

// 预警类型配置
const alertTypes = [
  { label: '登录预警', value: 'login', color: '#f56c6c' },
  { label: '操作预警', value: 'operation', color: '#e6a23c' },
  { label: '安全预警', value: 'security', color: '#ff4d4f' }
]

// 选中的预警类型
const selectedTypes = ref(['login', 'operation', 'security'])

// 模拟数据
const mockData: Record<'day' | 'week' | 'month', {
  xAxis: string[]
  series: Record<string, number[]>
}> = {
  day: {
    xAxis: Array.from({ length: 24 }, (_, i) => `${String(i).padStart(2, '0')}:00`),
    series: {
      login: Array.from({ length: 24 }, () => Math.floor(Math.random() * 10)),
      operation: Array.from({ length: 24 }, () => Math.floor(Math.random() * 8)),
      security: Array.from({ length: 24 }, () => Math.floor(Math.random() * 5))
    }
  },
  week: {
    xAxis: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    series: {
      login: Array.from({ length: 7 }, () => Math.floor(Math.random() * 50)),
      operation: Array.from({ length: 7 }, () => Math.floor(Math.random() * 40)),
      security: Array.from({ length: 7 }, () => Math.floor(Math.random() * 30))
    }
  },
  month: {
    xAxis: Array.from({ length: 30 }, (_, i) => `${i + 1}日`),
    series: {
      login: Array.from({ length: 30 }, () => Math.floor(Math.random() * 100)),
      operation: Array.from({ length: 30 }, () => Math.floor(Math.random() * 80)),
      security: Array.from({ length: 30 }, () => Math.floor(Math.random() * 60))
    }
  }
}

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return

  chart = echarts.init(chartRef.value)
  updateChart()
}

// 更新图表
const updateChart = () => {
  if (!chart) return

  const data = mockData[timeRange.value]
  const option: EChartsOption = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(0, 0, 0, 0.7)',
      borderColor: '#64ffda',
      borderWidth: 1,
      textStyle: { color: '#fff' }
    },
    legend: {
      show: false
    },
    grid: {
      top: 10,
      right: 10,
      bottom: 20,
      left: 40,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.xAxis,
      axisLine: {
        lineStyle: { color: '#8892b0' }
      },
      axisLabel: {
        color: '#8892b0',
        fontSize: 12
      }
    },
    yAxis: {
      type: 'value',
      splitLine: {
        lineStyle: { color: '#eee' }
      }
    },
    series: alertTypes
      .filter(type => selectedTypes.value.includes(type.value))
      .map(type => ({
        name: type.label,
        type: chartType.value,
        data: data.series[type.value],
        smooth: true,
        showSymbol: false,
        itemStyle: {
          color: type.color
        },
        areaStyle: chartType.value === 'line' ? {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: type.color + '40' },
            { offset: 1, color: type.color + '10' }
          ])
        } : undefined
      }))
  }

  chart.setOption(option)
}

// 处理窗口大小变化
const handleResize = () => {
  chart?.resize()
}

// 处理时间范围变化
const handleTimeRangeChange = () => {
  updateChart()
}

// 切换预警类型
const toggleAlertType = (type: string) => {
  const index = selectedTypes.value.indexOf(type)
  if (index > -1) {
    selectedTypes.value.splice(index, 1)
  } else {
    selectedTypes.value.push(type)
  }
  updateChart()
}

// 切换图表类型
const toggleChartType = () => {
  chartType.value = chartType.value === 'line' ? 'bar' : 'line'
  updateChart()
}

// 刷新数据
const refreshData = () => {
  loading.value = true
  setTimeout(() => {
    updateChart()
    loading.value = false
  }, 1000)
}

// 监听属性变化
watch(() => props.timeRange, (newVal) => {
  timeRange.value = newVal
  updateChart()
})

// 初始化
onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

// 清理
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
</script>

<style lang="scss" scoped>
.chart-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 16px;

  .chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    .chart-actions {
      display: flex;
      gap: 12px;
      align-items: center;
    }
  }

  .chart-content {
    flex: 1;
    position: relative;

    .echarts-container {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
    }
  }

  .chart-footer {
    margin-top: 16px;

    .legend {
      display: flex;
      justify-content: center;
      gap: 24px;
      flex-wrap: wrap;

      .legend-item {
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 4px;
        transition: all 0.3s ease;

        &:hover {
          background: var(--el-fill-color-light);
        }

        &.disabled {
          opacity: 0.5;
        }

        .color-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
        }

        .label {
          font-size: 12px;
          color: var(--el-text-color-regular);
        }
      }
    }
  }
}
</style> 