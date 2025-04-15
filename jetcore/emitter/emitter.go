package emitter

import "sync"

type Listener func(data any)

type Emitter struct {
	listeners map[string][]Listener
	mu        sync.RWMutex
}

func New() *Emitter {
	return &Emitter{listeners: make(map[string][]Listener)}
}

func (e *Emitter) On(event string, fn Listener) {
	e.mu.Lock()
	defer e.mu.Unlock()
	e.listeners[event] = append(e.listeners[event], fn)
}

func (e *Emitter) Emit(event string, data any) {
	e.mu.RLock()
	defer e.mu.RUnlock()
	for _, fn := range e.listeners[event] {
		go fn(data)
	}
}
