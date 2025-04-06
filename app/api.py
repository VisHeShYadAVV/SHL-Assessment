from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.recommender import get_recommendations

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SHL  API is working"}

class QueryInput(BaseModel):
    query: str
    k: int 

@app.get("/recommend")
def recommend(query: str, k: int):
    try:
        if k < 1 or k > 8:  
            raise HTTPException(status_code=400, detail="Number of recommendations must be between 1 and 8")

        df = get_recommendations(query)  

        if df.empty:
            raise HTTPException(status_code=404, detail="No relevant assessments found")

        recommendations = df.head(k).to_dict(orient="records")  
        return recommendations
    except Exception as e:
        print(f"Error: {e}")  
        raise HTTPException(status_code=500, detail=str(e))
