import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import pinia from './store'
import './styles/index.scss'
import 'virtual:svg-icons-register'
import SvgIcon from './components/SvgIcon.vue'
import './theme/halloween' // 注册 ECharts 主题

const app = createApp(App)

app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.component('SvgIcon', SvgIcon)

app.mount('#app')
