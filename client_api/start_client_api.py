import uvicorn
from fastapi import FastAPI

from api.products import router
from core.settings import settings


app = FastAPI(
    title=settings.api.app_name
)

app.include_router(router, prefix=f"/{settings.api.version}/products", tags=["products"])


if __name__ == "__main__":
    uvicorn.run(
        "start_client_api:app",
        host=settings.api.url,
        port=settings.api.port
    )