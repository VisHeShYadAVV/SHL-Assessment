from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.recommender import get_recommendations

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
def root():
    return {"message": "Hello from Vishesh’s SHL backend"}

# Input model
class QueryInput(BaseModel):
    query: str
    k: int

# Main recommendation route
@app.get("/recommend")
def recommend(query: str, k: int):
    try:
        if k < 1 or k > 8:
            raise HTTPException(status_code=400, detail="k must be between 1 and 8")

        results = get_recommendations(query, k)

        if not results:
            raise HTTPException(status_code=404, detail="No relevant assessments found")

        return results

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
