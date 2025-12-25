<template>
  <el-container class="layout">
    <el-aside :width="sidebarOpen ? '220px' : '64px'" class="aside">
      <div class="brand" @click="goHome">
        <span class="brand__logo">V3</span>
        <span v-if="sidebarOpen" class="brand__title">Visual Dashboard</span>
      </div>
      <el-menu
        :default-active="route.path"
        background-color="#0b1224"
        text-color="#cbd5e1"
        active-text-color="#3b82f6"
        class="menu"
        :collapse="!sidebarOpen"
        @select="handleSelect"
      >
        <el-menu-item index="/">
          <el-icon><DataAnalysis /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/personal">
          <el-icon><User /></el-icon>
          <span>个人</span>
        </el-menu-item>
        <el-menu-item index="/department">
          <el-icon><OfficeBuilding /></el-icon>
          <span>部门</span>
        </el-menu-item>
        <el-menu-item index="/charts-demo">
          <el-icon><DataAnalysis /></el-icon>
          <span>图表示例</span>
        </el-menu-item>
        <el-menu-item index="/about">
          <el-icon><InfoFilled /></el-icon>
          <span>关于</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <el-button link @click="toggleSidebar">
          <el-icon><component :is="sidebarOpen ? Expand : Fold" /></el-icon>
        </el-button>
        <div class="spacer" />
        <el-tag type="info" effect="dark">Vue 3 / Vite / Element Plus</el-tag>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Fold, Expand, DataAnalysis, User, OfficeBuilding, InfoFilled } from '@element-plus/icons-vue'
import { useAppStore } from '@/stores/app'

const router = useRouter()
const route = useRoute()
const appStore = useAppStore()

const sidebarOpen = computed(() => appStore.sidebarOpen)

const toggleSidebar = () => appStore.toggleSidebar()
const goHome = () => router.push('/')

const handleSelect = (path) => {
  router.push(path)
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
  background: transparent;
}

.aside {
  background: #0b1224;
  color: #cbd5e1;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #10192d;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 64px;
  padding: 0 16px;
  cursor: pointer;
}

.brand__logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6, #06b6d4);
  color: #fff;
  font-weight: 800;
}

.brand__title {
  font-weight: 700;
  color: #e2e8f0;
  letter-spacing: 0.2px;
}

.menu {
  border-right: none;
  flex: 1;
}

.header {
  display: flex;
  align-items: center;
  gap: 12px;
  height: 64px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid #e2e8f0;
}

.main {
  padding: 20px;
}

.spacer {
  flex: 1;
}
</style>
