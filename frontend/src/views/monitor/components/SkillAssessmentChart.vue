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
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      data: ['优秀', '良好', '合格', '待提升']
    },
    series: [
      {
        name: '技能评估',
        type: 'pie',
        radius: ['50%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: 35, name: '优秀' },
          { value: 45, name: '良好' },
          { value: 15, name: '合格' },
          { value: 5, name: '待提升' }
        ]
      },
      {
        name: '技能评估',
        type: 'pie',
        radius: ['0%', '40%'],
        avoidLabelOverlap: false,
        label: {
          show: true,
          position: 'center',
          formatter: [
            '{title|总体评价}',
            '{value|良好}'
          ].join('\n'),
          rich: {
            title: {
              fontSize: 14,
              color: '#999',
              padding: [0, 0, 10, 0]
            },
            value: {
              fontSize: 24,
              fontWeight: 'bold',
              color: '#67C23A'
            }
          }
        },
        emphasis: {
          label: {
            show: true
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: 100, name: '总体评价' }
        ],
        itemStyle: {
          color: 'rgba(103,194,58,0.1)'
        }
      }
    ],
    color: ['#67C23A', '#409EFF', '#E6A23C', '#F56C6C'],
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
