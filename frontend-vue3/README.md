# Visual 前端（Vue 3 + Vite）

> 与旧版 `frontend` 完全隔离的全新脚手架，用于迁移到 Vue 3。

## 快速开始

```bash
cd frontend-vue3
npm install
npm run dev
# 浏览器访问 http://localhost:5173
```

## 技术栈
- Vue 3.4 + Vite 5
- Element Plus 2
- Vue Router 4
- Pinia 2
- Axios 1
- NProgress（路由进度条）
- ECharts 5 + echarts-wordcloud（词云）

## 当前结构
- 布局：`src/layouts/AppLayout.vue`（侧边菜单 + 顶栏）包裹仪表盘/个人/部门等子路由。
- 路由：`src/router/index.js` 已使用 Vue Router 4，包含 `/`（Dashboard）、`/personal`、`/department`、`/about`。
- 权限：`src/permission.js` 挂载 NProgress & token 检查（token 存在 `localStorage`）。
- 状态：`src/stores/app.js`（Pinia）示例，含侧边栏开关。
- 请求：`src/utils/request.js`（axios 封装，附带 token header、错误提示）。
- 视图占位：`src/views/DashboardView.vue`、`src/views/PersonalView.vue`、`src/views/DepartmentView.vue`、`src/views/AboutView.vue`。
- 图表示例：`src/views/ChartsDemoView.vue` 使用 echarts v5 + wordcloud。
- 登录占位：`src/views/LoginView.vue`，路由守卫白名单已包含 `/login`。

## 迁移建议（下一步）
1. 在 `src/styles` 补齐主题、布局配色，使 Element Plus 风格贴近旧版。
2. 把旧的登录/权限流复制到 `src/permission.js` 和 store（如需要登录页，可新增 `/login`）。
3. 按页面迁移：从布局/导航开始，逐个把旧版 `dashboard/personal/department` 逻辑（含 echarts）搬到对应视图；升级 echarts 到 v5 并验证词云插件兼容性。
4. 补充接口封装（如 `/src/api/*`），将旧请求逻辑接入 `src/utils/request.js`，保持 token/错误处理一致。
5. 完善测试：跑 `npm run lint`，并视情况补充组件测试。
