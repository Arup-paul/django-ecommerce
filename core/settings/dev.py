"""
Development settings — used on local machine.
Activated via DJANGO_SETTINGS_MODULE=core.settings.dev
"""
from .base import *  # noqa: F401,F403

# Force DEBUG on locally regardless of .env
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Write each email to a .eml file under sent_emails/ (links stay on one unbroken
# line, unlike the console backend which soft-wraps at 76 chars).
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

# Allow Django to serve static/media in dev (handled by `runserver`)
INTERNAL_IPS = ['127.0.0.1']
