import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from preprocessing import simulate_realtime_data
from confluent_kafka import Consumer, KafkaException, KafkaError
import time
from realtime_prediction import real_time_prediction  # Import the function

def train_and_evaluate_model_from_kafka(kafka_config, batch_mode=False, interval=300):
    """
    Train and evaluate the model using Kafka data stream.
    If batch_mode is True, it processes data in periodic batches.
    """
    # Set up the Kafka consumer
    consumer = Consumer(kafka_config)
    consumer.subscribe(['your-kafka-topic'])

    # Initialize feature and label lists for training
    X_data = []
    y_data = []

    # Accumulate data from Kafka
    try:
        if batch_mode:
            start_time = time.time()
            while time.time() - start_time < interval:
                msg = consumer.poll(timeout=1.0)  # Adjust timeout as needed

                if msg is None:
                    continue  # No message, continue to poll
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())

                # Assuming the message value contains features and label
                features = np.fromstring(msg.value().decode('utf-8'), sep=',')
                label = features[-1]  # Assuming the last feature is the label (fault)
                X_data.append(features[:-1])  # All except the last as features
                y_data.append(label)  # The last as the target variable

            # Convert to numpy arrays for sklearn
            X = np.array(X_data)
            y = np.array(y_data)
        else:
            # Real-time training by consuming the Kafka data and training continuously
            while True:
                msg = consumer.poll(timeout=1.0)  # Adjust timeout as needed

                if msg is None:
                    continue  # No message, continue to poll
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        raise KafkaException(msg.error())

                # Assuming the message value contains features and label
                features = np.fromstring(msg.value().decode('utf-8'), sep=',')
                label = features[-1]  # Assuming the last feature is the label (fault)
                X_data.append(features[:-1])  # All except the last as features
                y_data.append(label)  # The last as the target variable

                # Convert to numpy arrays for sklearn
                X = np.array(X_data)
                y = np.array(y_data)

                # Train model on the incoming data
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X, y)

                # Evaluate model
                y_pred = model.predict(X)
                accuracy = accuracy_score(y, y_pred)
                print(f"Real-time Model Accuracy: {accuracy * 100:.2f}%")
                joblib.dump(model, 'fault_prediction_model.pkl')

    except KeyboardInterrupt:
        pass
    finally:
        # Close the consumer when done
        consumer.close()

    # After training, call real-time prediction
    try:
        # Load the trained model once after training is completed
        model = joblib.load('fault_prediction_model.pkl')  # Load model
        print("Model loaded successfully for real-time prediction.")
        
        # Kafka configuration for real-time prediction
        kafka_config = {
            'bootstrap.servers': 'your_kafka_broker',
            'group.id': 'your_group_id',
            'auto.offset.reset': 'earliest'
        }
        
        # Start real-time predictions
        real_time_prediction(model, kafka_config)
        
    except Exception as e:
        print(f"Error in real-time prediction: {e}")
