import requests
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

API_KEY = 'b8a03c825ab64da3bbf460c920f0b492'
BASE_URL = 'https://newsapi.org/v2/everything'

def fetch_news(query, page_size=100):
    params = {
        'q': query,
        'apiKey': API_KEY,
        'pageSize': page_size
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        st.write(f"Error fetching news: {response.status_code}")
        return pd.DataFrame()
    
    data = response.json()
    articles = data.get('articles', [])
    
    df = pd.DataFrame(articles)
    return df

def preprocess_articles(df):
    df['content'] = df['title'].fillna('') + ' ' + df['description'].fillna('')
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(df['content'])
    return tfidf_matrix

def recommend_articles(tfidf_matrix, article_index, num_recommendations=5):
    cosine_sim = cosine_similarity(tfidf_matrix[article_index], tfidf_matrix)
    similar_articles = cosine_sim.flatten().argsort()[-(num_recommendations+1):-1]
    return similar_articles

def get_personalized_news(user_interests, num_recommendations=5):
    all_articles = pd.DataFrame()
    for interest in user_interests:
        df = fetch_news(interest)
        all_articles = pd.concat([all_articles, df], ignore_index=True)
    
    if all_articles.empty:
        st.write("No articles found for the given interests.")
        return pd.DataFrame()
    
    tfidf_matrix = preprocess_articles(all_articles)
    recommended_indices = recommend_articles(tfidf_matrix, 0, num_recommendations)
    return all_articles.iloc[recommended_indices][['title', 'description']]

# Fetch and display news articles
news_df = fetch_news('technology')
if not news_df.empty:
    st.write(news_df[['title', 'description']].head())
else:
    st.write("No news articles found for 'technology'.")

# Example user interests
user_interests = ['technology', 'AI', 'science']
personalized_news = get_personalized_news(user_interests)

if not personalized_news.empty:
    st.write(personalized_news)
else:
    st.write("No recommendations available.")
