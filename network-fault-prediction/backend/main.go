package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/segmentio/kafka-go"
)

type PredictionRequest struct {
	NetworkData map[string]float64 `json:"network_data"`
}

type PredictionResponse struct {
	Prediction string `json:"prediction"`
}

// consumeKafkaMessages consumes messages from the Kafka topic
func consumeKafkaMessages() {
	// Kafka setup
	broker := "localhost:9092" // Change to your Kafka broker address
	topic := "network-faults"  // Kafka topic to listen to
	groupID := "go-consumer-group"

	// Create a new Kafka reader
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers: []string{broker},
		Topic:   topic,
		GroupID: groupID,
	})

	defer reader.Close()

	// Continuously read messages from Kafka
	for {
		m, err := reader.ReadMessage(context.Background())
		if err != nil {
			log.Printf("Error reading message: %v", err)
			continue
		}

		// Parse the message into a PredictionRequest
		var request PredictionRequest
		err = json.Unmarshal(m.Value, &request)
		if err != nil {
			log.Printf("Error parsing message: %v", err)
			continue
		}

		// Send data to the Python model for prediction
		sendPredictionToPython(request)
	}
}

// sendPredictionToPython sends the Kafka message data to the Python model
func sendPredictionToPython(request PredictionRequest) {
	// Prepare the request data for the Python model
	requestData, err := json.Marshal(request)
	if err != nil {
		log.Printf("Error marshalling request data: %v", err)
		return
	}

	// Send data to the Python model via HTTP
	resp, err := http.Post("http://localhost:5000/predict", "application/json", bytes.NewBuffer(requestData))
	if err != nil {
		log.Printf("Error contacting Python model: %v", err)
		return
	}
	defer resp.Body.Close()

	// Process the prediction response
	var prediction PredictionResponse
	err = json.NewDecoder(resp.Body).Decode(&prediction)
	if err != nil {
		log.Printf("Error decoding prediction response: %v", err)
		return
	}

	// Log the prediction result
	log.Printf("Prediction Result: %s", prediction.Prediction)
}

func main() {
	// Start consuming Kafka messages
	consumeKafkaMessages()
}
