from pydantic_settings import BaseSettings, SettingsConfigDict

from redis import asyncio as aioredis
from celery import Celery

class RedisSettings(BaseSettings):
    PORT: int

    model_config = SettingsConfigDict(env_file="src/env/database.env")
    
redis_settings = RedisSettings()
redis_url = f'redis://redis:{redis_settings.PORT}/0'

celery_app = Celery("celery_app", broker=redis_url, backend=redis_url)
celery_app.conf.update(
    broker_url=redis_url,
    result_backend=redis_url,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    include=[
        "src.tasks.tasks"
    ]
)
