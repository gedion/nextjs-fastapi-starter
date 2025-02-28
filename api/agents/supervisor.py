from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

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

# Create Scrum Master / Product Owner workflow
workflow = create_supervisor(
    [frontend_dev, backend_dev],
    model=model,
    prompt=(
        "You are a Scrum Master and Product Owner. "
        "You manage a frontend developer and a backend developer. "
        "Delegate frontend tasks (UI, styling, UX) to frontend_dev. "
        "Delegate backend tasks (API, data processing, business logic) to backend_dev. "
        "Ensure tasks are prioritized correctly and developers focus on their domain."
    )
)

# Compile and run
scrum_master = workflow.compile()
