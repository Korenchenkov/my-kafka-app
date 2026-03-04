my-kafka-app
A simple Python application demonstrating Apache Kafka integration with a producer and consumer. The project includes Docker setup for Kafka and Zookeeper, and can be deployed on Kubernetes.

Features
Kafka producer that sends "Hello, Kafka!" messages

Kafka consumer that listens and prints received messages

Docker Compose configuration for running Kafka and Zookeeper

Kubernetes manifests for deploying Kafka brokers (StatefulSet)

Ready-to-run containerized Python app

Prerequisites
Docker & Docker Compose

Python 3.10+ (if running locally)

Kubernetes cluster (optional, for K8s deployment)

kafka-python library (included in requirements.txt)

Getting Started
1. Clone the repository

git clone https://github.com/Korenchenkov/my-kafka-app.git
cd my-kafka-app

2. Start Kafka and Zookeeper with Docker Compose

docker-compose up -d
This starts:

Zookeeper on port 2181

Kafka broker on port 9092

Verify containers are running:


docker ps -a
3. Create a Kafka topic

docker exec -it kafka kafka-topics --create \
  --topic test-topic \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1
4. Build the Python app Docker image

docker build -t kafka-demo-app .
5. Run the app
The app both produces and consumes a message. Use --network host to connect to Kafka running on the host:


docker run --rm --network host kafka-demo-app
Expected output:

text
Message sent: RecordMetadata(topic='test-topic', partition=0, offset=0, ...)
Received: Hello, Kafka! from partition 0
Project Structure
text
.
ÜÄÄ app/
Å   ÜÄÄ Dockerfile
Å   ÜÄÄ requirements.txt
Å   ÑÄÄ main.py          # Producer + consumer logic
ÜÄÄ docker-compose.yml    # Kafka + Zookeeper services
ÜÄÄ kafka-demo-deployment.yaml  # Kubernetes StatefulSet for Kafka
ÑÄÄ README.md
Running Locally (without Docker)
Install dependencies:


pip install -r app/requirements.txt
Ensure Kafka is running (e.g., via Docker Compose as above).

Run the script:


python app/main.py
Kubernetes Deployment
The repository includes a StatefulSet for running Kafka brokers on Kubernetes:


kubectl apply -f kafka-demo-deployment.yaml
Note: This deploys Kafka brokers only. You also need Zookeeper and appropriate configurations. For production, consider using a Kafka operator or Helm chart.

License
This project is open source and available under the MIT License.