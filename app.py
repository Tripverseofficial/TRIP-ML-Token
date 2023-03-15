import load_data

from flask import Flask, jsonify, request
from scripts.CNN_model.convolutional import predict_price as cnn_predict
from scripts.time_series.time import predict_price as time_predict

# Load historical data
historical_data = load_data.load_historical_data()

# Load market data
market_data = load_data.load_market_data()

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # get input data from request
    input_data = request.json['input']
    # determine which machine learning model to use based on some criteria
    # for example, you could use a "model_type" parameter in the request
    model_type = request.json['model_type']
    if model_type == 'cnn':
        prediction = cnn_predict(input_data, market_data)
    elif model_type == 'time':
        prediction = time_predict(input_data, historical_data)
    else:
        # handle invalid model_type
        return jsonify({'error': 'Invalid model_type'}), 400
    # return prediction in JSON format
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run()
