from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent


class ApiSettings(BaseModel):
    url: str = "127.0.0.1"
    port: int = 5003
    app_name: str = "products API"
    version: str = "v1"


class KafkaSettings(BaseModel):
    bootstrap_servers: list = ["localhost:19092"]
    group_id: str = "test_group"
    products_publish_topic: str = "publish_products"
    topic_blocked_teg_products: str = "blocked_teg_products"
    topic_for_prepare_recommendations: str = "prepare_recommendations"
    topic_recommendations: str = "recommendations"
    topic_filtered_products: str = "filtered_products"


class PostgresSettings(BaseModel):
    username: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: int = 5432
    db_name: str = "products_db"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    @property
    def url_sync(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file_encoding='utf-8',
        env_file=BASE_DIR / ".env"
    )

    api: ApiSettings = ApiSettings()
    postgres: PostgresSettings = PostgresSettings()
    kafka: KafkaSettings = KafkaSettings()


settings = Settings()
print(settings.postgres.url)