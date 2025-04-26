from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Union
from app.model import SHLMODEL
import pandas as pd

df = pd.read_csv("shl_real_assessments.csv")

model = SHLMODEL(df)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the SHL Assessment Recommendation API!"}

@app.get("/recommend", response_model=Union[List[Dict[str, str]], Dict[str, str]])
def recommend(query: str = Query(...), k: int = Query(5, ge=1, le=8)):
    """
    Returns the top k relevant SHL assessments based on the provided query.
    """
    try:
        results = model.getTopAssessments(query, k)

        if not results:
            raise HTTPException(status_code=404, detail="No relevant assessments found.")

        response = [
            {
                "assessment_name": result["assessment_name"],
                "url": result["url"],
                "description": result["description"],
                "duration": result["duration"],
                "remote_testing_support": result["remote_testing_support"],
                "adaptive_irt_support": result["adaptive_irt_support"],
                "score": str(result["score"])
            }
            for result in results
        ]
        return response

    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
