from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from langgraph_api.lifespan import lifespan
from langgraph_api.api import routes as langgraph_routers


# ✅ Create FastAPI app
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json", lifespan=lifespan)
# ✅ Add CORS middleware

# ✅ Debugging: Print all registered assistant routes
print("📌 Final registered Assistant routes in FastAPI:")
for route in langgraph_routers:
    if route.path in ("/docs", "/openapi.json"):
        app.router.routes.insert(0, route)
    else:
        app.router.routes.append(route)

print("🚀 FastAPI Server with Custom Assistant Routes is ready!")

@app.get("/api/py/prompt-optimizer")
async def hello_fast_api():
    return { "value": "hello fast api" }