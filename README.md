# Visual Insider Threat Toolkit

## 项目简介
- 本仓库整合了可视化前端、Flask 后端以及 Insider Threat 数据集，帮助复现 ChinaVis 2018 相关分析。
- 目录结构如下：

| 目录 | 说明 |
| --- | --- |
| `frontend/` | Vue 2 + Element UI 管理端界面（webpack 3 构建，需 Node 10.x） |
| `backend/` | Flask + MySQL API，与数据导入脚本。 |
| `InsiderThreatData/` | ITD-2018 数据集及其文档，默认未跟踪完整 CSV（体积较大）。 |

## 致谢
- 感谢 [rileycai/ChinaVisProject](https://github.com/rileycai/ChinaVisProject?tab=readme-ov-file) 提供的前端代码。
- 感谢 [imcmy/chinavis-2018](https://github.com/imcmy/chinavis-2018) 提供的后端实现与数据处理思路。
- 感谢 [csuvis/InsiderThreatData](https://github.com/csuvis/InsiderThreatData.git) 开源的 ITD-2018 数据集。

## 快速开始
1. 准备依赖：Python 3.8+、pip、MySQL 5.7/8.0、[nvm](https://github.com/nvm-sh/nvm) 与 Node.js `10.24.1`、npm 或 yarn。
2. 初始化后端（安装依赖、配置 MySQL、导入数据、运行 Flask）。
3. 初始化前端（`nvm use 10.24.1`、安装依赖、配置 `BASE_API`、运行 `npm run dev`）。

### 环境建议
- 操作系统：Linux / macOS / WSL。Windows 原生亦可，但建议使用 WSL 以获得更好的脚本兼容性。
- MySQL：创建一个空数据库（例如 `chinavis`），并为后端创建具有读写权限的用户。

## 后端（`backend/`）

### 1. 安装依赖
```bash
cd backend
python3 -m venv venv           # 可替换成 pyenv/conda
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. 配置数据库连接
- 默认的连接字符串位于 `backend/app/__init__.py:10-30`，格式为 `mysql+pymysql://用户名:密码@主机/数据库`。
- 推荐通过环境变量覆盖，避免修改源码：
  ```bash
  export CHINAVIS_DB_URI="mysql+pymysql://user:pass@127.0.0.1:3306/chinavis"
  export FLASK_APP=setup.py
  export FLASK_ENV=development   # 生产环境可设置为 production
  ```
- 若使用 Docker / 远程 MySQL，请相应修改主机与端口。

### 3. 导入数据（可选但推荐）
1. 将 `InsiderThreatData/ITD-2018 Data Set.zip` 解压到 `InsiderThreatData/ITD-2018 Data Set/`，或直接克隆原始数据仓库。
2. 运行数据导入脚本（自动处理 CSV、部门映射等）：
   ```bash
   cd backend
   source venv/bin/activate
   python scripts/import_dataset.py \
     --db-host 127.0.0.1 \
     --db-port 3306 \
     --db-user chinavis \
     --db-pass chinavis2018 \
     --db-name chinavis \
     --data-root "../InsiderThreatData/ITD-2018 Data Set"
   ```
   - 该脚本支持 `--truncate` 清空表后再导入，以及自定义 `--batch-size`。

### 4. 启动服务
```bash
cd backend
source venv/bin/activate
./run.sh                         # 默认监听 0.0.0.0:5000
# 或者手动
# flask run --host 0.0.0.0 --port 5000
```
- 生产部署可以选择 `gunicorn -w 4 'setup:create_app()'`，或使用仓库内的 `Dockerfile`/`docker-compose.yml`。

## 前端（`frontend/`）
由于依赖较老，需要 Node.js `10.24.1` 以及对应版本的 npm。

### 1. 切换 Node 版本
```bash
cd frontend
nvm install 10.24.1   # 首次使用时
nvm use 10.24.1
```

### 2. 安装依赖
```bash
npm install            # 或 yarn
```

### 3. 配置 API 地址
- 开发环境：编辑 `frontend/config/dev.env.js`，修改 `BASE_API` 为后端地址（默认 `http://127.0.0.1:5000`）。
- 生产环境：编辑 `frontend/config/prod.env.js`，将 `BASE_API` 指向上线后的后端。

### 4. 运行与构建
```bash
# 开发热更新 (默认端口 5208，会自动打开浏览器)
npm run dev

# 生成生产包，输出到 frontend/dist
npm run build
```
- 若希望由任意静态服务器托管 build 结果，请将 `dist/` 发布到 CDN / Nginx 等。

## 数据集说明
- `InsiderThreatData/` 目录仅保留必要的文档与脚本，原始 CSV / ZIP 体积较大，建议通过 `.gitignore` 排除后另行下载。
- 需要完整数据时，可直接 `git clone https://github.com/csuvis/InsiderThreatData.git`，或解压本地 ZIP。
- 导入完成后即可删除原始 CSV，以节省磁盘空间。

## 常见下一步
- 使用 `.env` 或进程管理器（如 supervisor）持久化环境变量。
- 将前端打包结果与后端 API 一并部署在同一域名，避免跨域配置。
- 按需添加单元测试 / 可观测性，以便长期维护。
