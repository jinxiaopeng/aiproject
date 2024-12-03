<template>
  <div class="radar-chart">
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch } from 'vue'
import Chart from 'chart.js/auto'

export default defineComponent({
  name: 'RadarChart',
  props: {
    data: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const chartRef = ref<HTMLCanvasElement | null>(null)
    let chart: Chart | null = null

    const initChart = () => {
      if (!chartRef.value) return

      chart = new Chart(chartRef.value, {
        type: 'radar',
        data: {
          labels: props.data.labels,
          datasets: [{
            label: '技能分布',
            data: props.data.datasets[0].data,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
          }]
        },
        options: {
          scales: {
            r: {
              beginAtZero: true,
              max: 100
            }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }
      })
    }

    watch(() => props.data, () => {
      if (chart) {
        chart.destroy()
      }
      initChart()
    }, { deep: true })

    onMounted(() => {
      initChart()
    })

    return {
      chartRef
    }
  }
})
</script>

<style scoped>
.radar-chart {
  width: 100%;
  height: 100%;
}
</style> 