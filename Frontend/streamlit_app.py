import streamlit as st
import requests

# Set up the page configuration
st.set_page_config(page_title="SHL Assessment Recommender", page_icon="🔍")

# Set the title of the app
st.title("SHL Assessment Recommendation System")

# Input for job description or assessment needs
query = st.text_area("Enter Job Description or Assessment Needs:")
k = st.slider("Number of Recommendations", 1, 8, 5)

# Button to get recommendations
if st.button("Get Recommendations"):
    with st.spinner("Fetching..."):
        try:
            # Send GET request with query and k as URL parameters
            response = requests.get(
                "https://shl-assessment.onrender.com/recommend",  # Backend URL
                params={"query": query, "k": k}  # Send query and k as URL parameters
            )

            # Check if the request was successful
            if response.status_code == 200:
                results = response.json()

                # Handle case when no results are found
                if not results:
                    st.warning("No recommendations found for this query.")
                else:
                    # Display the recommendations
                    for idx, item in enumerate(results, 1):
                        name = item.get("name", "Unnamed")
                        url = item.get("url", "#")
                        duration = item.get("duration", "N/A")
                        remote = item.get("remote_testing", "N/A")
                        adaptive = item.get("adaptive_testing", "N/A")
                        test_type = item.get("type", "General")  # default fallback

                        # Display the recommendation details
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
