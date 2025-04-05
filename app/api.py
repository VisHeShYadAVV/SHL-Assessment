from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.recommender import get_recommendations


app=FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "SHL API is working"}

# incoming JSON must have a string
class QueryInput(BaseModel):
    query: str


@app.post("/recommend")

# POST API
def recommend(input:QueryInput):
    try:
        df=get_recommendations(input.query)
        if(df.empty):
            raise HTTPException(status_code=404,detail="No relevant assessments found")
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))