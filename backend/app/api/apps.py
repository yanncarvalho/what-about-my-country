import os
from django.apps import AppConfig
from app.api.factory import RedisFactory

class ApiConfig(AppConfig):
    name: str = 'app.api'
    verbose_name: str = 'countries info api'

    def ready(self) -> None:
      if(os.environ.get("APP_ENVIRONMENT") == 'prod'):
        RedisFactory.redis_connected_or_exception()


