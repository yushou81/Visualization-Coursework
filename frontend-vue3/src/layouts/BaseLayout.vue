<template>
  <el-container class="layout">
    <el-header class="layout-header">
      <Navbar />
    </el-header>
    <el-main class="layout-main">
      <RouterView />
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background: radial-gradient(120% 120% at 10% 10%, #1f2937 0%, #0f172a 45%, #0b1020 100%);
  color: #e5e7eb;
}

.layout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 20px;
  box-sizing: border-box;
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
  background: rgba(30, 41, 59, 0.7);
}

.layout-main {
  padding: 20px;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

.meta {
  font-size: 12px;
  color: #cbd5e1;
}
</style>
