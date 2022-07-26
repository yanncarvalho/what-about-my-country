from django.apps import AppConfig

class ApiConfig(AppConfig):
    name: str = 'api'
    verbose_name: str = "country api"

    def ready(self) -> None:
        from . import populate_db
        populate_db.countries()
        return super().ready()