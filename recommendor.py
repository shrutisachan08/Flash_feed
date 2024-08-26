import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

# Function to fetch news from NewsAPI
def fetch_news(api_key, category='general', country='us', page_size=100):
    url = f'https://newsapi.org/v2/top-headlines?category={category}&country={country}&pageSize={page_size}&apiKey={api_key}'
    response = requests.get(url)
    return response.json()['articles']

# Function to preprocess news data
def preprocess_news(articles):
    df = pd.DataFrame(articles)
    df['content'] = df['title'] + ' ' + df['description'].fillna('')
    return df

# Function to get recommendations
def get_recommendations(df, preferences, num_recommendations=5):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['content'])
    
    user_preferences = ' '.join(preferences)
    user_vector = tfidf.transform([user_preferences])
    
    cosine_similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()
    recommended_indices = cosine_similarities.argsort()[-num_recommendations:][::-1]
    
    return df.iloc[recommended_indices]

# Streamlit app
def main():
    st.title('News Recommendation System')

    # You should replace this with your actual NewsAPI key
    api_key = 'b8a03c825ab64da3bbf460c920f0b492'

    # Fetch news
    articles = fetch_news(api_key)
    df = preprocess_news(articles)

    # User preferences input
    st.header('Enter Your Preferences')
    preferences = st.text_input('Enter keywords separated by commas (e.g., technology, sports, politics)')

    if st.button('Get Recommendations'):
        if preferences:
            user_preferences = [pref.strip() for pref in preferences.split(',')]
            recommendations = get_recommendations(df, user_preferences)

            st.header('Recommended News')
            for _, article in recommendations.iterrows():
                st.subheader(article['title'])
                st.write(article['description'])
                st.write(f"Read more: {article['url']}")
                st.write('---')
        else:
            st.warning('Please enter your preferences to get recommendations.')

if __name__ == '__main__':
    main()