import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "client_api"))
import json
from confluent_kafka import Consumer

from client_api.core.settings import settings
from client_api.db.engine import get_sync_db_session
from client_api.db.models import Product
from client_api.schema import ProductDTO


def save_product(message_json):
    product = ProductDTO.from_faust(message_json)
    session_generator = get_sync_db_session()
    session = next(session_generator)
    Product.save_product(session, product)


if __name__ == "__main__":
    consumer_conf = {
        "bootstrap.servers": settings.kafka.bootstrap_servers[0],
        "group.id": settings.kafka.group_id,
        "auto.offset.reset": "earliest",
    }

    try:
        consumer = Consumer(consumer_conf)
        consumer.subscribe([settings.kafka.topic_filtered_products])

        try:
            while True:
                message = consumer.poll(1)

                if message is None:
                    continue
                if message.error():
                    print(f"Ошибка при получении сообщения: {message.error()}")
                    continue

                key = message.key()
                if key:
                    key = key.decode("utf-8")
                value = message.value().decode("utf-8")
                message_json = json.loads(value)
                save_product(message_json)
                print(f"Получено сообщение:, value='{value}', {}")
        finally:
            consumer.close()
    except Exception as e:
        print(e)