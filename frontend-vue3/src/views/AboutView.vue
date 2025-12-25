<template>
  <div class="page">
    <el-card>
      <h2>关于这个新工程</h2>
      <p>
        这里是全新的 Vue 3 + Vite 脚手架，用于替换旧的 Vue 2 + webpack 3 前端。
        所有内容与原有 frontend 目录隔离，你可以按需迁移页面。
      </p>
      <ul>
        <li>使用 Element Plus 代替 Element UI</li>
        <li>路由升级为 Vue Router 4，支持动态路由和守卫</li>
        <li>状态管理默认 Pinia（也可改用 Vuex 4）</li>
        <li>基于 Vite 的现代构建，支持 ESM 和 TS 扩展（如需）</li>
      </ul>
    </el-card>
  </div>
</template>

<script setup>
</script>

<style scoped>
.page {
  padding: 24px;
  max-width: 960px;
  margin: 0 auto;
}

ul {
  margin: 12px 0 0;
  padding-left: 16px;
  line-height: 1.7;
}
</style>
