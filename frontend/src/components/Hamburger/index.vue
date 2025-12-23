<template>
  <div 
    :class="['hamburger', { 'is-active': isActive }]"
    @click="handleClick"
  >
    <el-icon :size="20">
      <Fold v-if="isActive" />
      <Expand v-else />
    </el-icon>
  </div>
</template>

<script setup>
import { Fold, Expand } from '@element-plus/icons-vue'

defineProps({
    isActive: {
      type: Boolean,
      default: false
  }
})

const emit = defineEmits(['toggle-click'])

const handleClick = () => {
  emit('toggle-click')
}
</script>

<style scoped>
.hamburger {
    display: inline-block;
    cursor: pointer;
  transition: transform 0.3s;
  
  &:hover {
    opacity: 0.8;
}

  &.is-active {
    transform: rotate(90deg);
  }
}
</style>
