import faust

from core.settings import settings
from schemas import BlockedProduct, Product
from utils import check_product_is_blocked


app = faust.App(
    "simple-faust-app",
    broker=settings.kafka.bootstrap_servers[0],
)

blocked_product_table = app.Table(
    "blocked_product_table",
    partitions=1,
    default=list
)

product_of_filtering_published_product = app.topic(settings.kafka.products_publish_topic, key_type=str, value_type=Product)
blocked_products = app.topic(settings.kafka.topic_blocked_teg_products, key_type=str, value_type=BlockedProduct)
filtered_product_topic = app.topic(settings.kafka.topic_filtered_products, key_type=str, value_type=Product)


@app.agent(product_of_filtering_published_product)
async def process_message(stream):
    message: Product
    async for message in stream:
        is_blocked = await check_product_is_blocked(blocked_product_table, message)
        if not is_blocked:
            await filtered_product_topic.send(value=message)
            continue


@app.agent(blocked_products)
async def process_block_products(stream):
    message: BlockedProduct
    async for message in stream:
        block_products_log = blocked_product_table.get(message.field_name) or []
        block_products_log.append(message.field_value)
        blocked_product_table[message.field_name] = block_products_log
