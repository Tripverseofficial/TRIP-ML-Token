import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from concurrent.futures import ProcessPoolExecutor
from data.load_data import load_historical_data, load_market_data

# Load historical data and market data
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

# Train market sentiment model
market_sentiment_model = train_market_sentiment_model() # replace with your function to train market sentiment model

# Save trained models and data for later use
model_fit.save('arima_model.pkl')
market_sentiment_model.save('market_sentiment_model.pkl')
df.to_pickle('historical_data.pkl')
market_df.to_pickle('market_data.pkl')
