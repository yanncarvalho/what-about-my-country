from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'backend.api'
    verbose_name = 'countries info api'
    start = False
    def ready(self) -> None:
        if not self.start:
            self.start = True
            from backend import populate_db
            populate_db.countries()

