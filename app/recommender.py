import pandas as pd
from app.model import SHLMODEL


df = pd.read_csv("shl_real_assessments.csv")
model = SHLMODEL(df)

def get_generic_assessments(skip_ids=set(), count=10):
    return df[~df['AssessmentID'].isin(skip_ids)].head(count)


def get_recommendations(query: str, k: int = 10):
    results = model.getTopAssessments(query, k)
    output = []

    for _, row in results.iterrows():
        output.append({
            "assessment_name": row.get("Name", "Unnamed"),
            "url": row.get("Link", "#"),
            "remote_testing_support": row.get("Remote Testing Support", "N/A"),
            "adaptive_irt_support": row.get("Adaptive Support", "N/A"),
            "duration": row.get("Duration", "N/A"),
            "test_type": row.get("Test Type", "N/A")  
        })

    if len(output) < k:
        needed = k - len(output)
        fillers = get_generic_assessments(set(results['AssessmentID']), needed)
        for _, row in fillers.iterrows():
            output.append({
                "assessment_name": row.get("Name", "Unnamed"),
                "url": row.get("Link", "#"),
                "remote_testing_support": row.get("Remote Testing Support", "N/A"),
                "adaptive_irt_support": row.get("Adaptive Support", "N/A"),
                "duration": row.get("Duration", "N/A"),
                "test_type": row.get("Test Type", "N/A")
            })

    return output

