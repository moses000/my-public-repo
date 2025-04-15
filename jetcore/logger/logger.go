package logger

import (
	"log"
)

type Logger struct{}

func New() *Logger {
	return &Logger{}
}

func (l *Logger) Info(msg string, args ...any) {
	log.Println("[INFO]", msg, args)
}

func (l *Logger) Warn(msg string, args ...any) {
	log.Println("[WARN]", msg, args)
}

func (l *Logger) Error(msg string, args ...any) {
	log.Println("[ERROR]", msg, args)
}
