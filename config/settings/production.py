from config.settings.base import *  # noqa: F403

DEBUG = env.bool("FARABIN_DEBUG", default=False)  # noqa: F405

ALLOWED_HOSTS = env.list(  # noqa: F405
    "FARABIN_ALLOWED_HOSTS",
    default=["saramad.farabinbrand.com", "farabinback.farbinbrand.com", "0.0.0.0"],
)


INTERNAL_IPS = None


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "PASSWORD": env.get_value("FARABIN_DB_PASSWORD"),  # noqa: F405
        "NAME": env.get_value("FARABIN_DB_NAME"),  # noqa: F405
        "USER": env.get_value("FARABIN_DB_USER"),  # noqa: F405
        "HOST": env.get_value("FARABIN_DB_HOST"),  # noqa: F405
        "PORT": env.get_value("FARABIN_DB_PORT"),  # noqa: F405
    }
}

X_FRAME_OPTIONS = "ALLOWANY"
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True


# CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_PRELOAD = True
CSRF_COOKIE_SECURE = True
