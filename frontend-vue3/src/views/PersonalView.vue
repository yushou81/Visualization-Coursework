<template>
  <div class="page">
    <el-result
      icon="info"
      title="Personal 页面占位"
      sub-title="在这里迁移旧版的个人视图（词云、网络流量、登录等图表）。"
    >
      <template #extra>
        <el-button type="primary" @click="goBack">返回首页</el-button>
      </template>
    </el-result>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const goBack = () => router.push({ name: 'home' })
</script>

<style scoped>
.page {
  padding: 48px 24px;
}
</style>
