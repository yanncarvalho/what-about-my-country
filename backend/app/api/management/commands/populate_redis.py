from django.core.management.base import BaseCommand
class Command(BaseCommand):
    help = 'Populate Redis'

    def handle(self, *args, **kwargs):
     self.stdout.write('start to populate Redis')
     from app.api.populate import Populate
     thread = Populate()
     thread.start()
     thread.join()
     self.stdout.write('finished Redis population')
