from fastapi import FastAPI
from app.recommender import get_recommendations
import uvicorn
import os

app = FastAPI()

@app.get("/recommend")
def recommend(query: str, k: int = 5):
    return {"results": get_recommendations(query, k)}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Railway needs this!
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
