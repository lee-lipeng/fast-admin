# fast-admin

本项目是一个基于 FastAPI 框架、Tortoise-ORM 和 PostgreSQL 数据库构建的一个基础权限管理系统。


## 技术栈

- **FastAPI:** 高性能 Web 框架。
- **Tortoise-ORM:** 异步 ORM 框架。
- **PostgreSQL:** 关系型数据库。
- **Aerich:** 数据库迁移工具。
- **JWT:** JSON Web Token，用于用户认证。
- **PDM:** Python 包管理工具。

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/lee-lipeng/fast-admin.git
cd fast-admin
```

### 2. 环境配置

复制环境变量示例文件并根据实际情况修改：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库连接信息：

```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=your-password
DATABASE_NAME=fast_admin
```

### 3. 安装依赖

```bash
pdm install
```

### 4. 数据库初始化

```bash
# 初始化 Aerich
aerich init -t fast_admin.core.config.TORTOISE_ORM

# 初始化数据库
aerich init-db
```

### 5. 启动项目

```bash
pdm run fast_admin
```

项目启动后，访问以下地址：

- API 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc
