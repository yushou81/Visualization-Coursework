<template>
  <div class="department-container">
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
      <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
        <el-card shadow="hover" class="chart-card">
          <Checktime />
        </el-card>
        </el-col>
      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
        <el-card shadow="hover" class="chart-card">
          <Server />
        </el-card>
        </el-col>
      </el-row>
    
    <el-row :gutter="20" class="content-row">
      <el-col :xs="24" :sm="24" :md="10" :lg="10" :xl="10">
        <el-card shadow="hover" class="chart-card">
          <Checkdep />
        </el-card>
        </el-col>
      <el-col :xs="24" :sm="24" :md="14" :lg="14" :xl="14">
        <el-card shadow="hover" class="chart-card">
          <Tcplog />
        </el-card>
        </el-col>
      </el-row>
    
    <el-row :gutter="20" class="content-row">
      <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
        <el-card shadow="hover" class="chart-card">
          <Webclass />
        </el-card>
        </el-col>
      <el-col :xs="24" :sm="12" :md="6" :lg="6" :xl="6">
        <el-card shadow="hover" class="chart-card">
          <Playball />
        </el-card>
        </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-card shadow="hover" class="chart-card">
          <LoginError />
        </el-card>
        </el-col>
      </el-row>
    
    <el-row :gutter="20" class="content-row">
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-card shadow="hover" class="chart-card">
          <Usaupload />
        </el-card>
        </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
        <el-card shadow="hover" class="chart-card">
          <Databaseerror />
        </el-card>
        </el-col>
      </el-row>
</div>
</template>

<script setup>
import {
  Checktime,
  Server,
  Webclass,
  Tcplog,
  LoginError,
  Checkdep,
  Departmentcloudword,
  Usaupload,
  Databaseerror,
  Playball
} from '@/views/department/components'
</script>

<style lang="scss" scoped>
.department-container {
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
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    :deep(.el-card__body) {
      padding: 20px;
    }
  }
  
  .content-row {
    margin-top: 20px;
  }
}
</style>
