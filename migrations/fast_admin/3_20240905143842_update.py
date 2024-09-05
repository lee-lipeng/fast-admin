from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "logs" ADD "process" VARCHAR(255);
        ALTER TABLE "logs" ADD "thread" VARCHAR(255);
        ALTER TABLE "logs" DROP COLUMN "process_id";
        ALTER TABLE "logs" DROP COLUMN "thread_id";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "logs" ADD "process_id" INT;
        ALTER TABLE "logs" ADD "thread_id" INT;
        ALTER TABLE "logs" DROP COLUMN "process";
        ALTER TABLE "logs" DROP COLUMN "thread";"""
