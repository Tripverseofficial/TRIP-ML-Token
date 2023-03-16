import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from sklearn.model_selection import train_test_split

def prepare_data(df):
    # Prepare data for CNN model
    X = df.drop(['price', 'volume'], axis=1)
    Y = df['price']
    X = np.reshape(X.values, (X.shape[0], X.shape[1], 1))
    return X, Y

def train_model(X, Y, random_state=None):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=random_state)

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
    model.fit(X_train, y_train, epochs=50, verbose=1)

    return model

def save_model(model, filename):
    # Save the model
    model.save(filename)

# Load market data
df = pd.read_csv("data/market_data.csv")

# Prepare data for CNN model
X, Y = prepare_data(df)

# Train the model
model = train_model(X, Y)

# Save the model
save_model(model, "cnn_model.h5")
