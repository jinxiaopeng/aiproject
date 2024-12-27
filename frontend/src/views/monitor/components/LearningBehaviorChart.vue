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

  const option: any = {
    title: {
      text: '学习行为分析',
      left: 'center',
      top: 20
    },
    tooltip: {
      trigger: 'axis',
      formatter: '{b0}: {c0}分钟'
    },
    grid: {
      top: 70,
      left: '5%',
      right: '5%',
      bottom: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: props.data.map(item => {
        const date = new Date(item.lastAccess)
        return `${date.getHours().toString().padStart(2, '0')}:00`
      }),
      axisLabel: {
        interval: 2
      }
    },
    yAxis: {
      type: 'value',
      name: '学习时长(分钟)',
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    series: [{
      name: '学习时长',
      type: 'line',
      smooth: true,
      data: props.data.map(item => item.totalTime),
      symbolSize: 6,
      itemStyle: {
        color: '#409EFF'
      },
      areaStyle: {
        opacity: 0.2
      }
    }]
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
  height: 400px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);

  .chart-container {
    width: 100%;
    height: 100%;
  }
}
</style>
