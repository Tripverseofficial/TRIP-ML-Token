import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from data.load_data import load_historical_data, load_market_data
from preprocessing import preprocess_data, prepare_data
from sentiment_analysis import analyze_sentiment, train_sentiment_analysis_model
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error

def train_lstm(X_train, y_train, X_test, y_test):
    model = Sequential()
    model.add(LSTM(128, input_shape=(1, X_train.shape[2])))
    model.add(Dense(1))
    model.compile(loss='mse', optimizer='adam')
    model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0)
    y_pred = model.predict(X_test)
    return mean_absolute_error(y_test, y_pred)

# Load historical data and market data
df = load_historical_data()
market_df = load_market_data()

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set timestamp as index
df.set_index('timestamp', inplace=True)

# Add more features to the dataset
df = prepare_data(df, market_df)

# Prepare data for time series forecasting
scaler = MinMaxScaler(feature_range=(0, 1))
X = scaler.fit_transform(df.drop(columns=['price']).values)
y = X[:, 0]
n_splits = 5
tscv = TimeSeriesSplit(n_splits=n_splits)

# Train and evaluate LSTM model
mae_scores = []
with ProcessPoolExecutor() as executor:
    for train_index, test_index in tscv.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]-1))
        X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]-1))
        mae_scores.append(train_lstm(X_train, y_train, X_test, y_test))
print('LSTM MAE:', np.mean(mae_scores))

# Fit ARIMA model to historical data
model = ARIMA(y, order=(5,1,0))
model_fit = model.fit()

# Make ARIMA predictions
size = int(len(y) * 0.2)
arima_predictions = model_fit.forecast(steps=len(y)-size)[0]

# Scrape news articles, tweets and telegram messages
news_df = scrape_news()
tweets_df = scrape_tweets()
telegram_df = scrape_telegram()

# Preprocess data
with ProcessPoolExecutor() as executor:
    clean_news_df, clean_tweets_df, clean_telegram_df = list(executor.map(preprocess_data, [news_df, tweets_df, telegram_df]))

# Perform sentiment analysis
with ProcessPoolExecutor() as executor:
    news_sentiment_scores, tweets_sentiment_scores, telegram_sentiment_scores = list(executor.map(analyze_sentiment, [clean_news_df, clean_tweets_df, clean_telegram_df]))

# Combine sentiment scores
combined_sentiment_scores = np.concatenate((news_sentiment_scores, tweets_sentiment_scores, telegram_sentiment_scores))

# Train and evaluate sentiment analysis model
model = train_sentiment_analysis_model(combined_sentiment_scores) 
sentiment_scores = model.predict(combined_sentiment_scores)
mae_scores = []
for train_index, test_index in tscv.split(sentiment_scores):
    y_train, y_test = y[train_index], y[test_index]
    y_pred = sentiment_scores[test_index]
    mae = mean_absolute_error(y_test, y_pred)
    mae_scores.append(mae)
    print('Sentiment Analysis MAE:', np.mean(mae_scores))

    # Combine LSTM and ARIMA predictions with sentiment analysis
    combined_predictions = (arima_predictions + sentiment_scores) / 2

    # Scale predictions back to original range
    combined_predictions = scaler.inverse_transform(np.concatenate(([combined_predictions[0]], combined_predictions[1:])))
    arima_predictions = scaler.inverse_transform(np.concatenate(([arima_predictions[0]], arima_predictions[1:])))

    # Output predictions
    print('ARIMA Predictions:', arima_predictions[-1])
    print('LSTM + Sentiment Analysis Predictions:', combined_predictions[-1])
    

