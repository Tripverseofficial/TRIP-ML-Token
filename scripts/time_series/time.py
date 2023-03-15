import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from concurrent.futures import ProcessPoolExecutor
from new_scrapper import scrape_news
from twitter_scrapper import scrape_tweets
from preprocessing import preprocess_data
from sentiment_analysis import analyze_sentiment

from data.load_data import load_historical_data, load_market_data

df = load_historical_data()
market_df = load_market_data()

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set timestamp as index
df.set_index('timestamp', inplace=True)

# Prepare data for ARIMA model
X = df['price'].values
size = int(len(X) * 0.8)
train, test = X[0:size], X[size:len(X)]
history = [x for x in train]

# Fit ARIMA model to historical data
model = ARIMA(history, order=(5,1,0))
model_fit = model.fit()

# Make ARIMA predictions
with ProcessPoolExecutor() as executor:
    arima_predictions = list(executor.map(lambda x: x[0], [model_fit.forecast() for _ in range(len(test))]))
history.extend(test)

# Market Sentiment Analysis
# Train market sentiment model
market_sentiment_model = train_market_sentiment_model() # replace with your function to train market sentiment model

# Make market sentiment predictions
market_sentiment_predictions = market_sentiment_model.predict(market_df) # replace with your function to predict market sentiment

# Make sentiment impact predictions
sentiment_impact_predictions = predict_sentiment_impact(market_sentiment_predictions, combined_sentiment_scores) # replace with your function to predict the impact of market sentiment on token price


# Scrape news articles and tweets
news_df = scrape_news()
tweets_df = scrape_tweets()

# Preprocess data
with ProcessPoolExecutor() as executor:
    clean_news_df, clean_tweets_df = list(executor.map(preprocess_data, [news_df, tweets_df]))

# Perform sentiment analysis
with ProcessPoolExecutor() as executor:
    news_sentiment_scores, tweets_sentiment_scores = list(executor.map(analyze_sentiment, [clean_news_df, clean_tweets_df]))

# Combine sentiment scores
combined_sentiment_scores = np.concatenate((news_sentiment_scores, tweets_sentiment_scores))
                                            
# Combine ARIMA and market sentiment predictions
combined_predictions = np.add(arima_predictions, sentiment_impact_predictions)

# Print predictions
print(combined_predictions)
