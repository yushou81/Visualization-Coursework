<template>
  <div v-if="!item.hidden">
    <template v-if="onlyOneChild && hasOneShowingChild(item.children, item) && (!onlyOneChild.children || onlyOneChild.noShowingChildren) && !item.alwaysShow">
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

    <el-submenu v-else :index="resolvePath(item.path)">
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
    </el-submenu>
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
