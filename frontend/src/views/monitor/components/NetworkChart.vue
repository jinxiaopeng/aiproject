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

// 格式化流量数据
const formatFlow = (value: number) => {
  if (value >= 1024 * 1024) {
    return `${(value / (1024 * 1024)).toFixed(2)} MB/s`
  }
  if (value >= 1024) {
    return `${(value / 1024).toFixed(2)} KB/s`
  }
  return `${value} B/s`
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
      },
      formatter: (params: any) => {
        let result = `${params[0].axisValue}<br/>`
        params.forEach((item: any) => {
          result += `${item.marker} ${item.seriesName}: ${formatFlow(item.value)}<br/>`
        })
        return result
      }
    },
    legend: {
      data: ['入站流量', '出站流量'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
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
        name: '流量',
        axisLine: {
          lineStyle: {
            color: '#909399'
          }
        },
        axisLabel: {
          color: '#909399',
          formatter: (value: number) => formatFlow(value)
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
        name: '入站流量',
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
        data: [
          1024 * 1024 * 5,
          1024 * 1024 * 4.8,
          1024 * 1024 * 5.2,
          1024 * 1024 * 5.5,
          1024 * 1024 * 4.9,
          1024 * 1024 * 5.1,
          1024 * 1024 * 5.3,
          1024 * 1024 * 4.7,
          1024 * 1024 * 5.0,
          1024 * 1024 * 4.8
        ]
      },
      {
        name: '出站流量',
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
        data: [
          1024 * 1024 * 3,
          1024 * 1024 * 2.8,
          1024 * 1024 * 3.2,
          1024 * 1024 * 3.5,
          1024 * 1024 * 2.9,
          1024 * 1024 * 3.1,
          1024 * 1024 * 3.3,
          1024 * 1024 * 2.7,
          1024 * 1024 * 3.0,
          1024 * 1024 * 2.8
        ]
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