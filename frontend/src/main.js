import { createApp } from 'vue'
import 'normalize.css/normalize.css'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

import '@/styles/index.scss'
import '@/theme/halloween'

import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

import '@/icons'
import '@/permission'

const app = createApp(App)
const pinia = createPinia()

// Register all Element Plus icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus, {
  locale: zhCn
})
app.use(pinia)
app.use(router)

app.mount('#app')
