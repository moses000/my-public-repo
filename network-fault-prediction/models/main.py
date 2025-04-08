import json
import joblib
from flask import Flask, request, jsonify
from model_training_and_evaluation import train_and_evaluate_model_from_kafka
from realtime_prediction import real_time_prediction
from confluent_kafka import Consumer, KafkaException, KafkaError
import threading

# Initialize Flask app
app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('fault_prediction_model.pkl')

# Kafka configuration for consuming data
kafka_config = {
    'bootstrap.servers': 'your-kafka-server',  # Replace with your Kafka server
    'group.id': 'your-group-id',  # Replace with your group ID
    'auto.offset.reset': 'earliest'
}

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to make predictions using the trained model.
    """
    try:
        data = request.get_json(force=True)
        features = list(data['network_data'].values())  # Adjust to handle your actual data structure
        
        # Predict fault (1 = Fault, 0 = No Fault)
        prediction = model.predict([features])
        
        # Return prediction result as JSON
        return jsonify({'prediction': str(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/train', methods=['POST'])
def train():
    """
    Endpoint to train the model with data from Kafka (real-time or batch).
    """
    try:
        # Retrieve whether to run in batch or real-time mode from the request
        data = request.get_json(force=True)
        batch_mode = data.get('batch_mode', False)
        interval = data.get('interval', 300)  # Interval for batch processing in seconds
        
        # Train the model using Kafka data stream
        if batch_mode:
            # Run in batch mode with a defined interval
            threading.Thread(target=train_and_evaluate_model_from_kafka, args=(kafka_config, True, interval)).start()
            return jsonify({'message': 'Training started in batch mode.'}), 202
        else:
            # Run in real-time mode
            threading.Thread(target=train_and_evaluate_model_from_kafka, args=(kafka_config, False)).start()
            return jsonify({'message': 'Training started in real-time mode.'}), 202

    except Exception as e:
        return jsonify({'error': str(e)}), 400


def run_flask_app():
    """
    Function to run Flask app, allowing it to be executed in a separate thread.
    """
    app.run(debug=True, host="0.0.0.0", port=5000)  # Allow external access to Flask API


if __name__ == '__main__':
    # Start the Flask application in a separate thread to handle API requests
    threading.Thread(target=run_flask_app).start()

    # Optionally, start real-time predictions or additional services
    # Example: You can add a real-time prediction loop here if you need
    real_time_prediction()
