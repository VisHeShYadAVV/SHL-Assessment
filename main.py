from app.api import app
from fastapi import FastAPI
from app.recommender import get_recommendations

app = FastAPI()

@app.get("/recommend")
def recommend(query: str, k: int = 5):
    return get_recommendations(query, k)
