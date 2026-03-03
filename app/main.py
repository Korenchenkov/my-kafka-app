from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable
import time

BOOTSTRAP_SERVERS = 'kafka:9092'
TOPIC = 'test-topic'
MAX_RETRIES = 5
RETRY_DELAY = 3  # seconds


def consume_message():
    consumer = None
    for attempt in range(MAX_RETRIES):
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=BOOTSTRAP_SERVERS,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='my-group',
                value_deserializer=lambda m: m.decode('utf-8')
            )
            break
        except NoBrokersAvailable:
            print(f"Consumer: no brokers available, retrying ({attempt + 1}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY)
    else:
        print("Consumer: failed to connect after max retries.")
        return

    try:
        for message in consumer:
            print(f"Received: {message.value} from partition {message.partition}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


def produce_message():
    producer = None
    for attempt in range(MAX_RETRIES):
        try:
            producer = KafkaProducer(
                bootstrap_servers=BOOTSTRAP_SERVERS,
                value_serializer=lambda v: v.encode('utf-8')
            )
            break
        except NoBrokersAvailable:
            print(f"Producer: no brokers available, retrying ({attempt + 1}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY)
    else:
        print("Producer: failed to connect after max retries.")
        return

    try:
        future = producer.send(TOPIC, 'Hello, Kafka!')
        result = future.get(timeout=10)
        print(f"Message sent: {result}")
    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        producer.close()


if __name__ == '__main__':
    produce_message()
    time.sleep(2)
    consume_message()
