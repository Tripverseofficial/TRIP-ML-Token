import pandas as pd

def load_historical_data():
    df = pd.read_csv("data/historical_data.csv")
    return df

def load_market_data():
    df = pd.read_csv("data/market_data.csv")
    return df
