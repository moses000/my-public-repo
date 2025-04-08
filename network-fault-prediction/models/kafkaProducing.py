import json
from confluent_kafka import Consumer, KafkaError
import joblib
import requests

# Load the pre-trained model
model = joblib.load('fault_prediction_model.pkl')

# Setup the Kafka consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'python-consumer-group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['network-faults'])

# Function to predict fault status
def predict_fault(features):
    prediction = model.predict([features])
    return prediction[0]

# Start consuming messages from Kafka
try:
    while True:
        msg = consumer.poll(1.0)  # 1 second timeout

        if msg is None:
            continue  # No message
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Decode the message
        message = json.loads(msg.value().decode('utf-8'))

        # Get the network features from the message
        features = list(message['network_data'].values())  # Adjust if needed

        # Get prediction from the model
        prediction = predict_fault(features)

        # Send the prediction result to a Flask API (or handle as needed)
        response = requests.post("http://localhost:5000/predict", json={"prediction": prediction})

        print(f"Predicted Fault: {prediction}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
