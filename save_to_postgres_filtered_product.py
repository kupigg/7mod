
import os
import time

from confluent_kafka import Consumer

from client_api.core.settings import settings


if __name__ == "__main__":

    consumer_conf = {
        "bootstrap.servers": settings.kafka.bootstrap_servers,
        "group.id": "test_group",
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

                key = message.key().decode("utf-8")
                value = message.value().decode("utf-8")
                offset = message.offset()
                print(f"Получено сообщение: key='{key}', value='{value}', {offset=}")
        finally:
            consumer.close()
    except Exception as e:
        print(e)