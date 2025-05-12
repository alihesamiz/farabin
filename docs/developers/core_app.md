# Django App Documentation: Core Module

## Overview

The **Core Modules** form a Django application designed to manage user authentication, services, permissions, and geographical data (provinces and cities). The system supports OTP-based authentication, database backups, file validation, and dynamic file storage. It integrates with external services (e.g., SMS for OTP, Google Drive for backups) and includes robust admin interfaces, REST API endpoints, caching, and testing utilities. The application supports internationalization and enforces strict validation for data integrity.

---

## Module Structure

The application is organized into the following key files and directories:

### Core Module

- **`admin.py`**: Defines admin interfaces for `User`, `OTP`, `Service`, `PackagePermission`, and `UserPermission`.
- **`managers.py`**: Implements a custom `UserManager` for user creation and superuser management.
- **`models.py`**: Defines models for `User`, `OTP`, `City`, `Province`, `Service`, `PackagePermission`, and `UserPermission`.
- **`serializers.py`**: Provides serializers for OTP sending (`OTPSendSerializer`) and verification (`OTPVerifySerializer`).
- **`tasks.py`**: Contains Celery tasks for sending OTPs, deleting expired OTPs, and backing up the database.
- **`utils.py`**: Implements `GeneralUtils` for OTP generation, SMS sending, Persian slugification, and dynamic file renaming.
- **`validators.py`**: Defines validators for phone numbers, landline numbers, and file types (PDF, image, Excel, ticket files).
- **`views.py`**: Implements an `OTPViewSet` for sending and verifying OTPs.
- **Management commands**
  - **`createstaffuser.py`**: Creates staff users with group permissions.
  - **`database.py`**: Handles database backup and restore operations with Google Drive integration.
  - **`load_cities.py`**: Populates `Province` and `City` models from a JSON file.
  - **`load_services.py`**: Loads `Service` data from a JSON file.

---

## Models

### `User`

Custom user model extending `BaseUser` and `PermissionsMixin`.

- **Fields**:
  - `phone_number`: Unique 11-digit phone number with validator.
  - `national_code`: Unique 11-digit national code.
  - `is_active`, `is_staff`, `is_superuser`: Boolean flags for user status.
  - `groups`: Many-to-many relation with `Group`.
  - `user_permissions`: Many-to-many relation with `auth.Permission`.
- **Meta**:
  - Verbose name: "User" / "Users".
- **String Representation**: Returns `phone_number`.
- **Custom Methods**:
  - `has_perm`: Checks permissions, prioritizing superuser status.
  - `has_module_perms`: Checks module-level permissions.
  - `is_admin`: Property for superuser status.
- **Manager**: `UserManager` for user creation.
- **Authentication**:
  - `USERNAME_FIELD`: `national_code`.
  - `REQUIRED_FIELDS`: `phone_number`.

### `OTP`

Stores one-time passwords for user authentication.

- **Fields**:
  - `user`: Foreign key to `User`.
  - `otp_code`: 6-digit OTP code.
  - `created_at`: Auto-set creation timestamp.
- **Meta**:
  - Verbose name: "OTP" / "OTPs".
- **Methods**:
  - `is_valid`: Checks if OTP is valid (within 3 minutes).
  - `generate_otp`: Generates a random 6-digit OTP.
- **String Representation**: Combines user phone number and OTP code.

### `Province`

Represents a geographical province.

- **Fields**:
  - `name`: Unique char field (max 200 characters).
- **Meta**:
  - Verbose name: "Province" / "Provinces".
- **String Representation**: Returns `name`.

### `City`

Represents a city within a province.

- **Fields**:
  - `name`: Char field (max 200 characters).
  - `province`: Foreign key to `Province`.
- **Meta**:
  - Unique together: (`name`, `province`).
  - Verbose name: "City" / "Cities".
- **String Representation**: Returns `name`.

### `Service`

Represents a service offered to companies.

- **Fields**:
  - `name`: Char field (max 255 characters).
  - `description`: Text field.
  - `price`: Decimal field (20 digits, 2 decimal places).
  - `service_active`: Boolean for activation status.
- **Meta**:
  - Verbose name: "Service" / "Services".
- **String Representation**: Combines `name` and truncated `description`.

### `PackagePermission`

Defines permissions for packages or services.

