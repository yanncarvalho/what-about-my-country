import os
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
logging.disable(logging.CRITICAL)
logging.disable(logging.INFO)
logging.disable(logging.WARNING)
logging.disable(logging.ERROR)