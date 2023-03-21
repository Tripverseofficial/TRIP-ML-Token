import requests
import json
import pandas as pd
from datetime import datetime
import time

# Set up API endpoint and parameters
endpoint = "https://api.coingecko.com/api/v3/coins/rebase"
params = {
    "localization": "false",
    "tickers": "false",
    "market_data": "true",
    "community_data": "false",
    "developer_data": "false",
    "sparkline": "false"
}

# Define function to collect data
def collect_data():
    try:
        # Make API request
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # check if request was successful

        data = response.json()
        
        # Extract relevant data
        timestamp = datetime.now()
        price = data["market_data"]["current_price"]["usd"]
        volume = data["market_data"]["total_volume"]["usd"]
        
        # Create DataFrame with data
        df = pd.DataFrame({"timestamp": [timestamp], "price": [price], "volume": [volume]})
        
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error collecting data: {e}")
    
    except (KeyError, ValueError) as e:
        print(f"Error parsing response data: {e}")
    
    except Exception as e:
        print(f"Unknown error occurred: {e}")
        
    # Sleep for 10 seconds to limit the rate of API requests
    time.sleep(10)

while True:
    # Call function to collect data
    try:
        df = collect_data()
        
        # Save data to historical_data.csv file
        with open("historical_data.csv", "a") as f:
            df.to_csv(f, header=f.tell()==0, index=False)
            
        # Save data to market_data.csv file
        with open("market_data.csv", "w") as f:
            df.to_csv(f, header=True, index=False)

    except Exception as e:
        print(f"Error occurred while collecting and saving data: {e}")

    # Sleep for 10 seconds before collecting data again
    time.sleep(10)
