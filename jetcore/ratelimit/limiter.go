package ratelimit

import (
	"sync"
	"time"

	"golang.org/x/time/rate"
)

type Limiter struct {
	clients map[string]*rate.Limiter
	r       rate.Limit
	burst   int
	mu      sync.Mutex
}

func New(rps int, burstWindow time.Duration) *Limiter {
	return &Limiter{
		clients: make(map[string]*rate.Limiter),
		r:       rate.Every(burstWindow / time.Duration(rps)),
		burst:   1,
	}
}

func (l *Limiter) getLimiter(key string) *rate.Limiter {
	l.mu.Lock()
	defer l.mu.Unlock()

	if limiter, ok := l.clients[key]; ok {
		return limiter
	}
	limiter := rate.NewLimiter(l.r, l.burst)
	l.clients[key] = limiter
	return limiter
}

func (l *Limiter) Allow(key string) bool {
	return l.getLimiter(key).Allow()
}
