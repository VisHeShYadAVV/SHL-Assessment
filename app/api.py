from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.recommender import get_recommendations
import uvicorn
import os

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello from Vishesh's backend"}

class QueryInput(BaseModel):
    query: str
    k: int 

@app.get("/recommend")
def recommend(query: str, k: int = 5):
    try:
        if k < 1 or k > 8:
            raise HTTPException(status_code=400, detail="Number of recommendations must be between 1 and 8")

        recommendations = get_recommendations(query, k)

        if not recommendations:
            raise HTTPException(status_code=404, detail="No relevant assessments found")

        return recommendations
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.api:app", host="0.0.0.0", port=port, reload=True)
