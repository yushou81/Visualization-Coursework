import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import HomeView from '@/views/HomeView.vue'
import DashboardView from '@/views/dashboard/DashboardView.vue'
import DepartmentView from '@/views/department/DepartmentView.vue'
import PersonalView from '@/views/personal/PersonalView.vue'
import BaseLayout from '@/layouts/BaseLayout.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: BaseLayout,
    children: [
      {
        path: '',
        redirect: '/dashboard'
      },
      {
        path: 'dashboard',
        name: 'dashboard',
        component: DashboardView,
        meta: { title: 'Dashboard', icon: 'example' }
      },
      {
        path: 'example/personal',
        name: 'personal',
        component: PersonalView,
        meta: { title: '个人', icon: 'user' }
      },
      {
        path: 'example/department',
        name: 'department',
        component: DepartmentView,
        meta: { title: '部门', icon: 'tree' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to, _from, next) => {
  NProgress.start()
  document.title = to.meta.title ? String(to.meta.title) : 'Visual Vue3'
  next()
})

router.afterEach(() => {
  NProgress.done()
})

export default router
