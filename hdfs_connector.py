import uuid


from confluent_kafka import Consumer
from hdfs import InsecureClient
from client_api.core.settings import settings


if __name__ == "__main__":
    consumer_conf = {
        "bootstrap.servers": settings.kafka.bootstrap_servers[0],
        "group.id":  settings.kafka.group_id,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": True,
        "session.timeout.ms": 6_000,
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe(["test_topi"])
    hdfs_client = InsecureClient("http://localhost:9870", user="root")
    try:
        while True:
            msg = consumer.poll(0.1)
            if msg is None:
                continue
            if msg.error():
                print(f"Ошибка: {msg.error()}")
                continue

            value = msg.value().decode("utf-8")
            print(
                f"Получено сообщение: {value=}, "
                f"partition={msg.partition()}, offset={msg.offset()}"
            )
            hdfs_file = f"data/message_{uuid.uuid4()}"
            with hdfs_client.write(hdfs_file, encoding="utf-8") as writer:
                writer.write(value + "\n")
            print(f"Сообщение '{value=}' записано в HDFS по пути '{hdfs_file}'")
    finally:
        consumer.close()