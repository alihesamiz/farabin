from django.utils.translation import gettext_lazy as _

from config.settings.base import *


DEBUG = env.bool("FARABIN_DEBUG", default=False)

ALLOWED_HOSTS = env.list("FARABIN_ALLOWED_HOSTS", default=[
    "saramad.farabinbrand.com", "farabinback.farbinbrand.com", "0.0.0.0"])

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

INTERNAL_IPS = None

PROJECT_APPS = [
    'management',
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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'PASSWORD': env.get_value("FARABIN_DB_PASSWORD"),
        'NAME': env.get_value("FARABIN_DB_NAME"),
        'USER': env.get_value("FARABIN_DB_USER"),
        'HOST': env.get_value("FARABIN_DB_HOST"),
        'PORT': env.get_value("FARABIN_DB_PORT")
    }
}

X_FRAME_OPTIONS = 'ALLOWANY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True


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


SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_PRELOAD = True
CSRF_COOKIE_SECURE = True


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
