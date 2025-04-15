package main

import (
	"fmt"
	"time"

	"github.com/moses000/my-public-repo/jetcore/balancer"
	"github.com/moses000/my-public-repo/jetcore/broker"
	"github.com/moses000/my-public-repo/jetcore/emitter"
	"github.com/moses000/my-public-repo/jetcore/jobber"
	"github.com/moses000/my-public-repo/jetcore/logger"
	"github.com/moses000/my-public-repo/jetcore/ratelimit"
)

func main() {
	log := logger.New()
	limit := ratelimit.New(5, time.Second)
	scheduler := jobber.New()
	events := emitter.New()
	queue := broker.NewTopicBroker()
	lb := balancer.NewRoundRobin([]string{"svc1", "svc2", "svc3"})

	for i := 0; i < 10; i++ {
		if !limit.Allow("client1") {
			log.Warn("Rate limit hit!")
			continue
		}
		log.Info("Request allowed")
	}

	scheduler.Every(3*time.Second, func() {
		log.Info("Scheduled Job ran")
	})

	events.On("user:signup", func(data any) {
		log.Info("New user signed up", data)
	})
	events.Emit("user:signup", "john@example.com")

	queue.Subscribe("order:created", func(payload any) {
		log.Info("Order received:", payload)
	})
	queue.Publish("order:created", "Order #123")

	for i := 0; i < 5; i++ {
		fmt.Println("Sending request to:", lb.Next())
	}

	select {}
}
