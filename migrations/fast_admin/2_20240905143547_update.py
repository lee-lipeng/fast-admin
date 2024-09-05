from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "logs" ADD "thread_id" INT;
        ALTER TABLE "logs" ADD "process_id" INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "logs" DROP COLUMN "thread_id";
        ALTER TABLE "logs" DROP COLUMN "process_id";"""
