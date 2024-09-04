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
COMMENT ON COLUMN "logs"."logger_name" IS '记录器名称';
COMMENT ON COLUMN "logs"."module" IS '模块名称';
COMMENT ON COLUMN "logs"."line_no" IS '行号';
COMMENT ON COLUMN "logs"."function_name" IS '函数名称';
COMMENT ON COLUMN "logs"."exception" IS '异常信息';
COMMENT ON TABLE "logs" IS '日志模型';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "logs";"""
