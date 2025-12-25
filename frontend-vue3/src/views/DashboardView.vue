<template>
  <div class="page">
    <div class="hero">
      <div>
        <p class="eyebrow">Dashboard</p>
        <h1>迁移中的仪表盘</h1>
        <p class="lede">
          把旧版的首页图表搬到这里。当前为占位内容，路由和布局已准备好。
        </p>
        <el-space>
          <el-button type="primary">添加图表</el-button>
          <el-button>接入数据</el-button>
        </el-space>
      </div>
      <el-card class="status" shadow="hover">
        <p class="label">迁移状态</p>
        <p class="value">待迁移</p>
        <p class="hint">建议先接入 echarts v5，再逐步移植各图表。</p>
      </el-card>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.page {
  padding: 12px;
}

.hero {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}

.eyebrow {
  letter-spacing: 0.8px;
  color: #3b82f6;
  font-weight: 700;
  margin: 0 0 8px;
}

h1 {
  margin: 0;
  font-size: 28px;
  line-height: 1.2;
}

.lede {
  margin: 12px 0 20px;
  color: #475569;
  line-height: 1.6;
}

.status {
  text-align: right;
}

.label {
  margin: 0;
  color: #94a3b8;
}

.value {
  margin: 4px 0;
  font-size: 24px;
  font-weight: 800;
}

.hint {
  margin: 0;
  color: #94a3b8;
}

@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
  }
}
</style>
