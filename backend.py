from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import json

app = FastAPI(title="AskMyDoc Backend", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QueryRequest(BaseModel):
    query: str
    page: int
    timestamp: str

# Response model
class QueryResponse(BaseModel):
    success: bool
    message: str
    receivedData: dict
    serverTimestamp: str

@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    print("\n=== NEW QUERY RECEIVED ===")
    print(f"Timestamp: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Full request data: {json.dumps(request.dict(), indent=2)}")
    
    # Extract individual fields
    query = request.query
    page = request.page
    timestamp = request.timestamp
    
    print("\n--- Parsed Data ---")
    print(f"Query: {query}")
    print(f"Page: {page}")
    print(f"Original Timestamp: {timestamp}")
    print("========================\n")
    
    # Return response
    return QueryResponse(
        success=True,
        message="Query received successfully",
        receivedData={
            "query": query,
            "page": page,
            "timestamp": timestamp
        },
        serverTimestamp=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    )

@app.get("/health")
async def health_check():
    return {
        "status": "Server is running",
        "timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 FastAPI backend starting...")
    print("📝 Ready to receive queries at http://localhost:8000/api/query")
    print("💊 Health check available at http://localhost:8000/health")
    print("📚 API docs available at http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
