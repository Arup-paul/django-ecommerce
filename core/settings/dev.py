"""
Development settings — used on local machine.
Activated via DJANGO_SETTINGS_MODULE=core.settings.dev
"""
from .base import *  # noqa: F401,F403

# Force DEBUG on locally regardless of .env
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Print each email to the runserver terminal.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Allow Django to serve static/media in dev (handled by `runserver`)
INTERNAL_IPS = ['127.0.0.1']
