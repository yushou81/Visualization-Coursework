# Vue3 重构行动计划（含分工）

目标：将现有 Vue2 + webpack3 前端迁移到 Vue3 + Vite + TS，并保留主要业务功能。团队成员：陈起刚、邱宇轩、石文翔、赵洋毅。

## 阶段与任务

### 阶段 1：补充现状文档（~0.5 天）
- 补充 `frontend/Vue2-frontend-survey.md`：
  - 依赖兼容矩阵（旧库 → Vue3/Vite 对应版本/替代）：陈起刚负责，石文翔校对。
  - 页面/组件迁移优先级清单（核心→次要）：邱宇轩负责，赵洋毅校对。

### 阶段 2：确定新技术栈与规范（~0.5 天）
- 选型：Vite + Vue3 + TypeScript、Vue Router 4、Pinia、Element Plus、ECharts 5 + wordcloud 插件、axios 1.x、js-cookie、nprogress。
- 规范：目录/别名、环境变量命名、ESLint+Prettier+Stylelint、提交规范（Husky+lint-staged）、测试基线（Vitest + 可选 Cypress/Playwright）。
- 负责人：陈起刚（主导），石文翔评审。

### 阶段 3：搭建 Vue3 基线工程（~1 天）
- 在新目录 `frontend-vue3` 初始化 Vite vue-ts 模板。
- 配置：路径别名、环境变量示例、全局样式入口、ESLint/Prettier/Stylelint、Husky+lint-staged、Vitest（+e2e 占位）、TS 严格模式。
- 接入：Router4、Pinia、Element Plus、ECharts5（含 wordcloud），提供 1-2 个示例页（布局+表单+图表，使用 `<script setup>` 和组合式 API）。
- 负责人：陈起刚执行，石文翔评审。

### 阶段 4：迁移共通层（~1 天）
- 工具/网络：迁移 `src/utils`（时间/校验等）、重写 axios 封装（拦截器、错误提示、token 注入预留）。
- 框架：重建布局/导航/侧边栏/面包屑；路由守卫（NProgress + token/角色占位）；SVG 图标方案（Vite svg sprite 或 iconify）。
- 负责人：石文翔主导，赵洋毅协作。

### 阶段 5：业务模块分批迁移（~2–3 天，可并行）
- 邱宇轩：Dashboard 及子组件（Department/Employee/Organization/Emailrel 等），将 DOM 初始化图表改为 `ref` + `onMounted`，适配 ECharts5。
- 赵洋毅：Department 页面及子组件（词云/折线/柱状），确认 wordcloud 兼容与主题引入方式。
- 石文翔：Personal 页面（请求接口 + 多图表），处理空态/错误，必要时引入 mock。
- 陈起刚：维护路由表/菜单与权限逻辑，抽象角色/菜单占位，全局样式/主题 token。

### 阶段 6：验证与优化（~0.5 天）
- 跑 lint/test/build，修复类型与构建问题。
- 核查功能与数据渲染；记录残留问题。
- 评估打包体积/性能（Vite build 报告）。

### 阶段 7：交付与文档（~0.5 天）
- 在调研文档末尾追加迁移进度、已知问题、后续待办。
- 输出 README：环境变量、启动/构建命令、约定与分工、示例页说明。

## 近期待办（可立即执行）
1) 在 `Vue2-frontend-survey.md` 补兼容矩阵与迁移优先级清单（陈起刚、邱宇轩先动手）。  
2) 初始化 `frontend-vue3` Vite 工程并提交基础配置（陈起刚）。  
3) 石文翔起草 axios 封装与路由守卫方案；赵洋毅确认 wordcloud/ECharts5 兼容包。  
4) 每人认领的页面模块列出待迁移点与数据依赖，记录到调研文档附录。
