"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
import sys
import psycopg2.extensions
import environ
import logging
from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import default_headers, default_methods
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Read .env file
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env'), overwrite=True)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)


# Allowed hosts & IP addresses
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

INTERNAL_IPS = env.list('INTERNAL_IPS', default=[])

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: settings.DEBUG,
}

CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=[])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'corsheaders', # CORS
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # REST Framework
    'rest_framework_simplejwt', # JWT
    'django_filters', # Django Filters
    'core.apps.CoreConfig',
    'authentication.apps.AuthenticationConfig',
    'blog.apps.BlogConfig',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar') # Django Debug Toolbar


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware', # GZip Compression
]

if DEBUG:
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware') # Django Debug Toolbar


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n', # Django Internationalization
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


ASGI_APPLICATION = 'backend.asgi.application'

WSGI_APPLICATION = 'backend.wsgi.application'

APPEND_SLASH = env.bool('APPEND_SLASH', default=True)


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': env.str('POSTGRES_ENGINE', default='django.db.backends.sqlite3'),
        'HOST': env.str('POSTGRES_HOST', default='localhost'),
        'PORT': env.str('POSTGRES_PORT', default='5432'),
        'USER': env.str('POSTGRES_USER', default='user'),
        'PASSWORD': env.str('POSTGRES_PASSWORD', default='password'),
        'NAME': env.str('POSTGRES_DB', default='db.sqlite3'),
        'CHARSET': env.str('POSTGRES_CHARSET', default='utf8'),
        'TIME_ZONE': env.str('POSTGRES_TIME_ZONE', default='UTC'),
        'CONN_HEALTH_CHECKS': env.bool('CONN_HEALTH_CHECKS', default=True),
        'CONN_MAX_AGE': env.int('CONN_MAX_AGE', default=0),
        'OPTIONS': {
            'isolation_level': psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED if env.str(
                'POSTGRES_ENGINE', default='django.db.backends.sqlite3') != 'django.db.backends.sqlite3' else None,
            'sslmode': env.str('POSTGRES_SSLMODE', default='disable'),
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en', _('English')),
    ('ar', _('Arabic')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/'),
]

TIME_ZONE = env.str('TIME_ZONE', default='UTC')

USE_I18N = True

USE_TZ = env.bool('USE_TZ', default=True)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = env.str('STATIC_URL', default='/static/')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')

MEDIA_URL = env.str('MEDIA_URL', default='/media/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Logging Configurations

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


# REST Framework Configurations

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authentication.jwt_auth.JWTCookieAuthentication',
    ),
    'NON_FIELD_ERRORS_KEY': 'non-field-errors',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': env.int('PAGE_SIZE', default=10),
}

if DEBUG:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += ('rest_framework.authentication.SessionAuthentication',) # For DRF Browsable API only


# Pagination Configurations

PAGINATION_PAGE_SIZE = 10
PAGINATION_MAX_PAGE_SIZE = 100
PAGINATION_ADMIN_PAGE_SIZE = 20


# Security Configurations

SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=False)

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=False)
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=False)


# CORS Configurations

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
CORS_ORIGIN_WHITELIST = env.list('CORS_ORIGIN_WHITELIST', default=[])
CORS_ALLOW_CREDENTIALS = env.bool('CORS_ALLOW_CREDENTIALS', default=True)
CORS_ALLOW_HEADERS = list(default_headers) + env.list('CORS_ALLOW_HEADERS', default=[])
CORS_ALLOW_METHODS = list(default_methods) + env.list('CORS_ALLOW_METHODS', default=[])


# JWT Configurations

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1), # Just for testing purposes, should be 5 minutes in production
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'JWT_CLAIM': 'jti',
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_OBTAIN_SERIALIZER': 'authentication.serializers.BaseTokenObtainPairSerializer',
    'TOKEN_REFRESH_SERIALIZER': 'authentication.serializers.CookieTokenRefreshSerializer',
}

JWT_AUTH_ACCESS_COOKIE_NAME = env.str('JWT_AUTH_ACCESS_COOKIE_NAME', default='access_token')
JWT_AUTH_ACCESS_COOKIE_PATH = env.str('JWT_AUTH_ACCESS_COOKIE_PATH', default='/')

JWT_AUTH_REFRESH_COOKIE_NAME = env.str('JWT_AUTH_REFRESH_COOKIE_NAME', default='refresh_token')
JWT_AUTH_REFRESH_COOKIE_PATH = env.str('JWT_AUTH_REFRESH_COOKIE_PATH', default='/')

JWT_AUTH_COOKIE_HTTPONLY = env.bool('JWT_AUTH_ACCESS_COOKIE_HTTPONLY', default=True)
JWT_AUTH_COOKIE_SECURE = env.bool('JWT_AUTH_ACCESS_COOKIE_SECURE', default=False)
JWT_AUTH_COOKIE_SAMESITE = env.str('JWT_AUTH_ACCESS_COOKIE_SAMESITE', default='Lax')


# Email Configurations

EMAIL_BACKEND = env.str('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env.str('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_TIMEOUT = env.int('EMAIL_TIMEOUT', default=10) # In seconds
EMAIL_HOST_NAME = env.str('EMAIL_HOST_NAME')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_SUBJECT_PREFIX = env.str('EMAIL_SUBJECT_PREFIX')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Miscellaneous Configurations

AUTH_USER_MODEL = 'authentication.User'
PASSWORD_RESET_TIMEOUT = env.int('PASSWORD_RESET_TIMEOUT', default=(60 * 60 * 24 * 3)) # 259200 seconds
DATETIME_FORMATS = {
    'timestamp': '%Y-%m-%dT%H:%M:%S%z',
}


# Redis Configurations

REDIS_HOST = env.str('REDIS_HOST', default='localhost')
REDIS_PORT = env.int('REDIS_PORT', default=6379)
REDIS_DB = env.int('REDIS_DB', default=0)
REDIS_PASSWORD = env.str('REDIS_PASSWORD', default=None)


# Celery Configuration

CELERY_ENABLE_UTC = env.bool('CELERY_ENABLE_UTC', default=False)
CELERY_TIMEZONE = env.str('CELERY_TIMEZONE', default='UTC')
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')


# Celery Beat Configurations

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# Channels Configurations

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(REDIS_HOST, REDIS_PORT)],
            'capacity': env.int('REDIS_CHANNEL_CAPACITY', default=100),
            'expiry': env.int('REDIS_CHANNEL_EXPIRY', default=60),
        },
    }
}
