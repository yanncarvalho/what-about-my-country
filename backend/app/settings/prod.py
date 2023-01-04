"""Production profile."""
import os

DEBUG = os.getenv('BACKEND_DEBUG').lower() == 'true'

SECRET_KEY = os.getenv('BACKEND_SECRET_KEY')

ALLOWED_HOSTS = [os.getenv('BACKEND_ALLOWED_HOSTS')]

#=---------------- CORS -----------------=#
CORS_ORIGIN_ALLOW_ALL = os.getenv('BACKEND_CORS_ORIGIN_ALLOW_ALL', 'true').lower() == 'true'


#=---------------- LOGGING SETTINGS -----------------=#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'log_file': {

            'class': 'logging.FileHandler',
            'filename': 'backend.log',
            'formatter': 'verbose',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['log_file'],
    },
    'app.api': {
        'handlers': ['log_file'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('BACKEND_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}
