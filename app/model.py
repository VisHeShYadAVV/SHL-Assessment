import google.generativeai as genai
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

class AssessmentResponse(BaseModel):
    assessment_name: str
    url: str
    description: str
    duration: str
    remote_testing_support: str
    adaptive_irt_support: str
    score: float
    
    class Config:
        orm_mode = True

class SHLMODEL:

    def __init__(self, dataframe):
        self.df = dataframe.fillna("")  
        fields = ["Name", "Description", "Duration", "Remote Testing Support", "Adaptive Support"]
        self.df["combined"] = self.df[fields].astype(str).agg("".join, axis=1)

        self.vectorizer = TfidfVectorizer()
        self.vectors = self.vectorizer.fit_transform(self.df["combined"])

    def enhance_query(self, user_input):
        """
        Enhance the input query to make it more meaningful for search using Generative AI model.
        """
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Enhance this query to make it more meaningful for search: {user_input}"
        
        try:
            response = model.generate_content(prompt)
            
            if isinstance(response, str):
                return response.strip()
            elif hasattr(response, 'text'):
                return response.text.strip()
            else:
                return str(response).strip()
        except Exception as e:
            print(f"Error in enhance_query: {e}")
            return user_input  

    def summarize_assessment(self, full_text):
        """
        Summarize the assessment details using Generative AI model.
        """
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Summarize the following assessment details: {full_text}"
        
        try:
            response = model.generate_content(prompt)
            
            if isinstance(response, str):
                return response.strip()
            elif hasattr(response, 'text'):
                return response.text.strip()
            else:
                return str(response).strip()
        except Exception as e:
            print(f"Error in summarize_assessment: {e}")
            return full_text  
    def getTopAssessments(self, user_query, k=5):
        """
        Get the top k assessments based on the user query.
        """
        better_query = self.enhance_query(user_query)
        query_vector = self.vectorizer.transform([better_query])

        scores = cosine_similarity(query_vector, self.vectors).flatten()
        self.df["score"] = scores
        top_results = self.df.nlargest(k, "score").copy()

        top_results["summary"] = top_results["combined"].apply(self.summarize_assessment)

        assessments = [
            AssessmentResponse(
                assessment_name=row["Name"],
                url=row["Link"],  
                description=row["Description"],
                duration=row["Duration"],
                remote_testing_support=row["Remote Testing Support"],
                adaptive_irt_support=row["Adaptive Support"],
                score=row["score"]
            )
            for index, row in top_results.iterrows()  
        ]

        return [{**assessment.dict(), 'score': str(assessment.score)} for assessment in assessments]
