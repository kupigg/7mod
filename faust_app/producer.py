import json

from confluent_kafka import Producer

from core.settings import settings


def send_message(producer: Producer, name_topic: str, message: dict, key: str = "key-1"):
    producer.produce(
        topic=name_topic,
        key=key,
        value=json.dumps(message),
    )


def get_test_products(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    conf = {
        "bootstrap.servers": settings.kafka.bootstrap_servers[0],
        "acks": "all",
        "retries": 3,
    }
    products = get_test_products("test_products.json")
    producer = Producer(conf)
    count = 0
    for product in products:
        count += 1
        send_message(producer, settings.kafka.products_publish_topic, message=product, key=f"key-{count}")
    producer.flush()
