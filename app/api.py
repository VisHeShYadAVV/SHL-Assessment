from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.recommender import get_recommendations

app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for simplicity, adjust for security if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for testing
@app.get("/")
def root():
    return {"message": "SHL API is working"}

# Incoming JSON must have a string (query) and an integer (k)
class QueryInput(BaseModel):
    query: str
    k: int  # Accept 'k' parameter to control the number of recommendations

# Endpoint to get recommendations based on query and k
@app.get("/recommend")
def recommend(query: str, k: int):
    try:
        # Ensure 'k' is within a valid range if needed (optional)
        if k < 1 or k > 8:  # Example validation, adjust as needed
            raise HTTPException(status_code=400, detail="Number of recommendations must be between 1 and 8")

        # Fetch recommendations
        df = get_recommendations(query)  # Assuming `get_recommendations` returns a DataFrame

        if df.empty:
            raise HTTPException(status_code=404, detail="No relevant assessments found")

        # Use 'k' to limit the number of recommendations
        recommendations = df.head(k).to_dict(orient="records")  # Adjust based on your DataFrame structure
        return recommendations
    except Exception as e:
        # Log the error (for debugging) and raise HTTPException
        print(f"Error: {e}")  # You can replace this with proper logging
        raise HTTPException(status_code=500, detail=str(e))
