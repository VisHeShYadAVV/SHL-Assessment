# import google.generativeai as genai
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# genai.configure(api_key="AIzaSyBJSd7iZDT8QvOULp7j9FIMSDJMu5OoB3o")

# class SHLMODEL:

#     def __init__(self,dataframe):
        
#         self.df = dataframe.fillna("")  
        
#         fields=["Name", "Description", "Duration", "Remote Testing Support", "Adaptive Support"]
#         self.df["combined"] = self.df[fields].astype(str).agg("".join,axis=1)
        
#         self.vectorizer = TfidfVectorizer()
#         self.vectors = self.vectorizer.fit_transform(self.df["combined"])
        

    
#     def enhance_query(self, user_input):
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         prompt = f"Enhance this query to make it more meaningful for search: {user_input}"
#         response = model.generate_content(prompt)
#         return response.text.strip()

#     def summarize_assessment(self, full_text):
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         prompt = f"Summarize the following assessment details: {full_text}"
#         response = model.generate_content(prompt)
#         return response.text.strip()

#     def getTopAssessments(self, user_query, k=5):
#         better_query = self.enhance_query(user_query)
#         query_vector = self.vectorizer.transform([better_query])

#         scores = cosine_similarity(query_vector, self.vectors).flatten()
#         self.df["score"] = scores

#         top_results = self.df.nlargest(k, "score").copy()
#         top_results["summary"] = top_results["combined"].apply(self.summarize_assessment)
        
#         return top_results[["Name", "summary", "score"]]
