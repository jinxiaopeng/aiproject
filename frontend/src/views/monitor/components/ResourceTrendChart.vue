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
  type: 'cpu' | 'memory' | 'disk' | 'network'
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

// 获取资源类型配置
const getResourceConfig = (type: string) => {
  const configs = {
    cpu: {
      name: 'CPU使用率',
      unit: '%',
      color: '#409EFF',
      data: [45, 42, 47, 50, 48, 55, 52, 48, 50, 52, 48, 45]
    },
    memory: {
      name: '内存使用率',
      unit: '%',
      color: '#67C23A',
      data: [62, 58, 65, 68, 70, 72, 75, 70, 68, 65, 62, 60]
    },
    disk: {
      name: '磁盘使用率',
      unit: '%',
      color: '#E6A23C',
      data: [75, 76, 77, 78, 78, 79, 80, 80, 81, 82, 82, 83]
    },
    network: {
      name: '网络带宽使用',
      unit: 'Mbps',
      color: '#F56C6C',
      data: [120, 132, 101, 134, 90, 230, 210, 180, 160, 150, 140, 130]
    }
  }
  return configs[type] || configs.cpu
}

// 设置图表配置
const setOptions = () => {
  if (!chart) return

  const config = getResourceConfig(props.type)
  const times = ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00']

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
        data: times,
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
        name: config.unit,
        axisLine: {
          lineStyle: {
            color: '#909399'
          }
        },
        axisLabel: {
          color: '#909399',
          formatter: `{value} ${config.unit}`
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
        name: config.name,
        type: 'line',
        stack: 'Total',
        smooth: true,
        lineStyle: {
          width: 2,
          color: config.color
        },
        showSymbol: false,
        areaStyle: {
          opacity: 0.3,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: config.color
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
        data: config.data
      },
      {
        name: '告警阈值',
        type: 'line',
        lineStyle: {
          type: 'dashed',
          color: '#F56C6C'
        },
        showSymbol: false,
        data: new Array(12).fill(90),
        markArea: {
          itemStyle: {
            color: 'rgba(245,108,108,0.1)'
          },
          data: [
            [
              {
                yAxis: 90
              },
              {
                yAxis: 100
              }
            ]
          ]
        }
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

// 监听数据和类型变化
watch(
  [() => props.data, () => props.type],
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