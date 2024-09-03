

# fast-admin

本项目是一个基于 FastAPI 框架、Tortoise-ORM 和 PostgreSQL 数据库构建的开源角色权限管理系统，旨在提供一个灵活、安全、易于扩展的权限管理解决方案。

## 核心特性

* **基于角色的访问控制 (RBAC):**  fast-admin 采用 RBAC 模型，可以精细地控制用户对系统资源的访问权限，确保数据安全。
* **用户管理:**  支持用户注册、登录、密码修改、角色分配等功能。
* **角色管理:**  支持自定义角色，并可以为角色分配不同的权限。
* **权限管理:**  支持定义权限，并将权限分配给角色。
* **API 路由:**  使用 FastAPI 设计 API 路由，提供清晰、易于扩展的 API 接口。
* **用户行为审计:**  记录用户的所有关键操作，用于审计和追踪。
* **数据库迁移:**  使用 Aerich 管理数据库迁移，方便数据库 schema 的更新。
* **JWT 认证:**  使用 JWT 进行用户认证，确保 API 安全。
* **异步数据库操作:**  使用 Tortoise-ORM 进行异步数据库操作，提高系统性能。
* **缓存机制:**  使用 Redis 缓存常用数据，提升系统响应速度。
* **分页功能:**  支持对查询结果进行分页，方便处理大量数据。
* **全局异常处理:**  提供全局异常处理机制，增强系统鲁棒性。
* **系统日志管理:**  将系统日志存储在 PostgreSQL 数据库中，并提供日志查询和分析接口。

## 技术栈

* **FastAPI:**  高性能 Web 框架。
* **Tortoise-ORM:**  异步 ORM 框架。
* **PostgreSQL:**  关系型数据库。
* **Aerich:**  数据库迁移工具。
* **Redis:**  缓存数据库。
* **JWT:**  JSON Web Token，用于用户认证。
* **PDM:**  Python 包管理工具。


## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/lee-lipeng/fast-admin.git
cd fast-admin
```

### 2. 安装依赖

```bash
pdm install
```

### 3. Aerich初始化

```bash
aerich init -t fast_admin.core.config.TORTOISE_ORM
aerich init-db
```

### 4. 启动项目

```bash
pdm run fast_admin
```
