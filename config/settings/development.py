from django.utils.timezone import timedelta

from config.settings.base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
]

INTERNAL_IPS = ["127.0.0.1"]

MIDDLEWARE += [  # noqa: F405
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = ["http://localhost:5173"]

CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_SECURE=False
SESSION_COOKIE_SAMESITE=None
CSRF_COOKIE_SAMESITE=None
CSRF_COOKIE_SECURE=False