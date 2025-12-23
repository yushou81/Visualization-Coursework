<template>
  <ScrollBar>
    <el-menu
      mode="vertical"
      :default-active="activeMenu"
      :collapse="isCollapse"
      :unique-opened="true"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409eff"
      router
    >
      <SidebarItem 
        v-for="route in routes" 
        :key="route.path"
        :item="route"
        :base-path="route.path"
      />
    </el-menu>
  </ScrollBar>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { constantRouterMap } from '@/router'
import SidebarItem from './SidebarItem.vue'
import ScrollBar from '@/components/ScrollBar/index.vue'
import { useAppStore } from '@/store/modules/app'

const route = useRoute()
const appStore = useAppStore()

const sidebar = computed(() => appStore.sidebar)
const routes = computed(() => {
  return constantRouterMap.filter(route => {
    if (route.hidden) return false
    return Array.isArray(route.children) && route.children.length > 0
  })
})
const isCollapse = computed(() => !sidebar.value.opened)
const activeMenu = computed(() => {
  const { meta, path } = route
  if (meta?.activeMenu) {
    return meta.activeMenu
  }
  return path
})
</script>

<style lang="scss" scoped>
:deep(.el-menu) {
  border: none;
  height: 100%;
  width: 100% !important;
}
</style>
