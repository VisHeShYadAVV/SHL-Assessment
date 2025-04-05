import google.generativeai as genai
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Set up the API key for Gemini
genai.configure(api_key="AIzaSyBJSd7iZDT8QvOULp7j9FIMSDJMu5OoB3o")

class SHLMODEL:

    def __init__(self,dataframe):
        
        self.df = dataframe.fillna("")  
# combine text to fields to prepare for search
        fields=["Name", "Description", "Duration", "Remote Testing Support", "Adaptive Support"]
        self.df["combined"] = self.df[fields].astype(str).agg("".join,axis=1)
        
        self.vectorizer = TfidfVectorizer()
        self.vectors = self.vectorizer.fit_transform(self.df["combined"])
        

    # Use Gemini to rewrite the user input in a cleaner form 
    
    def enhance_query(self, user_input):
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Enhance this query to make it more meaningful for search: {user_input}"
        response = model.generate_content(prompt)
        return response.text.strip()

    # use gemini to make summary for assessment

    def summarize_assessment(self, full_text):
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Summarize the following assessment details: {full_text}"
        response = model.generate_content(prompt)
        return response.text.strip()

    def getTopAssessments(self, user_query, k=5):
        # Improve the query with Gemini
        better_query = self.enhance_query(user_query)
        # Convert the query to a TF-IDF vector
        query_vector = self.vectorizer.transform([better_query])

        # Measure similarity between query and all assessments
        scores = cosine_similarity(query_vector, self.vectors).flatten()
        self.df["score"] = scores

        # Pick top k recommendeation
        top_results = self.df.nlargest(k, "score").copy()
        top_results["summary"] = top_results["combined"].apply(self.summarize_assessment)
        
        return top_results[["Name", "summary", "score"]]
