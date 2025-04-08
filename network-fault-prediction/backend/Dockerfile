# # Use Golang image to build the app
# FROM golang:1.18 AS builder

# # Set the working directory
# WORKDIR /app

# # Copy the Go files
# COPY . .

# # Build the Go app
# RUN go build -o app .

# # Start a new stage for the final image
# FROM gcr.io/distroless/base

# # Copy the built Go binary from the builder image
# COPY --from=builder /app/app /app

# # Set the command to run the Go app
# CMD ["/app"]

# Start with a base Go image
FROM golang:1.20-alpine as build

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the rest of the application files
COPY . .

# Build the Go app
RUN go build -o go-kafka-consumer .

# Start a new stage from scratch
FROM alpine:latest  

WORKDIR /root/

# Copy the pre-built binary from the previous build stage
COPY --from=build /app/go-kafka-consumer .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the executable
CMD ["./go-kafka-consumer"]

