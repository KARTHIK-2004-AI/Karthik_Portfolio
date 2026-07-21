"""
Production settings - for PythonAnywhere deployment
"""
from .base import *
import dj_database_url

DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed Hosts - default to PythonAnywhere domain & localhost if not set
raw_hosts = config('ALLOWED_HOSTS', default='karthikaarupalli.pythonanywhere.com,localhost,127.0.0.1,.pythonanywhere.com')
ALLOWED_HOSTS = [h.strip() for h in raw_hosts.split(',') if h.strip()]

# Database - PostgreSQL for production (or SQLite fallback)
db_url = config('DATABASE_URL', default=None)
if db_url:
    DATABASES = {
        'default': dj_database_url.config(default=db_url, conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# CORS
cors_raw = config('CORS_ALLOWED_ORIGINS', default='')
CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_raw.split(',') if origin.strip()]
if not CORS_ALLOWED_ORIGINS:
    CORS_ALLOW_ALL_ORIGINS = True

# PythonAnywhere reverse proxy header for HTTPS detection
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security settings
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
