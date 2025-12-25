<template>
  <div class="page">
    <el-card header="ECharts 词云占位" shadow="hover">
      <div ref="wordCloudRef" class="chart"></div>
      <p class="hint">迁移个人页词云时，可直接使用此初始化方式（echarts v5 + echarts-wordcloud）。</p>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue'
import { useEcharts } from '@/utils/echarts'

const wordCloudRef = ref(null)
let chart

const demoData = [
  { name: 'security', value: 88 },
  { name: 'network', value: 76 },
  { name: 'login', value: 64 },
  { name: 'email', value: 52 },
  { name: 'threat', value: 48 },
  { name: 'behavior', value: 44 },
  { name: 'analysis', value: 40 }
]

const renderChart = () => {
  if (!wordCloudRef.value) return
  chart = useEcharts(wordCloudRef.value, 'light')
  if (!chart) return

  chart.setOption({
    tooltip: {},
    series: [
      {
        type: 'wordCloud',
        shape: 'circle',
        gridSize: 16,
        sizeRange: [18, 60],
        rotationRange: [0, 0],
        textStyle: {
          color() {
            const colors = ['#2563eb', '#06b6d4', '#f97316', '#e11d48', '#22c55e']
            return colors[Math.floor(Math.random() * colors.length)]
          }
        },
        data: demoData
      }
    ]
  })
}

onMounted(() => {
  renderChart()
  window.addEventListener('resize', () => chart?.resize())
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', () => chart?.resize())
  chart?.dispose()
})
</script>

<style scoped>
.page {
  padding: 12px;
}

.chart {
  width: 100%;
  height: 360px;
}

.hint {
  color: #94a3b8;
  margin: 8px 0 0;
}
</style>
