from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate Redis'

    def handle(self, *args, **kwargs):
     self.stdout.write('start to populate Redis')
     from app.api.populate import Populate
     Populate().start()
