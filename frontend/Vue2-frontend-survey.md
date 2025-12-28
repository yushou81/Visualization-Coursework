# Vue2 前端现状调研（基础盘点）

面向后续 Vue3/Vite 重构的现状记录，便于分工和兼容性评估。文件/路径均相对 `frontend/` 目录。

## 项目与依赖
- package.json: `vue@2.5.10`、`vue-router@3.0.1`、`vuex@3.0.1`、`element-ui@2.0.8`、`axios@0.17.1`、`echarts@4.1.0` + `echarts-wordcloud`、`js-cookie@2.2.0`、`nprogress@0.2.0`。
- 构建：webpack 3 + vue-cli 2 模板；babel6；`node-sass@4.9`。Scripts: `dev`(webpack-dev-server)、`build`、`lint`。
- 兼容要求：`engines.node >=4`（非常老）。
- 主题依赖：要求在 `node_modules/echarts/theme` 下有 `halloween.js`（同时在 `src/theme/halloween.js` 提供别名）。

## 环境/构建配置
- 环境变量：`config/dev.env.js`、`config/prod.env.js` 暴露 `BASE_API`，被 axios baseURL 使用；`NODE_ENV` 设置。
- 构建配置：`config/index.js`（dev 端口 5208，publicPath `/`；prod publicPath `./`，prod sourceMap 关）；`build/*.js` 为 webpack 配置（别名 `@` -> `src`，`echarts/theme/halloween` -> `src/theme/halloween.js`；svg-sprite-loader 仅处理 `src/icons`）。
- 入口与模板：`src/main.js` 入口，`index.html` 由 webpack 注入。

## 应用初始化
- `src/main.js`: 引入 normalize.css、全局样式 `src/styles/index.scss`；注册 ElementUI (locale=en)；挂载 router/store；加载 `@/icons`（全局 svg 精灵）与 `@/permission`（路由守卫）。
- 全局样式：SCSS，`src/styles/index.scss` 汇总 mixin/variables/sidebar/element-ui 覆盖等；全局背景图 `src/assets/pumpkin.png` 在布局中使用。
- 全局组件：`src/components/SvgIcon`（全局注册）、`src/components/ScrollBar`（自定义滚动容器）。

## 路由与权限
- 配置：`src/router/index.js`，常量路由：`/`→`/dashboard`，`/example/personal`，`/example/department`，`*`→404（404 组件缺省，依赖 vue-element-admin 模板默认行为）。
- 路由元数据用于侧边栏/图标（`meta.title`、`meta.icon`），未使用动态加载或按角色生成。
- 守卫：`src/permission.js` 使用 NProgress；若存在 token 禁止访问 `/login`，否则直接放行；无角色/菜单校验。

## 状态管理
- Vuex Store: `src/store/index.js` 引入模块 app/user 与 getters。
- 模块 app (`src/store/modules/app.js`): 侧边栏开关，状态保存在 `js-cookie`（`sidebarStatus`）。
- 模块 user (`src/store/modules/user.js`): token/name/avatar/roles；动作 `Login/GetInfo/LogOut/FedLogOut` 调用 `src/api/login.js`；未启用 namespace 或持久化。
- Getters: `sidebar/token/avatar/name/roles` (`src/store/getters.js`)。

## 网络层
- Axios 封装：`src/utils/request.js`，baseURL=`process.env.BASE_API`，timeout 15000；空的 request 拦截器；response 错误使用 Element Message；未统一错误码处理。
- API 模块：
  - `src/api/login.js`: `login/getInfo/logout`。
  - `src/api/table.js`: `getList(id)`（GET `/`）。
  - `src/api/form.js`: `getChart(params)`（GET `form/chart`）。
- 鉴权：`src/utils/auth.js` 通过 Cookie 读写 `Admin-Token`。

## UI 组件与布局
- UI 库：Element UI 2.0.8；导航/侧边栏/面包屑封装在 `src/views/layout/*`。
- 侧边栏：`Sidebar/index.vue` 使用 `el-menu` + `ScrollBar`；菜单源于 `this.$router.options.routes`。
- 导航栏：`Navbar.vue` 包含 hamburger、breadcrumb（头像下拉被注释）。
- 全局 SVG 图标：`src/icons/index.js` 加载 `src/icons/svg/*.svg`。

