from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import seaborn as sns

# Ensure required resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Load saved Google Reviews HTML file
def parse_reviews_from_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    reviews = []
    for review in soup.find_all("q", class_="XllAv H4 _a"):  # Adjust class based on actual HTML
        reviews.append(review.text.strip())

    return reviews

# Preprocess text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(tokens)

# Perform Topic Modeling using LDA
def topic_modeling(reviews, num_topics=5):
    vectorizer = CountVectorizer(max_features=1000, stop_words='english')
    review_matrix = vectorizer.fit_transform(reviews)
    lda_model = LatentDirichletAllocation(n_components=num_topics, random_state=42)
    lda_model.fit(review_matrix)
    
    terms = vectorizer.get_feature_names_out()
    for idx, topic in enumerate(lda_model.components_):
        print(f"Topic {idx + 1}: ", [terms[i] for i in topic.argsort()[-10:]])

# Perform Sentiment Analysis
def sentiment_analysis(reviews):
    sentiments = []
    for review in reviews:
        polarity = TextBlob(review).sentiment.polarity
        if polarity > 0:
            sentiments.append('Positive')
        elif polarity < 0:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')
    return sentiments

# Analyze Issues in Negative Reviews
def issue_analysis(df):
    negative_reviews = df[df['sentiment'] == 'Negative']
    text = ' '.join(negative_reviews['review_text'])
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Main Execution
if __name__ == "__main__":
    import os

file_path = "reviews.html"
if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' not found. Make sure it exists in the correct directory.")
    exit()  # Replace with your saved file
    reviews = parse_reviews_from_html(file_path)
    
    if not reviews:
        print("No reviews found.")
    else:
        df = pd.DataFrame(reviews, columns=['review_text'])
        df['cleaned_text'] = df['review_text'].apply(preprocess_text)
        
        print("\nPerforming Topic Modeling...")
        topic_modeling(df['cleaned_text'])
        
        print("\nPerforming Sentiment Analysis...")
        df['sentiment'] = sentiment_analysis(df['cleaned_text'])
        sns.countplot(x=df['sentiment'], palette='coolwarm')
        plt.title("Sentiment Distribution")
        plt.show()
        
        print("\nPerforming Issue Analysis...")
        issue_analysis(df)
        
        df.to_csv("google_reviews.csv", index=False)  # Save results
