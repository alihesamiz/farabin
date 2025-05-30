# Django Config Module Documentation : Farabin Saramad

## Overview

The **Config Module** serves as the central configuration hub for the Farabin Saramad Django application. It defines project-wide settings, URL routing, Celery task scheduling, and a utility view for serving authenticated media files. The module is split into development and production environments, leveraging environment variables for flexibility and security. It supports internationalization, REST and GraphQL APIs, caching, logging, and asynchronous task processing with Celery.

---

## Module Structure

The Config Module consists of the following files:

- **`settings.base.py`**: Base Django settings, including environment variables, authentication, REST framework, JWT, Celery, caching, and logging.
- **`settings.development.py`**: Development-specific settings with SQLite and debugging tools.
- **`settings.production.py`**: Production settings with PostgreSQL and enhanced security.
- **`celery.py`**: Configures Celery for task scheduling and execution.
- **`urls.py`**: Defines URL patterns for admin, app endpoints, and static/media files.
- **`views.py`**: Implements a view for serving authenticated media files.

---

## Configuration Details

### Base Settings (`settings.base.py`)

- **Environment**:
  - Uses `django-environ` to load `.env` file from `BASE_DIR`.
  - Keys: `SECRET_KEY`, `FARABIN_COHERE_API_KEY`, `FARABIN_GEMINI_API_KEY`.
- **Templates**:
  - Backend: `DjangoTemplates`.
  - Context Processors: Debug, request, auth, messages.
- **Applications**:
  - WSGI: `config.wsgi.application`.
  - ASGI: `config.asgi.application`.
- **Authentication**:
  - Custom User Model: `core.User`.
  - Password Validators: User attribute similarity, minimum length, common password, numeric password.
  - REST Framework:
    - Authentication: `rest_framework_simplejwt.JWTAuthentication`.
    - Schema: `drf_spectacular.openapi.AutoSchema`.
  - Simple JWT:
    - Access Token Lifetime: 1 day.
    - Refresh Token Lifetime: 1 week.
    - Features: Rotate refresh tokens, blacklist after rotation, update last login.
    - Header: `Bearer`.
  - GraphQL:
    - Schema: `management.schema.schema`.
    - Middleware: `graphql_jwt.middleware.JSONWebTokenMiddleware`.
    - JWT Prefix: `JWT`.
  - Backends: `graphql_jwt.backends.JSONWebTokenBackend`, `django.contrib.auth.backends.ModelBackend`.
- **Internationalization**:
  - Language Code: `fa` (Persian).
  - Time Zone: `Asia/Tehran`.
  - Supported Languages: Persian (`fa`), English (`en-us`).
  - Locale Paths: `BASE_DIR/locale`.
  - Features: `USE_I18N`, `USE_TZ`, `USE_L10N` enabled.
- **Static and Media Files**:
  - Static: `STATIC_ROOT` (`BASE_DIR/static`), `STATIC_URL` (`/static/`), `CompressedManifestStaticFilesStorage`.
  - Media: `MEDIA_ROOT` (`BASE_DIR/media`), `MEDIA_URL` (`/media/`).
- **Database**:
  - Default Auto Field: `django.db.models.BigAutoField`.
- **API Documentation**:
  - Tool: `drf_spectacular`.
  - Title: "Farabin API".
  - Description: "API Documentation for Farabin Saramad".
  - Version: `1.0.0`.
  - Contact: Ahmad Asadi ([madassandd@gmail.com]).
- **CORS**:
  - Allowed Origins: Production domains (`saramad.farabinbrand.com`), localhost, and specific IPs.
- **Celery**:
  - Queues: `default`, `high_priority`.
  - Broker/Result Backend: Redis (configured via `FARABIN_REDIS_HOST`, `FARABIN_REDIS_PORT`, `FARABIN_REDIS_ASYNC_DATABASE`).
  - Settings: Reject tasks on worker loss, 1-hour result expiry, late acknowledgments, connection retry on startup.
- **Caching**:
  - Backend: `django_redis.cache.RedisCache`.
  - Location: Redis (`FARABIN_REDIS_HOST`, `FARABIN_REDIS_PORT`, `FARABIN_REDIS_CACHE_DATABASE`).
  - Options: `DefaultClient`, `farabin_cache` prefix, 3-minute timeout.
