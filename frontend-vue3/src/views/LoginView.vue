<template>
  <div class="login">
    <el-card class="panel" shadow="hover">
      <h2>登录</h2>
      <el-form @submit.prevent="onSubmit" label-position="top">
        <el-form-item label="Token">
          <el-input v-model="token" placeholder="请输入模拟 Token，真实接入请替换接口" />
        </el-form-item>
        <el-button type="primary" native-type="submit" block>保存并进入</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { setToken } from '@/utils/auth'

const token = ref('')
const router = useRouter()

const onSubmit = () => {
  if (!token.value) return
  setToken(token.value)
  router.push('/')
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  padding: 20px;
}

.panel {
  width: min(420px, 100%);
}
</style>
