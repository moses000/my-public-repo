import time
import joblib
from confluent_kafka import Consumer, KafkaException, KafkaError
import json

def consume_kafka_data(kafka_config, topic="your_topic"):
    """
    Consumes messages from a Kafka topic.
    
    Args:
        kafka_config: Kafka configuration dictionary for Consumer.
        topic: Kafka topic to subscribe to.
    
    Returns:
        features: A list of features to be used for prediction.
    """
    # Create a Kafka consumer
    consumer = Consumer(kafka_config)
    consumer.subscribe([topic])

    while True:
        msg = consumer.poll(timeout=1.0)  # Adjust timeout as needed
        if msg is None:
            continue  # No message, continue waiting
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue  # End of partition
            else:
                raise KafkaException(msg.error())
        else:
            try:
                # Deserialize message (assuming JSON format for features)
                data = msg.value().decode('utf-8')
                parsed_data = json.loads(data)  # Assuming the message is JSON formatted
                features = [parsed_data['feature1'], parsed_data['feature2'], parsed_data['feature3']]  # Adjust based on your actual data
                return features
            except Exception as e:
                print(f"Error parsing message: {e}")
                continue  # Skip the invalid message

def real_time_prediction(model, kafka_config, topic="your_topic", sleep_interval=1):
    """
    Make real-time predictions using the trained model and Kafka stream.
    
    Parameters:
        model: The trained model to use for predictions.
        kafka_config: Kafka configuration dictionary.
        topic: Kafka topic to consume from.
        sleep_interval: Time in seconds to wait between predictions.
    """
    while True:
        try:
            # Fetch real-time data from Kafka
            features = consume_kafka_data(kafka_config, topic)

            if len(features) == 0:
                print("No features available for prediction")
                continue

            # Predict fault (1 = Fault, 0 = No Fault)
            prediction = model.predict([features])
            print(f"Predicted fault status: {prediction[0]}")

        except Exception as e:
            print(f"Error during prediction: {str(e)}")

        time.sleep(sleep_interval)  # Simulate delay between predictions
