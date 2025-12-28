<template>
  <div class="scroll-container" ref="scrollContainer" @wheel.prevent="handleScroll">
    <div class="scroll-wrapper" ref="scrollWrapper" :style="{ top: `${top}px` }">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const delta = 15
const top = ref(0)
const scrollContainer = ref<HTMLElement | null>(null)
const scrollWrapper = ref<HTMLElement | null>(null)

const handleScroll = (e: WheelEvent) => {
  const eventDelta = (e as any).wheelDelta || -e.deltaY * 3
  const container = scrollContainer.value
  const wrapper = scrollWrapper.value
  if (!container || !wrapper) return

  const containerHeight = container.offsetHeight
  const wrapperHeight = wrapper.offsetHeight

  if (eventDelta > 0) {
    top.value = Math.min(0, top.value + eventDelta)
  } else {
    if (containerHeight - delta < wrapperHeight) {
      if (top.value < -(wrapperHeight - containerHeight + delta)) {
        top.value = top.value
      } else {
        top.value = Math.max(top.value + eventDelta, containerHeight - wrapperHeight - delta)
      }
    } else {
      top.value = 0
    }
  }
}
</script>

<style scoped>
.scroll-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.scroll-wrapper {
  position: absolute;
  width: 100%;
}
</style>
