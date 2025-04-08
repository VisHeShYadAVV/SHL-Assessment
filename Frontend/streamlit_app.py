import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Recommender", page_icon="🔍")

st.title("SHL Assessment Recommendation System")

query = st.text_area("Enter Job Description or Assessment Needs:")
k = st.slider("Number of Recommendations", 1, 8, 5)

if st.button("Get Recommendations"):
    with st.spinner("Fetching..."):
        try:
            response = requests.get(
                "http://127.0.0.1:8000/recommend",  # Local FastAPI backend
                params={"query": query, "k": k}  
            )

            if response.status_code == 200:
                results = response.json()

                if not results:
                    st.warning("No recommendations found for this query.")
                else:
                    for idx, item in enumerate(results, 1):
                        name = item.get("name", "Unnamed")
                        url = item.get("url", "#")
                        duration = item.get("duration", "N/A")
                        remote = item.get("remote_testing", "N/A")
                        adaptive = item.get("adaptive_testing", "N/A")
                        test_type = item.get("type", "General")
                        st.markdown(f"### {idx}. {name}")
                        st.markdown(f"[View Assessment Link]({url})")
                        st.markdown(
                            f"**Type:->** {test_type}  \n"
                            f"**Duration:->** {duration}  \n"
                            f"**Remote Testing Support:->** {remote}  \n"
                            f"**Adaptive/IRT Support:->** {adaptive}"
                        )
                        st.markdown("---")
            else:
                st.error(f"Error fetching recommendations from the server. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Exception: {e}")
