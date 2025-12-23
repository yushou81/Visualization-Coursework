<template>
  <div v-if="!item.hidden">
    <!-- 纯叶子节点，直接渲染菜单项 -->
    <template v-if="isLeaf">
      <el-menu-item 
        :index="leafIndex"
        :class="{'submenu-title-noDropdown': !isNest}"
      >
        <el-icon v-if="item.meta && item.meta.icon">
          <component :is="item.meta.icon" />
        </el-icon>
        <template #title>
          <span>{{ item.meta?.title }}</span>
        </template>
      </el-menu-item>
    </template>

    <!-- 只有一个可显示子节点时折叠为单项 -->
    <template v-else-if="onlyOneChild && hasOneShowingChild(item.children, item) && (!onlyOneChild.children || onlyOneChild.noShowingChildren) && !item.alwaysShow">
      <el-menu-item 
        :index="resolvePath(onlyOneChild.path)"
        :class="{'submenu-title-noDropdown': !isNest}"
      >
        <el-icon v-if="onlyOneChild.meta && onlyOneChild.meta.icon">
          <component :is="onlyOneChild.meta.icon" />
        </el-icon>
        <template #title>
          <span>{{ onlyOneChild.meta?.title }}</span>
        </template>
            </el-menu-item>
    </template>

    <!-- Element Plus 子菜单组件名为 el-sub-menu（中间有连字符） -->
    <el-sub-menu v-else :index="resolvePath(item.path)">
      <template #title>
        <el-icon v-if="item.meta && item.meta.icon">
          <component :is="item.meta.icon" />
        </el-icon>
        <span>{{ item.meta?.title }}</span>
      </template>
      <template v-if="item.children">
        <SidebarItem
          v-for="child in item.children"
          :key="child.path"
          :item="child"
          :base-path="resolvePath(child.path)"
          :is-nest="true"
        />
      </template>
    </el-sub-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { isExternal } from '@/utils/validate'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  basePath: {
    type: String,
    default: ''
    },
    isNest: {
      type: Boolean,
    default: false
  }
})

const onlyOneChild = computed(() => {
  if (!Array.isArray(props.item.children) || props.item.children.length === 0) {
    return null
  }
  return props.item.children[0]
})

const isLeaf = computed(() => {
  return !Array.isArray(props.item.children) || props.item.children.length === 0
})

const leafIndex = computed(() => {
  // basePath 在父级已传入完整路径，直接使用，避免重复拼接
  if (props.basePath) {
    return props.basePath
  }
  return resolvePath(props.item.path)
})

const hasOneShowingChild = (children = [], parent) => {
  if (!children || children.length === 0) {
    return false
  }
  
  const showingChildren = children.filter(item => {
    return !item.hidden
  })

  if (showingChildren.length === 1) {
    return true
  }

  return false
}

const resolvePath = (routePath) => {
  if (isExternal(routePath)) {
    return routePath
  }
  if (isExternal(props.basePath)) {
    return props.basePath
  }
  // Simple path resolution without path module
  if (routePath.startsWith('/')) {
    return routePath
  }
  const base = props.basePath.endsWith('/') ? props.basePath.slice(0, -1) : props.basePath
  return `${base}/${routePath}`.replace(/\/+/g, '/')
}
</script>
