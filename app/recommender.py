import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key="AIzaSyBJSd7iZDT8QvOULp7j9FIMSDJMu5OoB3o")

# Load and prepare dataset
df = pd.read_csv("shl_real_assessments.csv")
df['Name'] = df['Name'].fillna('')
df['Description'] = df['Description'].fillna('')
df['Combined'] = df['Name'] + " " + df['Description']

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['Combined'])

def get_full_assessment_info(name: str):
    match = df[df['Name'].str.lower() == name.lower()]
    if not match.empty:
        row = match.iloc[0]
        return {
            "assessment_name": row['Name'],
            "url": row['Link'],
            "remote_testing_support": row['Remote Testing Support'],
            "adaptive_irt_support": row['Adaptive Support'],
            "duration": row['Duration'],
            "description": row['Description'],
            "test_type": "General"
        }
    else:
        return {
            "assessment_name": name,
            "url": "#",
            "remote_testing_support": "N/A",
            "adaptive_irt_support": "N/A",
            "duration": "N/A",
            "description": "N/A",
            "test_type": "General"
        }

def get_enhanced_query_with_genai(query: str):
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Rephrase or expand this job description for better search matching: {query}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("[GenAI Error]", e)
        return query  # fallback

def get_recommendations(query: str, k: int):
    enhanced_query = get_enhanced_query_with_genai(query)
    query_vec = vectorizer.transform([enhanced_query])
    similarity_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    top_indices = similarity_scores.argsort()[::-1][:k]
    top_names = df.iloc[top_indices]['Name'].tolist()
    results = [get_full_assessment_info(name) for name in top_names]
    return results
