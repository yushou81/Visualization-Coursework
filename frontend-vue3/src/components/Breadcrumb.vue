<template>
  <el-breadcrumb separator="/">
    <el-breadcrumb-item v-for="item in crumbs" :key="item.path">
      <span v-if="item.disabled">{{ item.meta?.title || item.path }}</span>
      <RouterLink v-else :to="item.path">{{ item.meta?.title || item.path }}</RouterLink>
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'

const route = useRoute()
const crumbs = computed(() =>
  route.matched
    .filter((item) => item.meta?.title)
    .map((item, index, arr) => ({
      ...item,
      disabled: index === arr.length - 1
    }))
)
</script>
