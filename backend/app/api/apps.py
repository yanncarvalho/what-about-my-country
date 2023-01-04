"""Django app config"""
import os
from django.apps import AppConfig
from app.api.factory import RedisFactory


class ApiConfig(AppConfig):
    """Class representing a Django application and its configuration."""
    name: str = 'app.api'
    verbose_name: str = 'countries info api'

    def ready(self) -> None:
        """Initialize when django starts"""
        if os.environ.get("APP_ENVIRONMENT") == 'prod':
            RedisFactory.redis_connected_or_exception()
