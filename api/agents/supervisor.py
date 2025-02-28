from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent
from langchain import hub
from .checkpoint import get_connection_pool, initialize_store_and_checkpointer


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
  pool = await get_connection_pool()
  store, checkpointer = await initialize_store_and_checkpointer(pool)
  # Compile and run
  scrum_master = workflow.compile(store=store, checkpointer=checkpointer)
  return scrum_master
