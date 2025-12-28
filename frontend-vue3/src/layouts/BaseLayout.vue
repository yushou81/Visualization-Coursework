<template>
  <el-container class="layout">
    <el-aside width="220px" class="layout-aside">
      <div class="brand">Visual Vue3</div>
      <Sidebar :items="menuItems" />
    </el-aside>
    <el-container>
      <el-header class="layout-header">
        <Navbar />
      </el-header>
      <el-main class="layout-main">
        <RouterView />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'

const router = useRouter()
const menuItems = computed(() => {
  const base = router.getRoutes().find((r) => r.path === '/')
  return base?.children?.filter((c) => !c.meta?.hidden) || []
})
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background: radial-gradient(120% 120% at 10% 10%, #1f2937 0%, #0f172a 45%, #0b1020 100%);
  color: #e5e7eb;
}

.layout-aside {
  padding: 20px 12px;
  border-right: 1px solid rgba(148, 163, 184, 0.2);
  background: rgba(15, 18, 38, 0.9);
  box-sizing: border-box;
}

.brand {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
}

.icon {
  margin-right: 8px;
}

.menu {
  border-right: none;
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
