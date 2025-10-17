import asyncio
from aiokafka import AIOKafkaProducer
from faststream import FastStream
from faststream.kafka import KafkaBroker

from core.settings import settings


broker = KafkaBroker(bootstrap_servers=settings.kafka.bootstrap_servers)
fast_stream_app = FastStream(broker)


@broker.publisher(topic=settings.kafka.topic_recommendations)
async def publish_to_kafka(message: bytes):
    async with broker:
        await broker.publish(message, settings.kafka.topic_recommendations)


# event_loop = asyncio.get_event_loop()


# class AsyncKafkaProducer:
#     def __init__(self, servers: list[str], topic: str):
#         self._producer = AIOKafkaProducer(bootstrap_servers=servers, loop=event_loop)
#         self._topic = topic

#     async def start(self):
#         await self._producer.start()

#     async def stop(self):
#         await self._producer.stop()

#     async def send_message(self, message: bytes):
#         await self.start()
#         try:
#             await self._producer.send(self._topic, message)
#         except Exception as e:
#             print(f"Failed to send message: {e}")
#         finally:
#             await self.stop()


# def get_kafka_producer(topic: str = settings.kafka.topic_recommendations) -> AsyncKafkaProducer:
#     return AsyncKafkaProducer(servers=[settings.kafka.bootstrap_servers], topic=topic)
