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
      type: 'scroll',
      orient: 'horizontal',
      bottom: 0,
      data: [
        'SQL注入',
        'XSS攻击',
        '文件上传',
        '未授权访问',
        '暴力破解',
        '敏感信息泄露',
        '其他'
      ]
    },
    series: [
      {
        name: '威胁分布',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          position: 'outside',
          formatter: '{b}\n{c}次 ({d}%)'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        data: [
          { value: 35, name: 'SQL注入' },
          { value: 30, name: 'XSS攻击' },
          { value: 25, name: '文件上传' },
          { value: 20, name: '未授权访问' },
          { value: 15, name: '暴力破解' },
          { value: 10, name: '敏感信息泄露' },
          { value: 5, name: '其他' }
        ]
      },
      {
        name: '威胁等级',
        type: 'pie',
        radius: ['0%', '30%'],
        center: ['50%', '45%'],
        label: {
          position: 'center',
          formatter: [
            '{title|威胁等级}',
            '{value|中危}'
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
              color: '#E6A23C'
            }
          }
        },
        data: [
          { value: 100, name: '威胁等级' }
        ],
        itemStyle: {
          color: 'rgba(230,162,60,0.1)'
        }
      }
    ],
    color: [
      '#F56C6C',
      '#E6A23C',
      '#409EFF',
      '#67C23A',
      '#909399',
      '#FFCD00',
      '#C0C4CC'
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