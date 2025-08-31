import os
import tempfile
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict

import environ  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore
from kombu import Queue  # type: ignore

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env.get_value("FARABIN_SECRET_KEY")

FARABIN_GEMINI_API_KEY = env.get_value("FARABIN_GEMINI_API_KEY")


INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
]


PROJECT_APPS = [
    "apps.questionnaire",
    "apps.management",
    "apps.packages",
    "apps.salesdata",
    "apps.finance",
    "apps.company",
    "apps.tickets",
    "apps.core",
    "apps.swot",
]
 
THIRED_PARTY_APPS = [
    "rest_framework_simplejwt",
    "django_lifecycle_checks",
    "django_celery_beat",
    "drf_spectacular",
    "rest_framework",
    'rest_framework.authtoken',
    "nested_admin",
    "corsheaders",
    'rest_framework_simplejwt.token_blacklist',
   
]

INSTALLED_APPS += PROJECT_APPS + THIRED_PARTY_APPS
    
MIDDLEWARE = [

    "apps.core.utils.ServiceIntegrity",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "fa"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_TZ = True

USE_L10N = True


LANGUAGES = [
    ("en-us", _("English")),
    ("fa", _("Persian")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = BASE_DIR / "static"

STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "core.User"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Short-lived for security
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # Longer for user convenience
    'ROTATE_REFRESH_TOKENS': True,                   # Issue new refresh token on refresh
    'BLACKLIST_AFTER_ROTATION': True,                # Blacklist old refresh tokens (requires db)
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',                            # Or 'RS256' for asymmetric keys
    'SIGNING_KEY': 'your-secret-key-here',           # Change to a strong secret (use env vars in prod)
    'AUTH_HEADER_TYPES': ('Bearer',),                # For header-based auth (fallback if not using cookies)
    'AUTH_COOKIE': 'access_token',                   # Cookie name for access token
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_SECURE': True,                      # True in production (HTTPS)
    'AUTH_COOKIE_SAMESITE': 'Lax',                   # Or 'Strict' for max security
    'REFRESH_COOKIE': 'refresh_token',               # Cookie name for refresh token
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Farabin API",
    "DESCRIPTION": "API Documentation for Farabin",
    "VERSION": "1.0.0",
    "CONTACT": {"name": "", "email": ""},
    "SERVE_INCLUDE_SCHEMA": True,
}


X_FRAME_OPTIONS = "ALLOWANY"

CORS_ALLOWED_ORIGINS = [
    "https://saramad.farabinbrand.com",
    "http://saramad.farabinbrand.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.1.4:3000",
    "http://localhost:8000",
    "https://localhost:8000",
    "http://127.0.0.1:8000",
    "https://192.168.1.2:3000",
    "https://192.168.1.4:3000",
    "https://192.168.1.8:3000",
]

CELERY_QUEUES = (
    Queue("default", routing_key="task.default"),
    Queue("high_priority", routing_key="task.high_priority"),
)
CELERY_DEFAULT_QUEUE = "default"
CELERY_RESULT_BACKEND = f"redis://{env.get_value('FARABIN_REDIS_HOST')}:{
    env.get_value('FARABIN_REDIS_PORT')
}/{env.get_value('FARABIN_REDIS_ASYNC_DATABASE')}"
CELERY_BROKER_URL = f"redis://{env.get_value('FARABIN_REDIS_HOST')}:{
    env.get_value('FARABIN_REDIS_PORT')
}/{env.get_value('FARABIN_REDIS_ASYNC_DATABASE')}"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CDN_HEALTH_CHECK_URL = env.get_value("FARABIN_CDN")
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TASK_ACKS_LATE = True

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{env.get_value('FARABIN_REDIS_HOST')}:{env.get_value('FARABIN_REDIS_PORT')}/{env.get_value('FARABIN_REDIS_CACHE_DATABASE')}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "KEY_PREFIX": "farabin_cache",
        },
        "TIMEOUT": 3 * 60,
    }
}


LOG_DIR = Path(tempfile.gettempdir()) / "saramad_logs"

os.makedirs(LOG_DIR, exist_ok=True) if not os.path.exists(LOG_DIR) else None
LOGGING: Dict[str, Any] = {
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
            "format": '{{"timestamp": "{asctime}", "level": "{levelname}", "message": "{message}"}}',
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

# For the custom file path exceptions
FILE_PATH_EXCEPTION_MODELS = ["OrganizationChartBase", "CompanyProfile", "User"]

# For retrieving of the files based on the company field
HUMAN_RESOURCE_FILE_FIELDS = {
    "general": ["__all__"],
}


# For creating the automatic logs based on the apps
APPS_TO_LOG = PROJECT_APPS

for app in APPS_TO_LOG:
    LOGGING["handlers"][f"{app}_logs_file"] = {  # type: ignore
        "level": "INFO",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": LOG_DIR / f"{app}_logs.log",
        "formatter": "verbose",
        "maxBytes": 5 * 1024 * 1024,  # 5 MB
        "backupCount": 3,
    }

    LOGGING["handlers"][f"{app}_errors_file"] = {  # type: ignore
        "level": "ERROR",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": LOG_DIR / f"{app}_errors.log",
        "formatter": "verbose",
        "maxBytes": 5 * 1024 * 1024,  # 5 MB
        "backupCount": 3,
    }

    LOGGING["loggers"][app] = {  # type: ignore
        "handlers": [f"{app}_logs_file", f"{app}_errors_file"],
        "level": "INFO",
        "propagate": False,
    }

LOGGING["handlers"]["rotating_file"] = {  # type: ignore
    "level": "INFO",
    "class": "logging.handlers.RotatingFileHandler",
    "filename": LOG_DIR / "rotating.log",
    "maxBytes": 1024 * 1024 * 5,
    "backupCount": 5,
    "formatter": "verbose",
}


COOLDOWN_PERIOD = timedelta(minutes=1, seconds=30)

CORS_ALLOW_CREDENTIALS = True   
