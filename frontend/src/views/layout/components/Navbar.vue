<template>
  <div class="navbar">
    <Hamburger 
      class="hamburger-container" 
      :is-active="sidebar.opened"
      @toggle-click="toggleSideBar"
    />
    <Breadcrumb />
      </div>
</template>

<script setup>
import { computed } from 'vue'
import Breadcrumb from '@/components/Breadcrumb/index.vue'
import Hamburger from '@/components/Hamburger/index.vue'
import { useAppStore } from '@/store/modules/app'

const appStore = useAppStore()
const sidebar = computed(() => appStore.sidebar)

const toggleSideBar = () => {
  appStore.toggleSideBar()
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 60px;
  overflow: hidden;
  position: relative;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  
  .hamburger-container {
    line-height: 60px;
    height: 60px;
    float: left;
    padding: 0 15px;
      cursor: pointer;
    transition: background 0.3s;
    
    &:hover {
      background: rgba(0, 0, 0, 0.025);
    }
  }
}
</style>
