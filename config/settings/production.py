from django.utils.translation import gettext_lazy as _

from config.settings.base import *


DEBUG = env.bool("FARABIN_DEBUG", default=False)

ALLOWED_HOSTS = env.list(
    "FARABIN_ALLOWED_HOSTS",
    default=["saramad.farabinbrand.com", "farabinback.farbinbrand.com", "0.0.0.0"],
)


INTERNAL_IPS = None


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "PASSWORD": env.get_value("FARABIN_DB_PASSWORD"),
        "NAME": env.get_value("FARABIN_DB_NAME"),
        "USER": env.get_value("FARABIN_DB_USER"),
        "HOST": env.get_value("FARABIN_DB_HOST"),
        "PORT": env.get_value("FARABIN_DB_PORT"),
    }
}

X_FRAME_OPTIONS = "ALLOWANY"
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
