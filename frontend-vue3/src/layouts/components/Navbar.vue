<template>
  <div class="navbar">
    <div class="left">
      <SvgIcon name="tree" class="icon" />
      <span class="title">{{ title }}</span>
    </div>
    <el-menu
      mode="horizontal"
      :default-active="activePath"
      background-color="transparent"
      text-color="#e5e7eb"
      active-text-color="#fbbf24"
      class="menu"
      router
    >
      <el-menu-item v-for="item in menuItems" :key="item.path" :index="item.path">
        <SvgIcon v-if="item.meta?.icon" :name="item.meta.icon as string" class="icon" />
        <span>{{ item.meta?.title || item.path }}</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter, RouteRecordRaw } from 'vue-router'

const route = useRoute()
const router = useRouter()

const title = computed(() => route.meta.title || '页面')
const activePath = computed(() => route.path)
const menuItems = computed<RouteRecordRaw[]>(() => {
  const base = router.getRoutes().find((r) => r.path === '/')
  return base?.children?.filter((c) => !c.meta?.hidden) || []
})
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  padding: 0 20px;
  box-sizing: border-box;
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
  background: rgba(30, 41, 59, 0.7);
}

.left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.title {
  font-size: 18px;
  font-weight: 600;
}

.icon {
  color: #fbbf24;
}

.menu {
  border-bottom: none;
}
</style>
