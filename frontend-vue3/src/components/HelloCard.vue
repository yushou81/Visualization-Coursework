<template>
  <div class="card stats">
    <div class="label">示例状态</div>
    <div class="value">{{ message }}</div>
    <el-button type="primary" size="small" plain @click="increment">点击 +1 ({{ count }})</el-button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useDemoStore } from '@/stores/demo'

const store = useDemoStore()
const count = computed(() => store.count)
const message = computed(() => store.statusText)

const increment = () => store.increment()
</script>

<style scoped>
.stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.label {
  font-size: 14px;
  color: #cbd5e1;
}

.value {
  font-size: 24px;
  font-weight: 700;
  color: #fbbf24;
}
</style>
