from dotenv import load_dotenv
from typing import Optional
import os
load_dotenv()  # take environment variables from .env.

from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from .agents.supervisor import compile_workflow
from .prompts.optimizer import optimize

print(os.getenv('OPENAI_API_KEY'))
### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")


@app.get("/api/py/helloFastApi")
async def hello_fast_api(content: str = Query(...), thread_id: Optional[str] = Query(None)):
    workflow = await compile_workflow()
    config = {"configurable": {"thread_id": thread_id if thread_id else "tid-default-1"}}
    result = await workflow.ainvoke({
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]},
        config
    )
    #print(result)
    #response = StreamingResponse(result)
    #response.headers['x-vercel-ai-data-stream'] = 'v1'
    return result 

@app.get("/api/py/prompt-optimizer")
async def hello_fast_api():
    return await optimize()