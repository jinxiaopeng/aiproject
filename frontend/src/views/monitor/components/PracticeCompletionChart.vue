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
        type: 'shadow'
      }
    },
    legend: {
      data: ['已完成', '进行中', '未开始'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      boundaryGap: [0, 0.01],
      axisLabel: {
        formatter: '{value}%'
      }
    },
    yAxis: {
      type: 'category',
      data: ['Web安全基础', 'SQL注入', 'XSS攻防', '文件上传', '权限控制', '加密解密']
    },
    series: [
      {
        name: '已完成',
        type: 'bar',
        stack: 'total',
        label: {
          show: true,
          formatter: '{c}%'
        },
        emphasis: {
          focus: 'series'
        },
        data: [85, 75, 65, 60, 70, 55]
      },
      {
        name: '进行中',
        type: 'bar',
        stack: 'total',
        label: {
          show: true,
          formatter: '{c}%'
        },
        emphasis: {
          focus: 'series'
        },
        data: [10, 15, 20, 25, 15, 30]
      },
      {
        name: '未开始',
        type: 'bar',
        stack: 'total',
        label: {
          show: true,
          formatter: '{c}%'
        },
        emphasis: {
          focus: 'series'
        },
        data: [5, 10, 15, 15, 15, 15]
      }
    ],
    color: ['#67C23A', '#E6A23C', '#909399'],
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
