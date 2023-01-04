"""Test init"""
import os
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
os.environ.setdefault('APP_ENVIRONMENT', 'dev')
logging.disable(logging.CRITICAL)
logging.disable(logging.INFO)
logging.disable(logging.WARNING)
logging.disable(logging.ERROR)
