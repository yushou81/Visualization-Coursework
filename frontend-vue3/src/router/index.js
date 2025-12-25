import { createRouter, createWebHistory } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import DashboardView from '@/views/DashboardView.vue'
import AboutView from '@/views/AboutView.vue'
import PersonalView from '@/views/PersonalView.vue'
import DepartmentView from '@/views/DepartmentView.vue'
import ChartsDemoView from '@/views/ChartsDemoView.vue'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: '',
          name: 'dashboard',
          component: DashboardView,
          meta: { title: '仪表盘' }
        },
        {
          path: 'personal',
          name: 'personal',
          component: PersonalView,
          meta: { title: '个人' }
        },
        {
          path: 'department',
          name: 'department',
          component: DepartmentView,
          meta: { title: '部门' }
        },
        {
          path: 'charts-demo',
          name: 'charts-demo',
          component: ChartsDemoView,
          meta: { title: '图表示例' }
        }
      ]
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    }
  ],
  scrollBehavior: () => ({ left: 0, top: 0 })
})

export default router
