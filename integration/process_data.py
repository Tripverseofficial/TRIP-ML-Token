import load_data
from scripts.data_cleaning.outlier_removal import remove_outliers
from scripts.data_cleaning.missing_value_imputation import impute_missing_values
from scripts.data_cleaning.error_correction import correct_errors

# Load historical data
historical_data = load_data.load_historical_data()

# Load market data
market_data = load_data.load_market_data()

# Data cleaning
historical_data_cleaned = remove_outliers(historical_data)
historical_data_cleaned = impute_missing_values(historical_data_cleaned)
historical_data_cleaned = correct_errors(historical_data_cleaned)

market_data_cleaned = remove_outliers(market_data)
market_data_cleaned = impute_missing_values(market_data_cleaned)
market_data_cleaned = correct_errors(market_data_cleaned)

# Save cleaned data
load_data.save_cleaned_data(historical_data_cleaned, 'historical_data_cleaned.csv')
load_data.save_cleaned_data(market_data_cleaned, 'market_data_cleaned.csv')