## 视图与业务模块
- Dashboard：`src/views/dashboard/index.vue`，组合组件 `Department/Employee/Organization/Emailrel` 等（`src/views/dashboard/components`），依赖 ECharts。
- Department：`src/views/department/index.vue`，组合多个 ECharts 组件（词云、折线、柱状等）与 `echarts-wordcloud`、`halloween` 主题；数据主要为内置配置。
- Personal：`src/views/personal/index.vue`，通过输入 id 调用 REST（`request.get('/<id>')`），根据返回数据绘制多图表；空数据/异常会显示 warning。
- 基础组件索引：`src/views/department/components/index.js`、`src/views/dashboard/components/index.js` 统一导出。

## 样式体系
- 预处理：SCSS；`src/styles/mixin.scss` 提供 clearfix/scrollBar/relative 等；`variables.scss` 定义主题色、侧边栏背景等；`element-ui.scss` 做局部覆盖；`transition.scss` 动画。
- 布局背景：`src/views/layout/Layout.vue` 使用 `@include clearfix;` 和背景图。

## 测试与质量
- 未见 test 目录或单测/e2e 配置；ESLint 规则存在但在 webpack base 中被注释（`createLintingRule` 未启用）；无 CI 配置。

## 兼容性与迁移风险（Vue3/Vite 视角）
- 核心库需替换：Vue2 → Vue3；Vue Router 3 → 4（路由实例/守卫签名变更）；Vuex 3 → Pinia 或 Vuex4；Element UI → Element Plus。
- 构建链：webpack3/babel6/node-sass4 与现代依赖不兼容，需换 Vite+TS/babel7+sass；环境变量、别名、svg-sprite 需重写。
- 图表：ECharts 4 + echarts-wordcloud 需确认在 Vite/Vue3 下的兼容性，可能需升级到 ECharts 5 和新版词云插件。
- 全局行为：当前无 filters/自定义指令/事件总线，但有大量直接 DOM 查询 `document.getElementById` 初始化 ECharts，迁移时需改为 `ref` + 组合式生命周期。
- 权限逻辑：仅基于 token 是否存在，未做角色/菜单校验；迁移可顺便重构。
- 主题依赖：`halloween.js` 主题依赖硬编码路径，需在新构建链中重新引入。

## 可参考的后续行动
- 确认第三方库的 Vue3 兼容版本（Element Plus、Vue-ECharts@next 或 echarts-for-vue、axios 新版、js-cookie、nprogress 等）。
- 将本文件补充上：组件/页面迁移优先级、依赖兼容性矩阵、已知技术债列表，以指导分工。

## 依赖兼容矩阵（Vue2 → Vue3/Vite）
- Vue 2.5.10 → Vue 3.x（选择 `vue@^3`）。
- Vue Router 3.0.1 → Vue Router 4.x。
- Vuex 3.0.1 → Pinia（推荐）或 Vuex 4.x。
- Element UI 2.0.8 → Element Plus 2.x。
- ECharts 4.1.0 + echarts-wordcloud → ECharts 5.x + `echarts-wordcloud` 兼容包（确认 Vite 支持），或使用 Vue-ECharts@next / echarts-for-vue@next 作为封装。
- axios 0.17.1 → axios 1.x。
- js-cookie 2.2.0 → js-cookie 3.x。
- nprogress 0.2.0 → nprogress 最新版。
- normalize.css 7.0.0 → normalize.css 最新版或 postcss-normalize。
- svg-sprite-loader（webpack）→ Vite 用 `vite-plugin-svg-icons` 或 `unplugin-icons`；若用 Vue-ECharts 封装可直接引入 svg 文件。
- node-sass 4.9 → sass (dart-sass) 最新版。
- webpack 3 / babel6 / vue-loader 13 → Vite + esbuild + babel7（如需要）。
- 其他：postcss 系列、sass-loader/less-loader 等均需升级到 Vite 兼容版本。

## 页面/组件迁移优先级（核心 → 次要）
1) 全局框架：布局/导航/侧边栏/面包屑、路由守卫、SVG 图标方案、HTTP 封装、状态管理（必须优先）。
2) Dashboard 模块（核心展示路径）：`views/dashboard` 及子组件（Department/Employee/Organization/Emailrel）。
3) Department 模块：`views/department` 及子组件（词云、打卡、服务器、登录异常等）。
4) Personal 模块：`views/personal`（依赖后端接口/Mock，包含多图表）。
5) 其他：通用组件（ScrollBar、SvgIcon）在 Vite 环境重写后复用；样式/主题调整。

备注：迁移图表时优先改为 `ref` + 组合式生命周期，确认 wordcloud 主题加载方式；Personal 如后端缺失需先用 mock 数据占位。
