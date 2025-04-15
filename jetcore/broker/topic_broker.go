package broker

import "sync"

type Handler func(payload any)

type TopicBroker struct {
	subs map[string][]Handler
	mu   sync.RWMutex
}

func NewTopicBroker() *TopicBroker {
	return &TopicBroker{subs: make(map[string][]Handler)}
}

func (b *TopicBroker) Subscribe(topic string, fn Handler) {
	b.mu.Lock()
	defer b.mu.Unlock()
	b.subs[topic] = append(b.subs[topic], fn)
}

func (b *TopicBroker) Publish(topic string, payload any) {
	b.mu.RLock()
	defer b.mu.RUnlock()
	for _, fn := range b.subs[topic] {
		go fn(payload)
	}
}
