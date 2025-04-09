import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the CSV file
df = pd.read_csv("shl_real_assessments.csv")

# Fill NaNs with empty string for text processing
df['Name'] = df['Name'].fillna('')
df['Description'] = df['Description'].fillna('')

# Combine name and description for better matching
df['Combined'] = df['Name'] + " " + df['Description']

# Vectorize the combined text column
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['Combined'])

def get_full_assessment_info(name: str):
    """Fetch detailed info for a given assessment name from the dataset"""
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
            "test_type": "General"  # Adjust if needed
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

def get_recommendations(query: str, k: int):
    """Return top-k relevant assessments with full details"""
    query_vec = vectorizer.transform([query])
    similarity_scores = cosine_similarity(query_vec, tfidf_matrix).flatten()

    # Get indices of top-k matches
    top_indices = similarity_scores.argsort()[::-1][:k]
    top_names = df.iloc[top_indices]['Name'].tolist()

    # Return detailed recommendation info
    results = [get_full_assessment_info(name) for name in top_names]
    return results
