<template>
  <div class="home">
    <section class="hero card">
      <div>
        <h1>Vue3 / Vite 基线</h1>
        <p>组合式 API + Element Plus + Pinia + ECharts5 示例。</p>
        <el-space>
          <el-button type="primary" @click="goDocs">查看计划文档</el-button>
          <el-button type="success" plain @click="showMessage">操作提示</el-button>
        </el-space>
      </div>
    </section>
    <div class="grid">
      <HelloCard />
      <HelloChart />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ElMessage } from 'element-plus'
import HelloCard from '@/components/HelloCard.vue'
import HelloChart from '@/components/HelloChart.vue'

const showMessage = () => {
  ElMessage.success('组合式 API 示例：按钮已点击')
}

const goDocs = () => {
  window.open('https://vitejs.dev/guide/', '_blank')
}
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.hero h1 {
  margin: 0 0 8px;
  font-size: 24px;
}

.hero p {
  margin: 0 0 12px;
  color: #cbd5e1;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}
</style>
