<template>
  <div class="dashboard-container">
    <el-row style="margin: 10px 0">
      <el-alert title="提示：点击员工节点可显示该员工的邮件收发词云图信息" type="warning" center show-icon />
    </el-row>
    <Departmentcloudword />
    <el-row style="margin-top: 10px">
      <el-col :span="6">
        <el-row>
          <Department />
        </el-row>
      </el-col>
      <el-col :span="18" style="padding-right: 10px">
        <Organization />
      </el-col>
    </el-row>
    <el-row style="margin-top: 10px">
      <el-col :span="12">
        <Employee />
      </el-col>
      <el-col :span="12" style="padding-right: 10px">
        <Emailrel />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { Department, Employee, Organization, Emailrel } from '@/views/dashboard/components'
import { Departmentcloudword } from '@/views/department/components'
</script>

<style scoped>
.dashboard-container {
  margin: 10px 10px 10px -20px;
}
</style>
