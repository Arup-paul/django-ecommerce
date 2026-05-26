"""
Production settings — used on the live server.
Activated via DJANGO_SETTINGS_MODULE=core.settings.prod
"""
from .base import *  # noqa: F401,F403

DEBUG = False

# Security hardening (HTTPS-only deployment assumed)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'
X_FRAME_OPTIONS = 'DENY'

# Real SMTP — configure via .env on the server
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
