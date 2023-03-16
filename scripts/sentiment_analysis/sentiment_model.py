import pandas as pd
from data.sentiments_analysis.sentiment_analysis_model_training import train_sentiment_model
from data.sentiments_analysis.sentiment_analysis_model_evaluation import evaluate_sentiment_model

class SentimentModel:
    def __init__(self, data):
        self.model, self.vectorizer, self.accuracy = train_sentiment_model(data)

    def predict_sentiment(self, text):
        # Preprocess text
        text = preprocess_text(text)

        # Vectorize text using bag of words approach
        X = self.vectorizer.transform([' '.join(text)])

        # Make prediction
        sentiment = self.model.predict(X)[0]

        return sentiment

    def evaluate_model(self, data):
        report = evaluate_sentiment_model(self.model, self.vectorizer, data)
        return report
