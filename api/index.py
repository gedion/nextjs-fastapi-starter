from dotenv import load_dotenv
import os
load_dotenv()  # take environment variables from .env.

from fastapi import FastAPI
from .agents.supervisor import scrum_master 


print(os.getenv('OPENAI_API_KEY'))
### Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/py/docs", openapi_url="/api/py/openapi.json")

@app.get("/api/py/helloFastApi")
def hello_fast_api():
    result = scrum_master.invoke({
        "messages": [
            {
                "role": "user",
                "content": "Discuss a potential ai based application for gardening simulator"
            }
        ]
    })
    return result