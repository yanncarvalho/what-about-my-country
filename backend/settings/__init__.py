import os

from .base import *

profile = os.getenv('DJANGO_ENVIRONMENT', 'dev')

if profile == 'prod':
   from .prod import *
else:
   from .dev import *
