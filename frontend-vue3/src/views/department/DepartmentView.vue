<template>
  <div class="dashboard-container">
    <el-row style="margin: 10px 0">
      <el-alert
        title="提示：点击员工节点可显示该员工的邮件收发词云图信息"
        type="warning"
        center
        show-icon
      />
    </el-row>
    <Departmentcloudword />
    <el-row style="margin-top: 10px">
      <el-col :span="16">
        <Checktime />
      </el-col>
      <el-col :span="8">
        <Server />
      </el-col>
    </el-row>
    <el-row style="margin-top: 10px">
      <el-col :span="10">
        <Checkdep />
      </el-col>
      <el-col :span="14">
        <Tcplog />
      </el-col>
    </el-row>
    <el-row style="margin-top: 10px">
      <el-col :span="6">
        <Webclass />
      </el-col>
      <el-col :span="6" style="padding-right: 10px">
        <Playball />
      </el-col>
      <el-col :span="12">
        <LoginError />
      </el-col>
    </el-row>
    <el-row style="margin-top: 10px">
      <el-col :span="12" style="padding-right: 10px">
        <Usaupload />
      </el-col>
      <el-col :span="12" style="padding-right: 10px">
        <Databaseerror />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
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

<style scoped>
.dashboard-container {
  margin: 10px 10px 10px -20px;
}
.chartBox {
  width: 100%;
  border: #ccc 1px solid;
  margin: 0 10px;
}
</style>
