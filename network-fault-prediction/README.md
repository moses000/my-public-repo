# Network Fault Prediction AI Models

This repository contains a solution for predicting network faults and recommending solutions in a telecommunications environment. The system is composed of a **backend service written in Go** and **machine learning models developed in Python**, along with **Kafka** for real-time data streaming and **Kubernetes** for scalability.

The project aims to reduce downtime by predicting faults with high accuracy, enabling **Field Maintenance Engineers (FMEs)** to take quick corrective actions. This solution is designed to scale and handle high-throughput real-time data with low latency, ensuring critical network operations are handled efficiently.

## Problem Statement

Telecommunication networks often experience unpredicted faults that can cause significant downtime. Identifying the root cause of these faults and resolving them efficiently is critical for maintaining the reliability of the network. 

## Solution

This solution uses **Kafka** to stream real-time data, which is then consumed by backend services written in **Go** and **Python** for real-time fault prediction. The architecture is designed to scale using **Kubernetes** for managing the services, including Kafka consumers.

### Key Components:
- **Go Backend Service**: Scalable backend services built with **Go** to process large datasets in real time. The backend fetches data from various network sources, preprocesses it, and sends it to the machine learning model for predictions.
- **Machine Learning Model**: **Python-based model** that leverages **supervised learning** techniques and **data augmentation** to predict network faults and recommend corrective solutions. 
- **Kafka**: A distributed stream processing platform used to send and receive real-time data.
- **Kubernetes**: Used to deploy and scale the Kafka consumers (Go and Python microservices) dynamically based on system load.

### Key Features:
- **Real-time Data Processing**: Go backend services consume and process Kafka stream data in real time, ensuring fast and reliable predictions.
- **Fault Prediction Model**: The Python-based machine learning model is trained to predict network faults and recommend solutions to engineers.
- **Scalable Architecture**: With Kubernetes, the system scales automatically to handle large volumes of real-time data.
- **Kafka Integration**: Kafka ensures real-time, distributed data streaming, making the system responsive to changing network conditions.

### Technologies Used:
- **Go**: For building scalable backend services that process and handle real-time data streams.
- **Python**: For developing and training the machine learning model to predict network faults.
- **Scikit-learn**: For machine learning model training.
- **Pandas & NumPy**: For data manipulation and computations in the Python model.
- **Kafka**: For real-time message streaming and processing.
- **Docker**: For containerizing services.
- **Kubernetes**: For orchestrating and scaling services in a containerized environment.

## How to Run the Project

### Prerequisites:
- **Go** (v1.16 or higher)
- **Python** (v3.7 or higher)
- **Pip** (Python package manager)
- **Docker**: To build and run containerized applications.
- **Kubernetes**: A Kubernetes cluster (use Minikube for local development or any cloud-based Kubernetes service).
- **kubectl**: Kubernetes command-line tool for managing the cluster.
- **Kafka**: A running Kafka instance. You can use **Helm** to deploy Kafka on Kubernetes or run it locally.

### Backend Setup:

1. Clone the repository.
   ```bash
   git clone https://github.com/moses000/my-public-repo.git/network-fault-prediction
   cd network-fault-prediction
   ```

2. Navigate to the **backend** directory for the Go and Python consumers.
   ```bash
   cd backend
   ```

#### 2.1 Go Consumer Setup:
- **Docker Build**: 
  ```bash
  cd go-consumer
  docker build -t go-kafka-consumer/go-kafka-consumer .
  ```

- **Kubernetes Deployment**:
  ```bash
  kubectl apply -f kubernetes/go-consumer-deployment.yaml
  kubectl apply -f kubernetes/go-consumer-service.yaml
  kubectl apply -f kubernetes/go-consumer-hpa.yaml  # Horizontal Pod Autoscaling
  ```

#### 2.2 Python Consumer Setup:
- **Docker Build**:
  ```bash
  cd python-consumer
  docker build -t python-kafka-consumer/python-kafka-consumer .
  ```

- **Kubernetes Deployment**:
  ```bash
  kubectl apply -f kubernetes/python-consumer-deployment.yaml
  kubectl apply -f kubernetes/python-consumer-service.yaml
  kubectl apply -f kubernetes/python-consumer-hpa.yaml  # Horizontal Pod Autoscaling
  ```

### Kafka Setup:

You can deploy Kafka using **Helm** for an easy setup:
```bash
helm install kafka bitnami/kafka
```

Or manually with YAML files in the `kubernetes` folder:
```bash
kubectl apply -f kubernetes/kafka-deployment.yaml
```

### Scaling with Kubernetes:

Once the consumers are deployed, Kubernetes can automatically scale them based on CPU usage. Check the Horizontal Pod Autoscalers (HPA) by running:
```bash
kubectl get hpa
```

You can also scale the pods manually:
```bash
kubectl scale deployment go-consumer --replicas=3
kubectl scale deployment python-consumer --replicas=3
```

---

## Monitoring

- **View Kafka Logs**: You can monitor Kafka's performance by viewing the pod logs:
  ```bash
  kubectl logs <kafka-pod-name>
  ```

- **View Consumer Logs**:
  ```bash
  kubectl logs <go-consumer-pod-name>
  kubectl logs <python-consumer-pod-name>
  ```

---

## Contributing

Feel free to fork this project, open issues, or submit pull requests. If you have any suggestions or improvements, feel free to reach out!

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Steps to Upload to GitHub:

1. **Initialize Git** in your project folder:
   ```bash
   git init
   ```

2. **Add the remote repository**:
   ```bash
   git remote add origin <your-github-repository-url>
   ```

3. **Stage and Commit the Files**:
   ```bash
   git add .
   git commit -m "Initial commit with Network Fault Prediction solution and Kafka microservices"
   ```

4. **Push to GitHub**:
   ```bash
   git push -u origin master
   ```