- **Fields**:
  - `name`: Unique char field (max 255 characters).
  - `codename`: Unique char field (max 100 characters).
  - `description`: Text field (optional).
  - `service`: Many-to-many relation with `packages.Service`.
  - `package`: Foreign key to `packages.Package` (nullable).
- **String Representation**: Returns `name`.

### `UserPermission`

Links users to specific permissions.

- **Fields**:
  - `user`: Foreign key to `User`.
  - `permission`: Foreign key to `PackagePermission`.
- **Meta**:
  - Unique together: (`user`, `permission`).

---

## Admin Configuration

### `OtpAdmin`

- **Model**: `OTP`.
- **List Display**: `user`, `otp_code`, `created_at`.

### `UserAdmin`

- **Model**: `User`.
- **Features**:
  - **List Display**: `phone_number`, `national_code`, `is_active`, `is_staff`, `is_superuser`.
  - **Search Fields**: `phone_number`, `national_code`.
  - **Ordering**: By `phone_number`.
  - **Fieldsets**: Organized into personal info, permissions, and dates.
  - **Add Fieldsets**: For user creation with password fields.
  - **Readonly Fields**: `last_login`, `password`.
  - **Filter Horizontal**: `groups`, `user_permissions`.
  - **List Filter**: `is_active`, `is_staff`, `is_superuser`.

### `ServiceAdmin`

- **Model**: `Service`.
- **List Display**: `name`, `description`, `get_price`, `service_active`.
- **Custom Method**:
  - `get_price`: Formats `price` with 2 decimal places.

### `PackagePermissionAdmin`

- **Model**: `PackagePermission`.
- **List Display**: `name`, `codename`, `description`.
- **Search Fields**: `name`, `codename`.

### `UserPermissionAdmin`

- **Model**: `UserPermission`.
- **List Display**: `user`, `permission`.
- **List Filter**: `permission`.
- **Search Fields**: `user__username`, `permission__name`.

---

## Serializers

### `OTPSendSerializer`

- **Purpose**: Validates data for sending OTPs.
- **Fields**:
  - `phone_number`: 11-digit char field.
  - `national_code`: 11-digit char field.
- **Validation**:
  - Ensures `phone_number` and `national_code` are digits and 11 characters long.

### `OTPVerifySerializer`

- **Purpose**: Validates data for OTP verification.
- **Fields**:
  - `phone_number`: 11-digit char field.
  - `otp_code`: 6-digit char field.
- **Validation**:
  - Ensures `phone_number` is 11 digits and `otp_code` is 6 digits.

---

## Views

### `OTPViewSet`

- **Purpose**: Handles OTP sending and verification.
- **Actions**:
  - `send_otp`:
    - Validates input with `OTPSendSerializer`.
    - Creates/gets `User` and enforces a 3-minute cooldown.
    - Triggers `send_otp_task` Celery task.
    - Returns success or error responses.
  - `verify_otp`:
    - Validates input with `OTPVerifySerializer`.
    - Checks OTP validity and user status.
    - Issues JWT tokens (`refresh`, `access`) on success.
    - Creates `CompanyProfile` for non-superusers.
- **Features**:
  - Logs requests and errors.
  - Handles cooldowns and inactive users.

---

## Tasks

Celery tasks for asynchronous operations.

### `send_otp_task`

- **Purpose**: Sends OTP via SMS.
- **Arguments**: `user_id`, `phone_number`.
- **Features**:
  - Generates and saves OTP.
  - Uses `GeneralUtils.send_otp` for SMS.
  - Logs success or errors.

### `delete_expired_otp`

- **Purpose**: Deletes OTPs older than 30 minutes.
- **Features**:
  - Retries on failure (max 3 attempts).
  - Logs deleted count.

### `backup_database`

- **Purpose**: Backs up database and uploads to Google Drive.
- **Arguments**: `action` (`backup` or `restore`).
- **Features**:
  - Calls `database.py` command.
  - Retries on failure.

---

## Utilities

### `GeneralUtils`

- **Methods**:
  - `generate_otp`: Creates a 6-digit OTP.
  - `send_otp`: Sends OTP via SMS (uses IPPanel API).
  - `persian_slugify`: Slugifies strings, preserving Persian characters.
  - `rename_folder`: Dynamically renames file paths based on company, year, and field.
  - `send_sms`: Sends SMS to editors.
