<template>
  <div class="page">
    <el-result
      icon="success"
      title="部门视图占位"
      sub-title="将旧版部门分析页面迁移至此，复用 echarts/表格逻辑。"
    />
    <el-alert
      type="info"
      title="提示"
      description="在迁移时，优先确保数据接口与旧版保持一致，再逐步完善样式。"
      show-icon
      :closable="false"
    />
  </div>
</template>

<script setup>
</script>

<style scoped>
.page {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
