import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense

# Load market data
df = pd.read_csv("data/market_data.csv")

# Prepare data for CNN model
X = df.drop(['price', 'volume'], axis=1)
Y = df['price']
X = np.reshape(X.values, (X.shape[0], X.shape[1], 1))

# Define CNN model architecture
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(X.shape[1], 1)))
model.add(Conv1D(filters=64, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(1))

# Compile and fit model to market data
model.compile(optimizer='adam', loss='mse')
model.fit(X, Y, epochs=50, verbose=1)

# Make predictions
X_test = np.reshape(df.tail(1).drop(['price', 'volume'], axis=1).values, (1, X.shape[1], 1))
y_pred = model.predict(X_test)

# Print prediction
print(y_pred)
