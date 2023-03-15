import os
from typing import Any, Dict

from flask import Flask, jsonify, request
from jsonschema import validate, ValidationError
from scripts.CNN_model.convolutional import predict_price as cnn_predict
from scripts.time_series.time import predict_price as time_predict


def load_env_var(key: str, default: Any = None) -> Any:
    """Load environment variable or return default value."""
    return os.environ.get(key, default)


# Load historical data
historical_data_path = load_env_var("HISTORICAL_DATA_PATH", "data/historical_data.json")
historical_data = load_data.load_historical_data(historical_data_path)

# Load market data
market_data_path = load_env_var("MARKET_DATA_PATH", "data/market_data.json")
market_data = load_data.load_market_data(market_data_path)

# Define JSON schema for input data
input_data_schema = {
    "type": "object",
    "properties": {
        "input": {"type": "string"},
        "model_type": {"type": "string", "enum": ["cnn", "time"]},
    },
    "required": ["input", "model_type"],
}

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict() -> Dict[str, Any]:
    """Predict the price using either the CNN or time series model."""
    try:
        # Validate input data
        input_data = request.get_json()
        validate(instance=input_data, schema=input_data_schema)
    except (TypeError, ValueError, ValidationError) as e:
        # Return error if input data is invalid
        return jsonify({'error': str(e)}), 400

    # Get input data from request
    input_data = input_data['input']

    # Determine which machine learning model to use based on model_type
    model_type = input_data['model_type']
    if model_type == 'cnn':
        prediction = cnn_predict(input_data, market_data)
    elif model_type == 'time':
        prediction = time_predict(input_data, historical_data)
    else:
        # Handle invalid model_type
        return jsonify({'error': 'Invalid model_type'}), 400

    # Return prediction in JSON format
    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    app.run()
