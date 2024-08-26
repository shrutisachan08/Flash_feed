import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
import textstat
import random

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load a larger spaCy model for better vocabulary suggestions
nlp_large = spacy.load("en_core_web_md")

def extract_entities(text):
    """Extract named entities from the text."""
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def summarize_text(text, num_sentences=3):
    """Summarize the text using extractive summarization."""
    doc = nlp(text)
    keyword = []
    stopwords = list(STOP_WORDS)
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    
    for token in doc:
        if(token.text in stopwords or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)
    
    freq_word = Counter(keyword)
    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():  
        freq_word[word] = (freq_word[word]/max_freq)
        
    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]
    
    summary = []
    sorted_sents = sorted(sent_strength.items(), key=lambda x: x[1], reverse=True)
    counter = 0
    for i in range(len(sorted_sents)):
        summary.append(str(sorted_sents[i][0]).capitalize())
        counter += 1
        if(counter >= num_sentences):
            break
            
    return ' '.join(summary)

def analyze_readability(text):
    """Analyze the readability of the text."""
    flesch_reading_ease = textstat.flesch_reading_ease(text)
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
    smog_index = textstat.smog_index(text)
    
    return {
        "Flesch Reading Ease": flesch_reading_ease,
        "Flesch-Kincaid Grade": flesch_kincaid_grade,
        "SMOG Index": smog_index
    }

def enhance_writing(text):
    """Enhance writing by improving grammar and vocabulary."""
    doc = nlp_large(text)
    enhanced_text = []
    suggestions = []

    for sent in doc.sents:
        enhanced_sent = []
        for token in sent:
            if token.pos_ in ['NOUN', 'VERB', 'ADJ', 'ADV'] and len(token.text) > 3:
                # Get similar words
                similar_words = [w for w in token.vocab if w.is_lower == token.is_lower and w.prob >= -15 and w.similarity(token) > 0.7]
                if similar_words:
                    # Choose a random similar word
                    replacement = random.choice(similar_words)
                    if replacement.text != token.text:
                        enhanced_sent.append(replacement.text)
                        suggestions.append(f"Consider replacing '{token.text}' with '{replacement.text}'")
                    else:
                        enhanced_sent.append(token.text)
                else:
                    enhanced_sent.append(token.text)
            else:
                enhanced_sent.append(token.text)
        
        # Basic grammar check (very simplistic)
        if enhanced_sent[0].islower():
            enhanced_sent[0] = enhanced_sent[0].capitalize()
            suggestions.append(f"Capitalized the first word of the sentence: '{enhanced_sent[0]}'")
        
        if enhanced_sent[-1] not in ['.', '!', '?']:
            enhanced_sent.append('.')
            suggestions.append("Added a period at the end of the sentence.")
        
        enhanced_text.append(' '.join(enhanced_sent))

    return ' '.join(enhanced_text), suggestions

def main():
    st.title("AI-Assisted Writing Tool for Journalists")

    article_text = st.text_area("Enter your article text here:", height=200)

    if st.button("Analyze and Improve"):
        if article_text:
            with st.spinner("Analyzing your text..."):
                # Entity extraction
                entities = extract_entities(article_text)
                
                # Text summarization
                summary = summarize_text(article_text)
                
                # Readability analysis
                readability_scores = analyze_readability(article_text)

                # Writing enhancement
                enhanced_text, suggestions = enhance_writing(article_text)

            # Display results
            st.subheader("Named Entities")
            for entity, label in entities:
                st.write(f"- {entity} ({label})")

            st.subheader("Text Summary")
            st.write(summary)

            st.subheader("Readability Scores")
            for metric, score in readability_scores.items():
                st.write(f"- {metric}: {score:.2f}")

            st.subheader("Enhanced Writing")
            st.write(enhanced_text)

            st.subheader("Writing Suggestions")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")

        else:
            st.warning("Please enter some text to analyze.")

if __name__ == "__main__":
    main()