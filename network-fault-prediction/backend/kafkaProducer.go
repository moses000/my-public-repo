package main

import (
	"encoding/json"
	"log"

	"github.com/segmentio/kafka-go"
)

type NetworkData struct {
	Feature1 float64 `json:"feature1"`
	Feature2 float64 `json:"feature2"`
	Feature3 float64 `json:"feature3"`
}

func produceKafkaMessages() {
	// Kafka setup
	broker := "localhost:9092" // Change to your Kafka broker address
	topic := "network-faults"  // Kafka topic to publish to

	// Create a Kafka writer
	writer := kafka.NewWriter(kafka.WriterConfig{
		Brokers: []string{broker},
		Topic:   topic,
	})

	defer writer.Close()

	// Simulate producing messages
	for {
		// Create dummy network fault data
		data := NetworkData{
			Feature1: 23.5,
			Feature2: 78.1,
			Feature3: 5.3,
		}

		// Marshal the data into JSON
		message, err := json.Marshal(data)
		if err != nil {
			log.Printf("Error marshalling data: %v", err)
			continue
		}

		// Write the message to Kafka
		err = writer.WriteMessages(context.Background(), kafka.Message{
			Value: message,
		})
		if err != nil {
			log.Printf("Error writing message to Kafka: %v", err)
		}

		// Simulate delay between messages
		time.Sleep(1 * time.Second)
	}
}

func main() {
	// Start producing Kafka messages
	produceKafkaMessages()
}
