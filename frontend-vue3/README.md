# Visual Vue3 基线

基于 Vite + Vue 3 + TypeScript + Element Plus + Pinia + ECharts5 的重构起步工程。

## 开发命令
- 安装依赖：`npm install`
- 本地开发：`npm run dev`
- 打包构建：`npm run build`
- 预览构建产物：`npm run preview`

## 环境变量
复制 `.env.example` 到 `.env` 并按需调整：
```
VITE_APP_TITLE=Visual Vue3
VITE_BASE_API=http://localhost:5000
```

## 结构说明
- `src/main.ts`：入口，注册 Pinia、Router、Element Plus。
- `src/router`：Vue Router 4 配置。
- `src/stores`：Pinia 示例。
- `src/utils`：request（axios 封装）。
- `src/components`：示例组件（计数卡片、ECharts 折线图）、SvgIcon、ScrollBar、Breadcrumb。
- `src/icons/svg`：SVG 雪碧图方案（vite-plugin-svg-icons）。
- `src/layouts`：BaseLayout + Navbar/Sidebar 组合。
- 视图：`src/views/HomeView.vue`（欢迎页）、`src/views/dashboard/`、`src/views/department/`、`src/views/personal/`（占位待迁移）。
- `src/styles/index.scss`：全局样式与 Element Plus 主题引入。

## 下一步可做
- 按需扩展路由守卫与菜单生成（如有权限需求）。
- 搭建 axios 拦截器细节与接口类型。
- 迁移旧项目的页面和图表逻辑，逐步替换示例组件。
