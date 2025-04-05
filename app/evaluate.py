import requests

# Benchmark dataset: list of queries and ideal top-3 assessments
benchmark = [
    {
        "query": "Looking for a candidate with strong numerical and logical reasoning skills.",
        "expected": [
            "Numerical Reasoning Test",
            "Logical Reasoning Test",
            "Cognitive Ability Test"
        ]
    },
    {
        "query": "Need someone for sales and client negotiation roles.",
        "expected": [
            "Sales Skills Assessment",
            "Negotiation Skills Test",
            "Customer Service Test"
        ]
    },
    # Add more queries as needed
]

def recall_at_k(predicted, expected, k=3):
    relevant_items = set(expected)
    retrieved_items = set(predicted[:k])
    return len(relevant_items & retrieved_items) / len(relevant_items)

def precision_at_k(predicted, expected, k=3):
    relevant_items = set(expected)
    retrieved_items = set(predicted[:k])
    return len(relevant_items & retrieved_items) / k

def evaluate_model():
    total_recall = 0
    total_precision = 0
    num_queries = len(benchmark)

    for item in benchmark:
        query = item["query"]
        expected = item["expected"]

        # Call your FastAPI model
        response = requests.get("http://127.0.0.1:8000/recommend", params={"query": query, "k": 3})
        if response.status_code == 200:
            results = response.json()
            predicted = [res["name"] for res in results]

            recall = recall_at_k(predicted, expected)
            precision = precision_at_k(predicted, expected)

            print(f"Query: {query}")
            print(f"Expected: {expected}")
            print(f"Predicted: {predicted}")
            print(f"Recall@3: {recall:.3f}")
            print(f"Precision@3: {precision:.3f}")
            print("-" * 50)

            total_recall += recall
            total_precision += precision
        else:
            print(f"Failed to get response for query: {query}")

    mean_recall = total_recall / num_queries
    mean_precision = total_precision / num_queries

    print(f"\n📊 Mean Recall@3: {mean_recall:.3f}")
    print(f"📊 Mean Precision@3: {mean_precision:.3f}")

if __name__ == "__main__":
    evaluate_model()
