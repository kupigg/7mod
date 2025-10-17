from pydantic import BaseModel, validator, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class ProductDTO(BaseModel):
    id: Optional[int] = None
    product_id: str
    name: str
    description: Optional[str] = None
    price_amount: float
    price_currency: str
    category: str
    brand: str
    stock_available: int
    stock_reserved: int
    sku: str
    tags: Optional[list] = None
    images: Optional[list] = None
    specifications_weight: Optional[str] = None
    specifications_dimensions: Optional[str] = None
    specifications_battery_life: Optional[str] = None
    specifications_water_resistance: Optional[str] = None
    index: str
    store_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_faust(cls, data: str) -> "ProductDTO":
        prepare_data = {}
        for key, value in data.items():
            if '__' in key:
                continue
            prepare_data[key] = value
        processed_data = {
            'product_id': prepare_data.get('product_id'),
            'name': prepare_data.get('name'),
            'description': prepare_data.get('description'),
            'price_amount': prepare_data.get('price').get('amount'),
            'price_currency': prepare_data.get('price').get('currency'),
            'category': prepare_data.get('category'),
            'brand': prepare_data.get('brand'),
            'stock_available': prepare_data.get('stock').get('available'),
            'stock_reserved': prepare_data.get('stock').get('reserved'),
            'sku': prepare_data.get('sku'),
            'tags': prepare_data.get('tags'),
            'images': prepare_data.get('images'),
            'specifications_weight': prepare_data.get('specifications').get('weight'),
            'specifications_dimensions': prepare_data.get('specifications').get('dimensions'),
            'specifications_battery_life': prepare_data.get('specifications').get('battery_life'),
            'specifications_water_resistance': prepare_data.get('specifications').get('water_resistance'),
            'index': prepare_data.get('index'),
            'store_id': prepare_data.get('store_id'),
            'created_at': prepare_data.get('created_at'),
            'updated_at': prepare_data.get('updated_at'),
        }
        return cls(**processed_data)