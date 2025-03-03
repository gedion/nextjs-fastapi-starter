from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langchain import hub
import asyncio
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


model = ChatOpenAI(model="gpt-4o-mini")

def render_ui(component: str) -> str:
    """Render a UI component for the frontend."""
    return f"Rendered UI component: {component}"

def api_request(endpoint: str) -> str:
    """Handle an API request for the backend."""
    return f"Fetched data from API endpoint: {endpoint}"

# Create specialized agents for Frontend and Backend

frontend_dev = create_react_agent(
    model=model,
    tools=[render_ui],
    name="frontend_dev",
    prompt=(
        "You are a frontend developer. "
        "Focus on UI components, styling, and user interactions. "
        "Always use one tool at a time."
    )
)

backend_dev = create_react_agent(
    model=model,
    tools=[api_request],
    name="backend_dev",
    prompt=(
        "You are a backend developer. "
        "Handle data processing, API requests, and business logic. "
        "Always use one tool at a time."
    )
)

prompt = hub.pull("scrum-master").messages[0].format()
# Create Scrum Master / Product Owner workflow
workflow = create_supervisor(
    [frontend_dev, backend_dev],
    model=model,
    prompt=prompt,
)

async def compile_workflow():
  pool = get_connection_pool()
  store, checkpointer = await initialize_store_and_checkpointer(pool)
  # Compile and run
  scrum_master = workflow.compile(store=store, checkpointer=checkpointer)
  return scrum_master

supervisor = asyncio.run(compile_workflow())