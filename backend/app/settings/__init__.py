import os

from .base import *

profile = os.getenv('BACKEND_ENVIRONMENT')

if profile == 'prod':
   from .prod import *
else:
   from .dev import *
