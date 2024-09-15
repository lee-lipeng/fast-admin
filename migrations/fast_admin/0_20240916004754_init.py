from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "logs" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "level" VARCHAR(20) NOT NULL,
    "message" TEXT NOT NULL,
    "timestamp" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "process" VARCHAR(255),
    "thread" VARCHAR(255),
    "logger_name" VARCHAR(255),
    "module" VARCHAR(255),
    "line_no" INT,
    "function_name" VARCHAR(255),
    "exception" TEXT
);
COMMENT ON COLUMN "logs"."created_at" IS '创建时间';
COMMENT ON COLUMN "logs"."updated_at" IS '更新时间';
COMMENT ON COLUMN "logs"."id" IS '日志ID';
COMMENT ON COLUMN "logs"."level" IS '日志级别';
COMMENT ON COLUMN "logs"."message" IS '日志消息';
COMMENT ON COLUMN "logs"."timestamp" IS '时间戳';
COMMENT ON COLUMN "logs"."process" IS '进程信息';
COMMENT ON COLUMN "logs"."thread" IS '线程信息';
COMMENT ON COLUMN "logs"."logger_name" IS '记录器名称';
COMMENT ON COLUMN "logs"."module" IS '模块名称';
COMMENT ON COLUMN "logs"."line_no" IS '行号';
COMMENT ON COLUMN "logs"."function_name" IS '函数名称';
COMMENT ON COLUMN "logs"."exception" IS '异常信息';
COMMENT ON TABLE "logs" IS '日志模型';
CREATE TABLE IF NOT EXISTS "permission" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "code" VARCHAR(255) NOT NULL UNIQUE,
    "type" VARCHAR(20) NOT NULL,
    "description" TEXT
);
COMMENT ON COLUMN "permission"."created_at" IS '创建时间';
COMMENT ON COLUMN "permission"."updated_at" IS '更新时间';
COMMENT ON COLUMN "permission"."id" IS '权限ID';
COMMENT ON COLUMN "permission"."name" IS '权限名称';
COMMENT ON COLUMN "permission"."code" IS '权限代码';
COMMENT ON COLUMN "permission"."type" IS '权限类型';
COMMENT ON TABLE "permission" IS '权限模型';
CREATE TABLE IF NOT EXISTS "role" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    "description" TEXT
);
COMMENT ON COLUMN "role"."created_at" IS '创建时间';
COMMENT ON COLUMN "role"."updated_at" IS '更新时间';
COMMENT ON COLUMN "role"."id" IS '角色ID';
COMMENT ON COLUMN "role"."name" IS '角色名称';
COMMENT ON COLUMN "role"."description" IS '角色描述';
COMMENT ON TABLE "role" IS '角色模型';
CREATE TABLE IF NOT EXISTS "user" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False
);
COMMENT ON COLUMN "user"."created_at" IS '创建时间';
COMMENT ON COLUMN "user"."updated_at" IS '更新时间';
COMMENT ON COLUMN "user"."id" IS '用户ID';
COMMENT ON COLUMN "user"."username" IS '用户名';
COMMENT ON COLUMN "user"."password_hash" IS '密码哈希值';
COMMENT ON COLUMN "user"."is_active" IS '用户是否激活';
COMMENT ON COLUMN "user"."is_superuser" IS '是否是超级管理员权限';
COMMENT ON TABLE "user" IS '用户模型';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "role_permission" (
    "role_id" INT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE,
    "permission_id" INT NOT NULL REFERENCES "permission" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "role_permission" IS '角色拥有的权限';
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_role_permis_role_id_7454bb" ON "role_permission" ("role_id", "permission_id");
CREATE TABLE IF NOT EXISTS "user_role" (
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "role_id" INT NOT NULL REFERENCES "role" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "user_role" IS '用户拥有的角色';
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_user_role_user_id_d0bad3" ON "user_role" ("user_id", "role_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
