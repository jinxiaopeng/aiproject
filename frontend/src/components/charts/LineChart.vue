<template>
  <div class="line-chart">
    <canvas ref="chartRef"></canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch } from 'vue'
import Chart from 'chart.js/auto'

export default defineComponent({
  name: 'LineChart',
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
        type: 'line',
        data: {
          labels: props.data.labels,
          datasets: [{
            label: props.data.datasets[0].label,
            data: props.data.datasets[0].data,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100
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
.line-chart {
  width: 100%;
  height: 100%;
}
</style> 