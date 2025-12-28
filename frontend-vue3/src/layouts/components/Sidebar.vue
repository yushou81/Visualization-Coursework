<template>
  <div class="sidebar">
    <ScrollBar>
      <el-menu
        :default-active="activePath"
        background-color="transparent"
        text-color="#e5e7eb"
        active-text-color="#fbbf24"
        class="menu"
        router
      >
        <template v-for="route in items" :key="route.path">
          <el-menu-item :index="resolvePath(route)">
            <SvgIcon v-if="route.meta?.icon" :name="route.meta.icon as string" class="icon" />
            <span>{{ route.meta?.title || route.path }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </ScrollBar>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouteRecordRaw } from 'vue-router'
import ScrollBar from '@/components/ScrollBar.vue'

interface Props {
  items: RouteRecordRaw[]
}

defineProps<Props>()

const route = useRoute()
const activePath = computed(() => route.path)

const resolvePath = (r: RouteRecordRaw) => r.path || '/'
</script>

<style scoped>
.sidebar {
  height: 100%;
}

.menu {
  border-right: none;
}

.icon {
  margin-right: 8px;
}
</style>
