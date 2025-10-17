from datetime import datetime
import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy import JSON, Integer, String, Float, DateTime, select, ARRAY
from sqlalchemy.sql import func

from client_api.schema import ProductDTO
from db.engine import Base


class OrmMixin:
    @classmethod
    async def get_by_field(cls, field_name: str, field_value: str, session: AsyncSession):
        query = select(cls).filter(getattr(cls, field_name) == field_value)
        result = await session.execute(query)
        result = result.scalars().all()
        return result

    @classmethod
    async def create(cls, session, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj


class MixinDate(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Product(MixinDate, OrmMixin):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    price_amount: Mapped[float] = mapped_column(Float)
    price_currency: Mapped[str] = mapped_column(String(10))
    category: Mapped[str] = mapped_column(String(50))
    brand: Mapped[str] = mapped_column(String(50))
    stock_available: Mapped[int] = mapped_column(Integer)
    stock_reserved: Mapped[int] = mapped_column(Integer)
    sku: Mapped[str] = mapped_column(String(50), unique=True)
    tags: Mapped[list] = mapped_column(ARRAY(String), nullable=True)
    images: Mapped[str] = mapped_column(String, nullable=True)  # fix type field
    specifications_weight: Mapped[str] = mapped_column(String(10), nullable=True)
    specifications_dimensions: Mapped[str] = mapped_column(String(100), nullable=True)
    specifications_battery_life: Mapped[str] = mapped_column(nullable=True)
    specifications_water_resistance: Mapped[str] = mapped_column(nullable=True)
    index: Mapped[str]
    store_id: Mapped[str]

    @classmethod
    def save_product(cls, session: AsyncSession | Session, product: ProductDTO):
        obj = cls()
        for key, value in product.model_dump().items():
            if key == 'images':
                value = json.dumps(value)
            setattr(obj, key, value)
        session.add(obj)
        session.commit()
        session.refresh(obj)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
