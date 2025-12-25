<template>
  <div class="app-shell">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
</script>

<style scoped>
.app-shell {
  min-height: 100vh;
  background: radial-gradient(circle at 20% 20%, #f7fbff 0, #e8f1ff 40%, #f5f7fa 70%);
  color: #1f2933;
}
</style>
