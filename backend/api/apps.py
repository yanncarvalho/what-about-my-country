import os
from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'backend.api'
    verbose_name = 'countries info api'
    def ready(self) -> None:
        from backend.populate_db import Populate
        Populate().start()