<template>
  <div class="chart-wrapper">
    <div 
      ref="chartRef"
      class="chart-container"
      v-loading="loading"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'

const props = defineProps<{
  data: any[]
  loading?: boolean
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  chart = echarts.init(chartRef.value)
  setOptions()
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
}

// 设置图表配置
const setOptions = () => {
  if (!chart) return

  const option: EChartsOption = {
    tooltip: {
      trigger: 'item'
    },
    legend: {
      data: ['当前水平', '目标水平'],
      bottom: 0
    },
    radar: {
      indicator: [
        { name: 'Web安全', max: 100 },
        { name: '系统安全', max: 100 },
        { name: '网络安全', max: 100 },
        { name: '密码学', max: 100 },
        { name: '渗透测试', max: 100 },
        { name: '安全开发', max: 100 }
      ],
      center: ['50%', '50%'],
      radius: '65%',
      splitNumber: 4,
      splitArea: {
        areaStyle: {
          color: ['rgba(255,255,255,0.1)', 'rgba(255,255,255,0.2)'],
          shadowColor: 'rgba(0, 0, 0, 0.2)',
          shadowBlur: 10
        }
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.2)'
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.2)'
        }
      }
    },
    series: [
      {
        name: '知识点掌握度',
        type: 'radar',
        data: [
          {
            value: [85, 75, 80, 70, 90, 65],
            name: '当前水平',
            areaStyle: {
              color: 'rgba(64,158,255,0.3)'
            },
            lineStyle: {
              width: 2
            }
          },
          {
            value: [100, 90, 95, 85, 95, 80],
            name: '目标水平',
            lineStyle: {
              width: 2,
              type: 'dashed'
            }
          }
        ]
      }
    ],
    color: ['#409EFF', '#67C23A'],
    backgroundColor: 'transparent'
  }

  chart.setOption(option)
}

// 处理窗口大小变化
const handleResize = () => {
  chart?.resize()
}

// 监听数据变化
watch(
  () => props.data,
  () => {
    setOptions()
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
.chart-wrapper {
  width: 100%;
  height: 100%;

  .chart-container {
    width: 100%;
    height: 100%;
  }
}
</style>
