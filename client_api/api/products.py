import json

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from source.kafka_ import publish_to_kafka
from db.engine import get_async_db_session
from db.models import Product
from utils.utils import get_recommendations


router = APIRouter()


@router.get("/search/")
async def search_products(field_name: str, field_value: str, user_id: int = 1, session: AsyncSession = Depends(get_async_db_session)):  # Для получения рекомендаций необходима авторизация или user_agent, выходит за рамки круса поэтому захардкодила
    result = await Product.get_by_field(field_name, field_value, session)
    # await kafka_producer.send_message(message=json.dumps({"user_id": user_id, "field_name": field_name, "field_value": field_value}, ))
    await publish_to_kafka(message=json.dumps({"user_id": user_id, "field_name": field_name, "field_value": field_value}).encode('utf-8'))
    return {
        "products": result
    }


@router.get("/recommendations/")
async def get_recommendations_view(user_id: int = 1, session: AsyncSession = Depends(get_async_db_session)):
    list_recommendations = get_recommendations(user_id)
    return {
        "recommendations": list_recommendations
    }