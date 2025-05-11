from datetime import timedelta
from pathlib import Path
import tempfile
import environ
import os

from kombu import Queue

from django.utils.translation import gettext_lazy as _


BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR/".env")

SECRET_KEY = env.get_value("FARABIN_SECRET_KEY")

FARABIN_COHERE_API_KEY = env.get_value("FARABIN_COHERE_API_KEY")
FARABIN_GEMINI_API_KEY = env.get_value("FARABIN_GEMINI_API_KEY")

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
    BASE_DIR/'locale',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = BASE_DIR / 'static'

STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'

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

GRAPHENE = {
    "SCHEMA": "management.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}
GRAPHQL_JWT = {
    # 'JWT_PAYLOAD_HANDLER': 'management.utils.jwt_payload',
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]


SPECTACULAR_SETTINGS = {
    'TITLE': 'Farabin API',
    'DESCRIPTION': 'API Documentation for Farabin Saramad',
    'VERSION': '1.0.0',
    'CONTACT': {"name": "Ahmad Asadi", "email": "madassandd@gmail.com"},
    'SERVE_INCLUDE_SCHEMA': True,
}


X_FRAME_OPTIONS = 'ALLOWANY'

CORS_ALLOWED_ORIGINS = [
    "https://saramad.farabinbrand.com",
    "http://saramad.farabinbrand.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.4:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://192.168.1.2:3000",
    "https://192.168.1.4:3000",
    "https://192.168.1.8:3000",
]

CELERY_QUEUES = (
    Queue('default', routing_key='task.default'),
    Queue('high_priority', routing_key='task.high_priority'),
)
CELERY_DEFAULT_QUEUE = 'default'
CELERY_RESULT_BACKEND = f'redis://{env.get_value("FARABIN_REDIS_HOST")}:{env.get_value(
    "FARABIN_REDIS_PORT")}/{env.get_value("FARABIN_REDIS_ASYNC_DATABASE")}'
CELERY_BROKER_URL = f'redis://{env.get_value("FARABIN_REDIS_HOST")}:{env.get_value(
    "FARABIN_REDIS_PORT")}/{env.get_value("FARABIN_REDIS_ASYNC_DATABASE")}'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TASK_ACKS_LATE = True

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{env.get_value("FARABIN_REDIS_HOST")}:{env.get_value("FARABIN_REDIS_PORT")}/{env.get_value("FARABIN_REDIS_CACHE_DATABASE")}',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'KEY_PREFIX': 'farabin_cache',
        },
        'TIMEOUT': 3*60,
    }
}


LOG_DIR = Path(tempfile.gettempdir()) / "saramad_logs"

os.makedirs(LOG_DIR, exist_ok=True) if not os.path.exists(LOG_DIR) else None


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {module} {process:d} {thread:d} - {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "json": {  # Structured JSON logging (useful for external logging systems)
            "format": "{{\"timestamp\": \"{asctime}\", \"level\": \"{levelname}\", \"message\": \"{message}\"}}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "django.log",
            "formatter": "verbose",
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 3,
        },
        "error_file": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "errors.log",
            "formatter": "verbose",
            "maxBytes": 5 * 1024 * 1024,  # 5 MB
            "backupCount": 3,
        },
        "json_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "log.json",
            "formatter": "json",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 3,
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["error_file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "config": {
            "handlers": ["console", "file", "json_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

# For automatically adding apps into the request type
APP_REQUEST_TYPES = ['finance', 'management']


# For the custom file path exceptions
FILE_PATH_EXCEPTION_MODELS = ["OrganizationChartBase"]


# For retrievong of the files based on the company field
HUMAN_RESOURCE_FILE_FIELDS = {
    "general": ["__all__"],
}
