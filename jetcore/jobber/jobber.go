package jobber

import (
	"time"
)

type JobFunc func()

type Jobber struct{}

func New() *Jobber {
	return &Jobber{}
}

func (j *Jobber) Every(d time.Duration, f JobFunc) {
	go func() {
		for range time.Tick(d) {
			go f()
		}
	}()
}
