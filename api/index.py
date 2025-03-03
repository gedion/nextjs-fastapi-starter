from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langgraph_api.lifespan import lifespan
from langgraph_api.api import routes as langgraph_routers


# ✅ Create FastAPI app
app = FastAPI(lifespan=lifespan)

# ✅ Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# ✅ Debugging: Print all registered assistant routes
print("📌 Final registered Assistant routes in FastAPI:")
for route in langgraph_routers:
    if route.path in ("/docs", "/openapi.json"):
        app.router.routes.insert(0, route)
    else:
        app.router.routes.append(route)

print("🚀 FastAPI Server with Custom Assistant Routes is ready!")
