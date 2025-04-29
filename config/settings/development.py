from django.utils.translation import gettext_lazy as _

from config.settings.base import *

DEBUG = True

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
    'management',
    'packages',
    'finance',
    'company',
    'request',
    'tickets',
    'core',
]

THIRED_PARTY_APPS = [
    'rest_framework_simplejwt',
    'django_celery_beat',
    'graphene_django',
    'drf_spectacular',
    'rest_framework',
    'nested_admin',
    'corsheaders',
    'debug_toolbar']

INSTALLED_APPS += PROJECT_APPS + THIRED_PARTY_APPS

INTERNAL_IPS = ["127.0.0.1"]

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
    'debug_toolbar.middleware.DebugToolbarMiddleware',]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}


# For creating the automatic logs based on the apps
APPS_TO_LOG = PROJECT_APPS

for app in APPS_TO_LOG:
    LOGGING["handlers"][f"{app}_logs_file"] = {
        "level": "INFO",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": LOG_DIR / f"{app}_logs.log",
        "formatter": "verbose",
        "maxBytes": 5 * 1024 * 1024,  # 5 MB
        "backupCount": 3,
    }

    LOGGING["handlers"][f"{app}_errors_file"] = {
        "level": "ERROR",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": LOG_DIR / f"{app}_errors.log",
        "formatter": "verbose",
        "maxBytes": 5 * 1024 * 1024,  # 5 MB
        "backupCount": 3,
    }

    LOGGING["loggers"][app] = {
        "handlers": [f"{app}_logs_file", f"{app}_errors_file"],
        "level": "INFO",
        "propagate": False,
    }

LOGGING["handlers"]["rotating_file"] = {
    "level": "INFO",
    "class": "logging.handlers.RotatingFileHandler",
    "filename":  LOG_DIR/"rotating.log",
    "maxBytes": 1024 * 1024 * 5,
    "backupCount": 5,
    "formatter": "verbose",
}
