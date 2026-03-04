# my-kafka-app

A simple Python application demonstrating Apache Kafka integration with a producer and consumer. The project includes Docker setup for Kafka and Zookeeper, a GitLab CI/CD pipeline, and can be deployed on Kubernetes.

---

## Features

- Kafka **producer** that sends `"Hello, Kafka!"` messages
- Kafka **consumer** that listens and prints received messages
- Docker Compose configuration for running Kafka and Zookeeper
- GitLab CI/CD pipeline with build, test, and deploy stages
- Kubernetes manifests for deploying Kafka brokers (StatefulSet)
- Ready-to-run containerized Python app

---

## Prerequisites

- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- Python 3.10+ *(if running locally)*
- Kubernetes cluster *(optional, for K8s deployment)*
- `kafka-python` library *(included in `requirements.txt`)*

---

## Project Structure

```
.
├── app/
│   └── main.py                    # Producer + consumer logic
├── tests/
│   └── unit/                      # Unit tests
├── .gitlab-ci.yml                 # GitLab CI/CD pipeline
├── docker-compose.yml             # Kafka + Zookeeper services
├── Dockerfile                     # App container image
├── kafka-demo-deployment.yaml     # Kubernetes StatefulSet for Kafka
└── README.md
```
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Korenchenkov/my-kafka-app.git
cd my-kafka-app
```

### 2. Start Kafka and Zookeeper with Docker Compose

```bash
docker-compose up -d
```

This starts:

| Service     | Port |
|-------------|------|
| Zookeeper   | 2181 |
| Kafka broker| 9092 |

Verify containers are running:

```bash
docker ps -a
```

### 3. Create a Kafka topic

```bash
docker exec -it kafka kafka-topics --create \
  --topic test-topic \
  --bootstrap-server localhost:9092 \
  --replication-factor 1 \
  --partitions 1
```

### 4. Build the Python app Docker image

```bash
docker build -t kafka-demo-app .
```

### 5. Run the app

The app both produces and consumes a message. It connects to Kafka via the `kafka-net` Docker network using the service name `kafka:9092`:

```bash
docker run --rm --network my-kafka-app_kafka-net kafka-demo-app
```

**Expected output:**

```
Message sent: RecordMetadata(topic='test-topic', partition=0, offset=0, ...)
Received: Hello, Kafka! from partition 0
```

---

## Running Locally (without Docker)

1. Install dependencies:

   ```bash
   pip install -r app/requirements.txt
   ```

2. Ensure Kafka is running (e.g., via Docker Compose as above).

3. Run the script:

   ```bash
   python app/main.py
   ```

> **Note:** When running locally, update `BOOTSTRAP_SERVERS` in [`app/main.py`](app/main.py) from `kafka:9092` to `localhost:9092`.

---

## CI/CD Pipeline (GitLab)

The [`.gitlab-ci.yml`](.gitlab-ci.yml) defines three stages:

| Stage    | Job                 | Description                                      |
|----------|---------------------|--------------------------------------------------|
| `build`  | `build`             | Builds and pushes the Docker image to the registry |
| `test`   | `unit_tests`        | Runs unit tests with `pytest`                    |
| `test`   | `integration_tests` | Spins up Kafka via Docker Compose and runs integration tests |
| `deploy` | `deploy`            | Deploys the image to the target environment      |

Pipelines run on the `master` and `develop` branches. The `deploy` job runs on `master` only.

---

## Kubernetes Deployment

The repository includes a StatefulSet for running Kafka brokers on Kubernetes:

```bash
kubectl apply -f kafka-demo-deployment.yaml
```

> **Note:** This deploys Kafka brokers only. You also need Zookeeper and appropriate configurations.  
> For production, consider using a Kafka operator or Helm chart (e.g., [Strimzi](https://strimzi.io/) or [Bitnami Kafka](https://artifacthub.io/packages/helm/bitnami/kafka)).

---

## License

This project is open source and available under the [MIT License](LICENSE).
