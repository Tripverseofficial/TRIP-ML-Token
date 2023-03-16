import pandas as pd
from sklearn.metrics import classification_report
from data.sentiments_analysis.preprocessing import preprocess_text

def evaluate_sentiment_model(model, vectorizer, data):
    # Preprocess text
    data['text'] = data['text'].apply(preprocess_text)

    # Vectorize text using bag of words approach
    X = vectorizer.transform(data['text'].apply(lambda x: ' '.join(x)))

    # Make predictions on data
    y_pred = model.predict(X)

    # Generate classification report
    report = classification_report(data['sentiment'], y_pred)

    return report
