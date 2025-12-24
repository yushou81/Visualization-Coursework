<template>
<div class="dashboard-container">
    <el-card shadow="hover" class="alert-card">
        <el-alert
          title="提示：点击员工节点可显示该员工的邮件收发词云图信息"
        type="info"
        :closable="false"
        show-icon
      />
    </el-card>
    
    <el-card shadow="hover" class="chart-card">
      <Departmentcloudword />
    </el-card>
    
    <el-row :gutter="20" class="content-row">
      <el-col :xs="24" :sm="24" :md="6" :lg="6" :xl="6">
        <el-card shadow="hover" class="chart-card">
          <Department />
        </el-card>
    </el-col>
      <el-col :xs="24" :sm="24" :md="18" :lg="18" :xl="18">
        <el-card shadow="hover" class="chart-card">
          <Organization />
        </el-card>
    </el-col>
  </el-row>
</div>
</template>

<script setup>
import { Department, Employee, Organization, Emailrel } from '@/views/dashboard/components'
import { Departmentcloudword } from '@/views/department/components'
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 0;
  
  .alert-card {
    margin-bottom: 20px;
    border-radius: 8px;
    
    :deep(.el-card__body) {
      padding: 15px;
    }
  }
  
  .chart-card {
    margin-bottom: 20px;
    border-radius: 8px;
    transition: all 0.3s;
    border: 1px solid #d4d4d4;
    background: #ffffff;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 20px rgba(11, 48, 66, 0.15);
      border-color: #437C8F;
    }
    
    :deep(.el-card__body) {
      padding: 20px;
    }
    
    :deep(.el-card__header) {
      background: #0B3042;
      color: #ffffff;
      border-bottom: 2px solid #437C8F;
    }
  }
  
  .content-row {
    margin-top: 20px;
    }
}
</style>
