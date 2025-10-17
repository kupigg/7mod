from confluent_kafka import Producer

from core.settings import settings
from producer import send_message


if __name__ == "__main__":
    conf = {
        "bootstrap.servers": settings.kafka.bootstrap_servers[0],
        "acks": "all",
        "retries": 3,
    }
    test_blocked_product = {
        "field_name": "category",
        "field_value": "Электроника",
    }
    producer = Producer(conf)
    send_message(producer, settings.kafka.topic_blocked_teg_products, message=test_blocked_product, key=f"test")
    producer.flush()