- **Logging**:
  - Directory: `/tmp/saramad_logs`.
  - Formatters:
    - `verbose`: Detailed with timestamp, level, name, module, process, thread.
    - `simple`: Level and message.
    - `json`: Structured JSON format.
  - Handlers:
    - `console`: Debug level, simple format.
    - `file`: Warning level, `django.log`, 5MB, 3 backups, verbose format.
    - `error_file`: Error level, `errors.log`, 5MB, 3 backups, verbose format.
    - `json_file`: Info level, `log.json`, 5MB, 3 backups, JSON format.
    - `mail_admins`: Error level, emails admins.
  - Loggers:
    - `django`: Console, file, info level.
    - `django.request`: Error file, mail admins, error level.
    - `config`: Console, file, JSON file, debug level.
- **Custom Settings**:
  - `APP_REQUEST_TYPES`: `["finance", "management"]` for dynamic request handling.
  - `FILE_PATH_EXCEPTION_MODELS`: `["OrganizationChartBase"]` for file path exceptions.
  - `HUMAN_RESOURCE_FILE_FIELDS`: Configures file retrieval (`general: ["__all__"]`).

### Development Settings (`settings.development.py`)

- **Debug**: Enabled (`True`).
- **Allowed Hosts**: All (`*`).
- **Database**:
  - Engine: SQLite (`BASE_DIR/db.sqlite3`).
- **Installed Apps**:
  - Core: Django admin, auth, contenttypes, sessions, messages, staticfiles, humanize.
  - Project Apps: `management`, `packages`, `finance`, `company`, `request`, `tickets`, `core`.
  - Third-Party: `rest_framework_simplejwt`, `django_lifecycle_checks`, `django_celery_beat`, `drf_spectacular`, `rest_framework`, `debug_toolbar`, `nested_admin`, `corsheaders`, `admin_interface`, `colorfield`.
- **Middleware**:
  - Includes `django.middleware.locale.LocaleMiddleware`, `whitenoise.middleware.WhiteNoiseMiddleware`, `corsheaders.middleware.CorsMiddleware`, `debug_toolbar.middleware.DebugToolbarMiddleware`.
- **Internal IPs**: `127.0.0.1` for debug toolbar.
- **Logging**:
  - Adds app-specific handlers for each project app (e.g., `company_logs.log`, `company_errors.log`).
  - Rotating file: `rotating.log`, 5MB, 5 backups, verbose format.

### Production Settings (`settings.production.py`)

- **Debug**: Disabled by default (`FARABIN_DEBUG` environment variable).
- **Allowed Hosts**: `saramad.farabinbrand.com`, `farabinback.farbinbrand.com`, `0.0.0.0` (configurable via `FARABIN_ALLOWED_HOSTS`).
- **Database**:
  - Engine: PostgreSQL.
  - Credentials: `FARABIN_DB_PASSWORD`, `FARABIN_DB_NAME`, `FARABIN_DB_USER`, `FARABIN_DB_HOST`, `FARABIN_DB_PORT`.
- **Installed Apps**:
  - Same as development, excluding `debug_toolbar`.
- **Middleware**:
  - Same as development, excluding `debug_toolbar.middleware.DebugToolbarMiddleware`.
- **Security**:
  - `X_FRAME_OPTIONS`: `ALLOWANY`.
  - HSTS: 1-year duration, include subdomains, preload.
  - Secure Cookies: `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`.
  - SSL Redirect: Enabled.
  - XSS Filter: Enabled (`SECURE_BROWSER_XSS_FILTER`).
  - Content Type Nosniff: Enabled (`SECURE_CONTENT_TYPE_NOSNIFF`).
- **CORS**: Same as base settings.
- **Logging**:
  - Same as development with app-specific logs and rotating file.

### Celery Configuration (`celery.py`)

- **App**: Celery instance named `config`.
- **Settings**:
  - Loads from `config.settings.development`.
  - Auto-discovers tasks from installed apps.
- **Scheduled Tasks**:
  - `delete_expired_otp`: Runs every 60 minutes on `default` queue (`core.tasks.delete_expired_otp`).
  - `backup_database`: Runs Sundays and Wednesdays at 8 PM on `high_priority` queue (`core.tasks.backup_database`).
- **Queue Configuration**:
  - Queues: `default`, `high_priority`.
  - Exchange: `tasks`.
  - Routing Key: `task.default`.
