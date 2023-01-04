"""Django Command implementation"""
from django.core.management.base import BaseCommand
from app.api.models_country import Country

class Command(BaseCommand):
    """implementation of BaseCommand"""
    help = 'Populate Redis'

    # pylint: disable=unused-argument
    def handle(self, *args, **kwargs):
        self.stdout.write('start to populate Redis')
        thread = Country.trigger_save_all_countries()
        thread.start()
        thread.join()
        self.stdout.write('finished Redis population')
