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
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985'
        }
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: [
      {
        type: 'category',
        boundaryGap: false,
        data: ['1min前', '2min前', '3min前', '4min前', '5min前', '6min前', '7min前', '8min前', '9min前', '10min前'],
        axisLine: {
          lineStyle: {
            color: '#909399'
          }
        },
        axisLabel: {
          color: '#909399'
        }
      }
    ],
    yAxis: [
      {
        type: 'value',
        name: '负载',
        axisLine: {
          lineStyle: {
            color: '#909399'
          }
        },
        axisLabel: {
          color: '#909399'
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(144,147,153,0.1)'
          }
        }
      }
    ],
    series: [
      {
        name: '1分钟',
        type: 'line',
        smooth: true,
        lineStyle: {
          width: 2,
          color: '#409EFF'
        },
        showSymbol: false,
        areaStyle: {
          opacity: 0.3,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: '#409EFF'
            },
            {
              offset: 1,
              color: 'rgba(255,255,255,0)'
            }
          ])
        },
        emphasis: {
          focus: 'series'
        },
        data: [2.5, 2.8, 2.3, 2.6, 2.9, 3.2, 2.8, 2.5, 2.7, 2.4]
      },
      {
        name: '5分钟',
        type: 'line',
        smooth: true,
        lineStyle: {
          width: 2,
          color: '#67C23A'
        },
        showSymbol: false,
        areaStyle: {
          opacity: 0.3,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: '#67C23A'
            },
            {
              offset: 1,
              color: 'rgba(255,255,255,0)'
            }
          ])
        },
        emphasis: {
          focus: 'series'
        },
        data: [2.8, 2.9, 2.7, 2.8, 3.0, 3.1, 2.9, 2.8, 2.9, 2.7]
      },
      {
        name: '15分钟',
        type: 'line',
        smooth: true,
        lineStyle: {
          width: 2,
          color: '#E6A23C'
        },
        showSymbol: false,
        areaStyle: {
          opacity: 0.3,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: '#E6A23C'
            },
            {
              offset: 1,
              color: 'rgba(255,255,255,0)'
            }
          ])
        },
        emphasis: {
          focus: 'series'
        },
        data: [3.0, 3.1, 2.9, 3.0, 3.1, 3.2, 3.0, 2.9, 3.0, 2.9]
      }
    ],
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