- **Debug Task**:
  - `debug_task`: Prints task request for debugging purposes.

### URL Routing (`urls.py`)

- **Admin**: `/farabin-admin/` (Django admin interface).
- **App Endpoints**:
  - `/management/`: Management module URLs.
  - `/packages/`: Packages module URLs.
  - `/finance/`: Finance module URLs.
  - `/company/`: Company module URLs.
  - `/requests/`: Request module URLs.
  - `/tickets/`: Tickets module URLs.
  - `/auth/`: Core module URLs (authentication).
- **Debug Endpoints** (available when `DEBUG=True`):
  - `/api/schema/`: API schema (OpenAPI).
  - `/swagger/`: Swagger UI for API documentation.
  - `/redoc/`: Redoc UI for API documentation.
  - Debug Toolbar: Included via `debug_toolbar_urls()`.
- **Internationalization**:
  - `/i18n/`: Language switcher URLs.
- **Static and Media Files**:
  - Serves `STATIC_URL` from `STATIC_ROOT`.
  - Serves `MEDIA_URL` from `MEDIA_ROOT`.

---

## Views

### `serve_file` (`views.py`)

- **Purpose**: Serves media files to authenticated users.
- **Method**: GET.
- **Permission**: `IsAuthenticated` (requires valid JWT token).
- **Parameters**:
  - `file_path`: Relative path to the file in `MEDIA_ROOT`.
- **Behavior**:
  - Checks if the file exists at `MEDIA_ROOT/file_path`.
  - Returns a `FileResponse` with the file content if found.
  - Raises `Http404` if the file does not exist.
- **Usage**: Access protected media files via authenticated API requests.

---

## Dependencies

- **Django**: Core framework for settings, URL routing, and views.
- **django-environ**: Environment variable management.
- **rest_framework**, **drf_spectacular**: REST API and OpenAPI documentation.
- **rest_framework_simplejwt**, **graphql_jwt**: JWT authentication for REST and GraphQL.
- **django-celery-beat**: Task scheduling.
- **django-redis**: Redis caching.
- **corsheaders**: Cross-Origin Resource Sharing.
- **whitenoise**: Static file serving.
- **debug-toolbar** (development only): Debugging tools.
- **External Services**:
  - Redis: Caching and Celery broker/result backend.
  - IPPanel SMS: OTP delivery (configured via `FARABIN_SMS_API_KEY`).
  - Google Drive: Database backups (configured via `FARABIN_DB_BACKUP_FOLDER_ID`).

---

## Usage

1. **Setup**:
   - Create a `.env` file in `BASE_DIR` with required variables (e.g., `SECRET_KEY`, `FARABIN_*`, Redis, PostgreSQL credentials).
   - Install dependencies: `pip install -r requirements.txt`.
   - Run migrations: `python manage.py migrate`.
2. **Development**:
   - Use `settings.development` for local development (`DEBUG=True`).
   - Access Swagger/Redoc at `/swagger/` or `/redoc/` for API documentation.
   - Use debug toolbar for performance insights.
3. **Production**:
   - Use `settings.production` with PostgreSQL and secure settings.
   - Configure allowed hosts and database credentials via environment variables.
4. **Celery**:
   - Start Celery worker: `celery -A config worker -l info`.
   - Start Celery Beat: `celery -A config beat -l info`.
   - Ensure Redis is running for broker and result backend.
5. **URL Access**:
   - Admin: `/farabin-admin/` for management.
   - API: `/auth/`, `/company/`, etc., for respective modules.
   - Media Files: Authenticated access via `/media/<file_path>` (requires JWT).
6. **Logging**:
   - Check logs in `/tmp/saramad_logs` (e.g., `django.log`, `errors.log`, `company_logs.log`).
   - JSON logs in `log.json` for structured logging.
   - Error emails sent to admins for critical issues.

---

> [!NOTE]
>
> - **Internationalization**: Persian is the default language, with English support.
>
> - **Security**: Production settings include HSTS, secure cookies, and SSL redirect.
>
> - **Celery Tasks**: Scheduled tasks ensure OTP cleanup and database backups.
>
> - **Logging**: Comprehensive with app-specific logs and JSON format for external systems.
>
> - **CORS**: Configured for specific origins to support frontend applications.
>
> - **API Documentation**: Automatically generated with `drf_spectacular` for REST endpoints.
