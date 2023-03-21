from pandas import DataFrame
from data.sentiments_analysis.sentiment_analysis_model_training import train_sentiment_model
from data.sentiments_analysis.sentiment_analysis_model_evaluation import evaluate_sentiment_model

class SentimentModel:
    def __init__(self, data):
        self.model, self.vectorizer, self.accuracy = train_sentiment_model(data)

    def preprocess_text(self, text):
        # Add your preprocessing code here

    def predict_sentiment(self, text, vectorizer, model):
        # Preprocess text
        text = self.preprocess_text(text)

        # Vectorize text using bag of words approach
        X = vectorizer.transform([' '.join(text)])

        # Make prediction
        sentiment = model.predict(X)[0]

        return sentiment

    def evaluate_model(self, data, vectorizer, model):
        report = evaluate_sentiment_model(model, vectorizer, data)
        return report
