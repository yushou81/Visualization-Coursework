<template>
  <div class="app-wrapper" :class="{ hideSidebar: !sidebar.opened }">
    <Sidebar class="sidebar-container" />
    <div class="main-container">
      <Navbar />
      <AppMain />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Navbar, Sidebar, AppMain } from '@/views/layout/components'
import { useAppStore } from '@/store/modules/app'

const appStore = useAppStore()
const sidebar = computed(() => appStore.sidebar)
</script>

<style lang="scss" scoped>
@import "@/styles/mixin.scss";

.app-wrapper {
  @include clearfix;
  position: relative;
  height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #0B3042 0%, #437C8F 100%);
  background-attachment: fixed;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url(@/assets/pumpkin.png);
    background-size: cover;
    background-position: center;
    opacity: 0.05;
    z-index: 0;
  }
  
  .sidebar-container {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    z-index: 1001;
    transition: width 0.28s;
    width: 210px;
  }
  
  .main-container {
    min-height: 100%;
    transition: margin-left 0.28s;
    margin-left: 210px;
    position: relative;
    z-index: 1;
  }
  
  &.hideSidebar {
    .sidebar-container {
      width: 54px !important;
    }
    
    .main-container {
      margin-left: 54px;
    }
  }
}
</style>
