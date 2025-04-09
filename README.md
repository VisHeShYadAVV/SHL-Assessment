# SHL Assessment Recommendation System

This project is an AI-powered recommendation system that suggests the most relevant SHL assessments based on a natural language job description or query.

## 🔗 Demo Links

- **Frontend Demo:** [https://shl-assessment-hnpazdzzrmfbnrbf5uvqsb.streamlit.app/](https://shl-assessment-hnpazdzzrmfbnrbf5uvqsb.streamlit.app/)
- **API Endpoint:** [https://shl-assessment-production-a03e.up.railway.app/recommend?query=java&k=5](https://shl-assessment-production-a03e.up.railway.app/recommend?query=java&k=5)
- **Report (PDF):** [https://drive.google.com/file/d/128znwbICpqa1tvLryXVxZVtc0Dxu93qv/view?usp=drive_link](https://drive.google.com/file/d/128znwbICpqa1tvLryXVxZVtc0Dxu93qv/view?usp=drive_link)

## 📄 Overview
Hiring managers often struggle to match job roles with relevant SHL assessments. This tool addresses the issue by parsing job descriptions or queries and returning the most suitable assessments from a prepared catalog.

## 🧠 Approach
- **Data:** A CSV file mimicking SHL catalog with fields like assessment name, duration, test type, remote testing, and IRT support.
- **Query Understanding:** Google Gemini API is used to extract structured insights from free-text input.
- **Recommendation Logic:**
  - Combine assessment name and description.
  - Vectorize with TF-IDF.
  - Use cosine similarity to rank and return top-k matches.

## ⚙️ Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** Streamlit
- **NLP & ML:** Google Gemini API, Scikit-learn
- **Deployment:** Render (API), Streamlit Cloud (Frontend)

## 📦 Files
- `main.py`: FastAPI backend
- `recommender.py`: Core recommendation logic
- `shl_real_assessments.csv`: Data file with mock SHL assessments

## 🚀 How to Run Locally
```bash
git clone https://github.com/VisHeShYadAVV/SHL-Assessment.git
cd SHL-Assessment
pip install -r requirements.txt
uvicorn main:app --reload
```

## 🧪 Sample API Query
```
GET /recommend?query=java&k=5
```

## 📬 Contact
**Vishesh Yadav**  
visheshyadav06122004@gmail.com

