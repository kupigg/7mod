from enum import Enum

import faust


class ProductFieldsForFiltering(str, Enum):
    NAME = "name"
    CATEGORY = "category"
    TAGS = "tags"
    BRAND = "brand"


class Price(faust.Record, serializer='json'):
    amount: float
    currency: str


class Stock(faust.Record, serializer='json'):
    available: int
    reserved: int


class Image(faust.Record, serializer='json'):
    url: str
    alt: str


class Specifications(faust.Record, serializer='json'):
    weight: str
    dimensions: str
    battery_life: str
    water_resistance: str


class Product(faust.Record, serializer='json'):
    product_id: str
    name: str
    price: Price
    tags: list[str]
    images: list[Image]
    stock: Stock
    specifications: Specifications
    created_at: str
    updated_at: str
    description: str = ""
    category: str = ""
    brand: str = ""
    sku: str = ""
    index: str = ""
    store_id: str = ""


class BlockedProduct(faust.Record, serializer='json'):
    field_name: ProductFieldsForFiltering
    field_value: str
