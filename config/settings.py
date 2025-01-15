from kombu import Queue
from datetime import timedelta
from pathlib import Path
import environ
import os

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR)


SECRET_KEY = env("FARABIN_SECRET_KEY")

DEBUG = env("FARABIN_DEBUG")
# DEBUG = True


ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

PROJECT_APPS = [
    'ticket',
    'diagnostics',
    'core',
    'company',
]

THIRED_PARTY_APPS = [
    'django_celery_beat',
    'drf_spectacular',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'nested_admin',
]


INSTALLED_APPS += PROJECT_APPS + THIRED_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


ASGI_APPLICATION = 'config.asgi.application'


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'PASSWORD': env("FARABIN_DB_PASSWORD"),
            'NAME': env("FARABIN_DB_NAME"),
            'USER': env("FARABIN_DB_USER"),
            'HOST': env("FARABIN_DB_HOST"),
            'PORT': env("FARABIN_DB_PORT")
        }
    }
if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'PASSWORD': env("FARABIN_DB_PASSWORD"),
            'NAME': env("FARABIN_DB_NAME"),
            'USER': env("FARABIN_DB_USER"),
            'HOST': env("FARABIN_DB_HOST"),
            'PORT': env("FARABIN_DB_PORT")
        }
    }


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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

USE_L10N = True


LANGUAGES = [
    ('en-us', _('English')),

    ('fa', _('Persian')),
]

LOCALE_PATHS = [
    BASE_DIR/'locale',  # Global locale directory
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = BASE_DIR / 'static'

STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'core.User'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(weeks=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),

}


# Browser protections
X_FRAME_OPTIONS = 'ALLOWANY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# production
CORS_ALLOWED_ORIGINS = [
    "https://saramad.farabinbrand.com",
    "http://saramad.farabinbrand.com",
    "http://localhost:3000",
    "http://localhost:8000",
    "https://192.168.1.2:3000",
    "https://192.168.1.4:3000",
    "https://192.168.1.8:3000",
]

CELERY_QUEUES = (
    Queue('default', routing_key='task.default'),
    Queue('high_priority', routing_key='task.high_priority'),
)
CELERY_DEFAULT_QUEUE = 'default'

# CELERY_ROUTES = {
#     'tasks.high_priority_task': {'queue': 'high_priority', 'routing_key': 'task.high_priority'},
#     'tasks.default': {'queue': 'default', 'routing_key': 'task.default'},
# }

CELERY_RESULT_BACKEND = f'redis://{env("FARABIN_REDIS_HOST")}:{env(
    "FARABIN_REDIS_PORT")}/{env("FARABIN_REDIS_ASYNC_DATABASE")}'
CELERY_BROKER_URL = f'redis://{env("FARABIN_REDIS_HOST")}:{env(
    "FARABIN_REDIS_PORT")}/{env("FARABIN_REDIS_ASYNC_DATABASE")}'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TASK_ACKS_LATE = True

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Use database 1
        'LOCATION': f'redis://{env("FARABIN_REDIS_HOST")}:{env("FARABIN_REDIS_PORT")}/{env("FARABIN_REDIS_CACHE_DATABASE")}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'KEY_PREFIX': 'farabin_cache',
        },
        'TIMEOUT': 3*60,
    }
}

# HTTPS settings
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_BROWSER_XSS_FILTER = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_PRELOAD = True
# CSRF_COOKIE_SECURE = True
