# filepath: /home/sid/projects/AskMyDoc/backend/main_backend.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Enable CORS for browser extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"message": "AskMyDoc API is running"}

@app.post("/api/query")
async def process_query(query: Query):
    """Simple endpoint that echoes the query"""
    print(f"Backend received: {query.query}")
    return {
        "content": f"Backend echo: {query.query}",
        "timestamp": "2023-05-23T12:00:00Z"
    }

if __name__ == "__main__":
    uvicorn.run("main_backend:app", host="0.0.0.0", port=8000, reload=True)

