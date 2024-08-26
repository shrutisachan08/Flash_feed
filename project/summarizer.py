import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import streamlit as st

# Initialize spaCy model
nlp = spacy.load('en_core_web_sm')

def summarizer(text):
    # Tokenize and process the text
    doc = nlp(text)
    
    # Initialize stopwords
    stopwords = set(STOP_WORDS)
    
    # Initialize word frequency dictionary
    word_freq = {}
    for word in doc:
        word_text = word.text.lower()
        if word_text not in stopwords and word_text not in punctuation:
            if word_text in word_freq:
                word_freq[word_text] += 1
            else:
                word_freq[word_text] = 1
    
    # Normalize word frequencies
    max_freq = max(word_freq.values(), default=1)  # avoid division by zero
    for word in word_freq.keys():
        word_freq[word] /= max_freq
    
    # Score sentences
    sent_scores = {}
    for sent in doc.sents:
        sent_scores[sent] = sum(word_freq.get(word.text.lower(), 0) for word in sent if word.text.lower() in word_freq)
    
    # Determine the number of sentences for the summary
    select_len = max(1, int(len(list(doc.sents)) * 0.3))  # ensure at least one sentence is selected
    
    # Get the top sentences for the summary
    summary_sents = nlargest(select_len, sent_scores, key=sent_scores.get)
    
    # Convert the sentences back to a string
    summary = ' '.join(sent.text for sent in summary_sents)
    
    return summary

# Streamlit UI
st.title("Text Summarizer")
st.write("Enter text below to summarize:")

# Increase the size of the text area by setting the height
text = st.text_area("Text", "", height=300)  # Adjust height as needed

if st.button("Generate Summary"):
    if text:
        summary = summarizer(text)
        st.subheader("Summary")
        st.write(summary)
    else:
        st.write("Please enter some text to summarize.")
