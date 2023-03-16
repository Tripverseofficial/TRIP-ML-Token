import pandas as pd
import numpy as np
from keras.models import load_model

# Load market data
df = pd.read_csv("data/market_data.csv")

# Prepare data for CNN model
X = df.drop(['price', 'volume'], axis=1)
Y = df['price']
X = np.reshape(X.values, (X.shape[0], X.shape[1], 1))

# Load the saved model
model = load_model("cnn_model.h5")

# Make predictions on test data
y_pred = model.predict(X)

# Print mean squared error
mse = np.mean((y_pred - Y) ** 2)
print("Mean squared error: {:.2f}".format(mse))
