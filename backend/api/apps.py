import os
from django.apps import AppConfig
from backend.api.factory import RedisFactory

class ApiConfig(AppConfig):
    name: str = 'backend.api'
    verbose_name: str = 'countries info api'

    def ready(self) -> None:
      if(os.environ.get("DJANGO_ENVIRONMENT") == 'prod'):
        RedisFactory.redis_connected_or_exception()


