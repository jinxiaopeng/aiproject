<template>
  <div class="trend-chart">
    <div ref="chartRef" class="chart-container"></div>
    
    <div v-if="loading" class="loading-overlay">
      <el-icon class="loading-icon" :size="24"><Loading /></el-icon>
      <span>加载中...</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { Loading } from '@element-plus/icons-vue'
import type { AlertTrend } from '@/types/monitor'

const props = defineProps<{
  data: AlertTrend[]
  type: 'security' | 'lab' | 'system'
  loading?: boolean
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  updateChart()
  
  window.addEventListener('resize', handleResize)
}

// 更新图表数据
const updateChart = () => {
  if (!chart || !props.data.length) return

  const timestamps = props.data.map(item => item.timestamp)
  const values = props.data.map(item => {
    switch (props.type) {
      case 'security':
        return item.security_alerts
      case 'lab':
        return item.lab_alerts
      case 'system':
        return item.system_alerts
      default:
        return 0
    }
  })

  const option: echarts.EChartsOption = {
    grid: {
      top: 20,
      right: 20,
      bottom: 30,
      left: 50,
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const [param] = params
        return `${param.name}<br/>${param.value} 个告警`
      }
    },
    xAxis: {
      type: 'category',
      data: timestamps,
      boundaryGap: false,
      axisLine: {
        lineStyle: {
          color: '#ddd'
        }
      },
      axisLabel: {
        color: '#666',
        formatter: (value: string) => {
          const date = new Date(value)
          return `${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
        }
      }
    },
    yAxis: {
      type: 'value',
      splitLine: {
        lineStyle: {
          color: '#eee'
        }
      },
      axisLabel: {
        color: '#666'
      }
    },
    series: [
      {
        type: 'line',
        data: values,
        smooth: true,
        showSymbol: false,
        lineStyle: {
          width: 2,
          color: getTypeColor()
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: getTypeColor(0.2)
            },
            {
              offset: 1,
              color: getTypeColor(0.05)
            }
          ])
        }
      }
    ]
  }

  chart.setOption(option)
}

// 获取类型颜色
const getTypeColor = (alpha = 1) => {
  const colors = {
    security: `rgba(245, 108, 108, ${alpha})`,
    lab: `rgba(103, 194, 58, ${alpha})`,
    system: `rgba(144, 147, 153, ${alpha})`
  }
  return colors[props.type]
}

// 处理窗口大小变化
const handleResize = () => {
  chart?.resize()
}

// 监听数据变化
watch(
  () => [props.data, props.type],
  () => {
    updateChart()
  },
  { deep: true }
)

onMounted(() => {
  initChart()
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
</script>

<style lang="scss" scoped>
.trend-chart {
  position: relative;
  width: 100%;
  height: 100%;

  .chart-container {
    width: 100%;
    height: 300px;
  }

  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.9);
    
    .loading-icon {
      animation: rotate 1s linear infinite;
      margin-bottom: 8px;
    }
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 