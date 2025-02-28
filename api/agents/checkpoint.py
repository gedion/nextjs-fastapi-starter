import os
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from langgraph.store.postgres.aio import AsyncPostgresStore
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

DB_URI = os.getenv(
    "POSTGRES_URL", 
    "postgres://neondb_owner:npg_1XldHyRnsA2S@ep-square-waterfall-a5r400c3-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
)

def get_connection_pool():
    pool = AsyncConnectionPool(
        DB_URI,
        max_size=20,
        open=True,
        timeout=30,
        kwargs={
            "autocommit": True,
            "row_factory": dict_row,
        }
    )
    return pool

async def initialize_store_and_checkpointer(pool):
    # Initialize AsyncPostgresStore
    store = AsyncPostgresStore(
        pool,
        index={
            "dims": 1536,
            "embed": "openai:text-embedding-3-small",
        }
    )
    await store.setup()

    # Initialize AsyncPostgresSaver for checkpointing
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup()

    return store, checkpointer
