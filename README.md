# SHL Assessment Recommendation System

**Author:** Vishesh Yadav 

## 🧠 Overview

Hiring managers often face difficulties identifying the right assessments for roles due to reliance on keyword filters. This project addresses the problem by developing an intelligent recommendation system that takes **natural language queries** or **job descriptions** as input and recommends relevant SHL assessments.

### 🔗 Live Links
- **Frontend Demo:** [https://shl-assessment-hnpazdzzrmfbnrbf5uvqsb.streamlit.app/](https://shl-assessment-hnpazdzzrmfbnrbf5uvqsb.streamlit.app/)
- **API Endpoint:** [https://shl-assessment.onrender.com/recommend](https://shl-assessment.onrender.com/recommend)
- **GitHub Repository:** [https://github.com/VisHeShYadAVV/SHL-Assessment](https://github.com/VisHeShYadAVV/SHL-Assessment)

---

## 🚀 Approach

### 🗂 Data Source
Due to scraping restrictions on the SHL website, I created **mock data** closely resembling the structure and variety of SHL’s real assessments.

Each entry contains:
- Assessment Name & URL
- Duration
- Test Type
- Remote Testing Support (Yes/No)
- Adaptive/IRT Support (Yes/No)

### 🔍 Query Parsing
- Leveraged **Google Gemini Free API** to analyze input queries.
- Extracted key features such as skills, duration limits, and required test types.

### 🧠 Recommendation Logic
- Applied **TF-IDF** vectorization and **cosine similarity** to match input queries with assessment metadata.
- Returned the **top 10 most relevant assessments** based on similarity.

---

## ⚙️ Tech Stack

- **Backend:** Python, FastAPI  
- **Frontend:** Streamlit  
- **NLP:** Google Gemini API, scikit-learn (TF-IDF, cosine similarity)  
- **Hosting:** Render (Free Plan)

---

## 🛠 Deployment Note

This project is hosted on **Render's free tier**, so the backend may take **40–60 seconds to wake up** if idle for more than 15 minutes. After that, responses are fast and stable.

---

## 📋 Output

The app displays a table of up to **10 recommended SHL assessments**, each including:
- Assessment Name (clickable)
- Duration
- Test Type
- Remote Testing Support (Yes/No)
- Adaptive/IRT Support (Yes/No)

---

## ✅ Example Queries

You can try queries like:
- _"I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes."_
- _"Looking to hire mid-level professionals who are proficient in Python, SQL and JavaScript. Need an assessment package that can test all skills with max duration of 60 minutes."_
- _"Here is a JD text, can you recommend some assessment that can help me screen applications. Time limit is less than 30 minutes."_

---

Feel free to explore, test, and contribute!