- **Configuration**:
  - Uses environment variables for SMS API keys and patterns.
  - Supports Google Drive integration for backups.

---

## Validators

- **`phone_number_validator`**: Ensures 11-digit mobile numbers (`09XXXXXXXXX`).
- **landline_number_validator**: Ensures 11-digit landline numbers (`0XXXXXXXXXX`).
- **`pdf_file_validator`**: Validates PDF files (max 2MB).
- **`image_file_validator`**: Validates JPG/PNG/JPEG files (max 2MB).
- **`ticket_file_validator`**: Validates PDF/JPG/PNG/JPEG files (max 2MB).
- **`excel_file_validator`**: Validates XLSX/XLS/CSV files (max 20MB).

---

## Management Commands

### `createstaffuser.py`

- **Purpose**: Creates a staff user with group permissions.
- **Features**:
  - Prompts for `phone_number`, `national_code`, and password.
  - Assigns user to a group (default: "Editor").
  - Loads permissions from `staff_permissions.txt`.
- **Output**: Success/error messages for user and group creation.

### `database.py`

- **Purpose**: Backs up or restores the PostgreSQL database with Google Drive integration.
- **Arguments**: `action` (`backup` or `restore`).
- **Features**:
  - **Backup**: Uses `pg_dump` to create SQL file, uploads to Google Drive.
  - **Restore**: Downloads latest backup, restores using `psql`.
  - Logs progress and errors.
  - Cleans up local files.

### `load_cities.py`

- **Purpose**: Populates `Province` and `City` models from `updated_cities.json`.
- **Features**:
  - Creates provinces and cities with unique constraints.
  - Outputs success message.

### `load_services.py`

- **Purpose**: Loads `Service` data from `services.json`.
- **Features**:
  - Validates required fields (`name`, `description`, `price`, `service_active`).
  - Creates or skips existing services.
  - Outputs success/warning messages.

---

## Signals

### `clear_dashboard_cache`

- **Triggered By**: `post_save`/`post_delete` on `Ticket`, `TaxDeclarationFile`, `BalanceReportFile`.
- **Purpose**: Clears dashboard cache for affected users.
- **Logging**: Logs cache clearance details.

---

## Tests

### `TestRetrieveProfile`

- **Test Cases**:
  - Anonymous access returns 401.
  - Invalid OTP returns 400.
  - Valid OTP returns tokens and 200.
  - Authenticated profile access returns 200.
- **Setup**: Uses `api_client`, `create_user`, `generate_otp`.

---

## Dependencies

- **Django**: Models, admin, views.
- **Django REST Framework**: API views, serializers.
- **django-lifecycle**: Lifecycle hooks.
- **Celery**: Asynchronous tasks.
- **django-cache**: Caching.
- **pytest-django**: Testing.
- **requests**: SMS and Google Drive APIs.
- **google-api-python-client**: Google Drive integration.
- **External Models**:
  - `auth.Group`, `auth.Permission`.
  - `finance.TaxDeclarationFile`, `finance.BalanceReportFile`.
  - `tickets.Ticket`.
  - `management.HumanResource`.
  - `packages.Service`, `packages.Package`.

---

## Usage

1. **Admin Interface**:
   - Manage users, OTPs, services, permissions, and company data.
   - Use actions to activate/deactivate services.
2. **API**:
   - `/auth/send/`: Send OTP (POST).
   - `/auth/verify/`: Verify OTP and get tokens (POST).
   - `/company/profile/`: Manage company profiles (authenticated).
   - Dashboard endpoint for aggregated data.
3. **Tasks**:
   - Run `send_otp_task` for OTP delivery.
   - Schedule `delete_expired_otp` and `backup_database`.
4. **Management Commands**:
   - `python manage.py createstaffuser`: Create staff users.
   - `python manage.py database backup|restore`: Manage database backups.
   - `python manage.py load_cities`: Populate provinces/cities.
   - `python manage.py load_services`: Load services.
5. **Testing**: Run `pytest` to verify functionality.

---

> [!NOTE]
> Internationalization is supported via `gettext_lazy`.
>
> OTPs expire after 3 minutes; expired OTPs are cleaned up via Celery.
>
> Database backups are stored in Google Drive with automatic cleanup.
>
> File uploads are validated for type and size.

> [!IMPORTANT]
> TODO: Implement service expiration logic in `CompanyProfileSerializer`.
