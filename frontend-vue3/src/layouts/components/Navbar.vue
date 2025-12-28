<template>
  <div class="navbar">
    <div class="left">
      <SvgIcon name="tree" class="icon" />
      <span class="title">{{ title }}</span>
    </div>
    <Breadcrumb />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Breadcrumb from '@/components/Breadcrumb.vue'

const route = useRoute()
const title = computed(() => route.meta.title || '页面')
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
</style>
