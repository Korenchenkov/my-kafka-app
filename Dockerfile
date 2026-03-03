FROM python:3.10.2-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV KAFKA_BROKER=localhost:9092

CMD ["python", "app/main.py"]