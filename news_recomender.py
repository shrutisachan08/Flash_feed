import streamlit as st
from newsapi import NewsApiClient

# Initialize the NewsApiClient with your API key
api_key = 'b8a03c825ab64da3bbf460c920f0b492'
newsapi = NewsApiClient(api_key=api_key)

# Fetch news articles based on a query
def fetch_news(query, language='en', from_date=None, to_date=None, page_size=10):
    try:
        response = newsapi.get_everything(
            q=query,  # Search query (e.g., a topic, keyword, or phrase)
            language=language,  # e.g., 'en' for English
            from_param=from_date,  # Start date (format: YYYY-MM-DD)
            to=to_date,  # End date (format: YYYY-MM-DD)
            page_size=page_size  # Number of articles to fetch
        )
        return response['articles']
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

# Streamlit app
st.title("News Fetcher")
query = st.text_input("Enter your search query:")
language = st.selectbox("Select language:", ['en', 'es', 'fr', 'de', 'it'])
page_size = st.slider("Number of articles to fetch:", min_value=1, max_value=100, value=10)

if st.button("Fetch News"):
    if query:
        articles = fetch_news(query=query, language=language, page_size=page_size)
        if articles:
            for article in articles:
                st.markdown(f"[{article['title']}]({article['url']})")
                st.write(f"Description: {article['description']}")
                st.write("-" * 80)
        else:
            st.write("No articles found.")
    else:
        st.warning("Please enter a search query.")