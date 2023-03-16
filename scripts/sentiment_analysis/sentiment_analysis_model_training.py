import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from data.sentiments_analysis.preprocessing import preprocess_text

def train_sentiment_model(data):
    # Preprocess text
    data['text'] = data['text'].apply(preprocess_text)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data['text'], data['sentiment'], test_size=0.2, random_state=42)

    # Vectorize text using bag of words approach
    vectorizer = CountVectorizer()
    X_train = vectorizer.fit_transform(X_train.apply(lambda x: ' '.join(x)))
    X_test = vectorizer.transform(X_test.apply(lambda x: ' '.join(x)))

    # Train model using Naive Bayes algorithm
    model = MultinomialNB()
    model.fit(X_train, y_train)

    # Evaluate model on test data
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return model, vectorizer, accuracy
