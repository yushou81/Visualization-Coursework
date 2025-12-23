<template>
  <el-breadcrumb class="app-breadcrumb" separator="/">
    <transition-group name="breadcrumb">
      <el-breadcrumb-item 
        v-for="(item, index) in levelList" 
        :key="item.path"
        v-show="item.meta && item.meta.title"
      >
        <span 
          v-if="item.redirect === 'noredirect' || index === levelList.length - 1" 
          class="no-redirect"
        >
          {{ item.meta.title }}
        </span>
        <router-link v-else :to="item.redirect || item.path">
          {{ item.meta.title }}
        </router-link>
      </el-breadcrumb-item>
    </transition-group>
  </el-breadcrumb>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const levelList = ref([])

const getBreadcrumb = () => {
  let matched = route.matched.filter(item => item.name)
      const first = matched[0]
  if (first && first.name !== 'Dashboard') {
    matched = [{ path: '/dashboard', meta: { title: '主页' } }].concat(matched)
      }
  levelList.value = matched
    }

getBreadcrumb()

watch(() => route.path, () => {
  getBreadcrumb()
})
</script>

<style lang="scss" scoped>
.app-breadcrumb {
    display: inline-block;
    font-size: 14px;
  line-height: 60px;
    margin-left: 10px;
  
  :deep(.el-breadcrumb__inner) {
    color: #606266;
    font-weight: normal;
    
    &.is-link {
      color: #409eff;
      
      &:hover {
        color: #66b1ff;
      }
    }
  }
  
    .no-redirect {
    color: #606266;
      cursor: text;
    }
  }
</style>
