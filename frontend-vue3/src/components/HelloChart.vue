<template>
  <div class="card">
    <div class="chart-title">示例折线图（ECharts 5）</div>
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import * as echarts from 'echarts'

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null

onMounted(() => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value, undefined, { renderer: 'canvas' })
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] },
    yAxis: { type: 'value' },
    series: [
      {
        type: 'line',
        smooth: true,
        areaStyle: {},
        data: [150, 230, 224, 218, 135, 147, 260]
      }
    ]
  })
})

onUnmounted(() => {
  chart?.dispose()
})
</script>

<style scoped>
.chart-title {
  margin-bottom: 12px;
  font-weight: 600;
  color: #e5e7eb;
}

.chart {
  width: 100%;
  height: 320px;
}
</style>
