import load_data
from scripts.CNN_model.cnn_model_evaluation import evaluate_cnn_model
from scripts.time_series.time_series_model_evaluation import evaluate_time_series_model
from scripts.sentiments_analysis.sentiment_analysis_model_evaluation import evaluate_sentiment_analysis_model

# Load cleaned historical data
historical_data_cleaned = load_data.load_cleaned_historical_data()

# Load cleaned market data
market_data_cleaned = load_data.load_cleaned_market_data()

# Load sentiment analysis data
sentiment_analysis_data = load_data.load_sentiment_analysis_data()

# Evaluate machine learning models
cnn_model_metrics = evaluate_cnn_model(market_data_cleaned, historical_data_cleaned)
time_series_model_metrics = evaluate_time_series_model(historical_data_cleaned)
sentiment_analysis_model_metrics = evaluate_sentiment_analysis_model(sentiment_analysis_data)

# Save model metrics
load_data.save_model_metrics(cnn_model_metrics, 'cnn_model_metrics.csv')
load_data.save_model_metrics(time_series_model_metrics, 'time_series_model_metrics.csv')
load_data.save_model_metrics(sentiment_analysis_model_metrics, 'sentiment_analysis_model_metrics.csv')
