<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <transition name="fade-transform" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<script setup>
// Vue 3 Composition API
</script>

<style lang="scss" scoped>
#app {
  width: 100%;
  height: 100%;
}
</style>
