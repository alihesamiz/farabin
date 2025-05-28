# Django App Documentation: Company Module

## Overview

The **Company Module** is a Django application designed to manage company profiles, services, licenses, and lifecycles. It provides a robust backend for handling company-related data, including admin interfaces, REST API endpoints, caching mechanisms, and testing utilities. The module integrates with Django's authentication system, supports internationalization, and includes validation and caching for performance optimization.

---

## Module Structure

The module consists of the following key files:

- **`admin.py`**: Defines Django admin interfaces for managing `CompanyProfile`, `CompanyService`, `License`, and `LifeCycle` models.
- **`models.py`**: Contains the database models for `CompanyProfile`, `CompanyService`, `License`, `LifeCycle`, `TechField`, and `SpecialTech`.
- **`serializers.py`**: Implements REST framework serializers for `CompanyProfile` and `CompanyService` to handle data serialization and validation.
- **`signals.py`**: Defines signal handlers to clear cache on updates to related models (`Ticket`, `TaxDeclarationFile`, `BalanceReportFile`).
- **`views.py`**: Implements REST API views for company profiles and dashboard data, with caching and authentication.
- **`test_profiles.py`**: Contains pytest-based tests for profile retrieval and authentication endpoints.

---

## Models

The module defines several models to represent company-related data.

### `LifeCycle`

Represents the capital-providing lifecycle of a company.

- **Fields**:
  - `capital_providing`: Choice field with options (`operational`, `finance`, `invest`).
- **Meta**:
  - Verbose name: "Life Cycle" / "Life Cycles".
- **String Representation**: Displays the human-readable `capital_providing` value.

### `SpecialTech`

Represents a specialized technology field.

- **Fields**:
  - `name`: Char field (max 255 characters).
- **Meta**:
  - Verbose name: "Special Tech" / "Special Techs".
- **String Representation**: Returns the `name`.

### `TechField`

Represents a technical field.

- **Fields**:
  - `name`: Char field (max 255 characters).
- **Meta**:
  - Verbose name: "Tech Field" / "Tech Fields".
- **String Representation**: Returns the `name`.

### `CompanyProfile`

The core model for storing company information, integrated with Django's lifecycle hooks.

- **Fields**:
  - `id`: UUID primary key.
  - `user`: One-to-one relation with the `User` model.
  - `company_title`: Char field for the company name.
  - `email`: Unique email field (nullable).
  - `manager_social_code`: Unique social code (nullable).
  - `manager_name`: Char field for the manager's full name.
  - `manager_phone_number`: Unique phone number with custom validator (nullable).
  - `office_phone_number`: Unique landline number with custom validator (nullable).
  - `license`: Many-to-many relation with `License`.
  - `tech_field`: Foreign key to `TechField`.
  - `special_field`: Foreign key to `SpecialTech`.
  - `insurance_list`: Positive small integer for insurance count.
  - `capital_providing_method`: Many-to-many relation with `LifeCycle`.
  - `province`: Foreign key to `core.Province`.
  - `city`: Foreign key to `core.City`.
  - `address`: Char field for the company address.
  - `is_active`: Boolean indicating active status.
- **Meta**:
  - Verbose name: "Company Profile" / "Company Profiles".
- **String Representation**: Combines `company_title` and user's `national_code`.
- **Lifecycle Hook**:
  - Clears cache after creation using `django_lifecycle`.

### `License`

Represents a company license type.

- **Fields**:
  - `code`: Unique choice field (`itl`, `tl`, `kbl`, `ol`).
  - `name`: Char field for the license name.
- **Meta**:
  - Verbose name: "License" / "Licenses".
- **String Representation**: Returns the `name`.

### `CompanyService`

Links a company to a service, tracking activation and purchase details.

- **Fields**:
  - `company`: Foreign key to `CompanyProfile`.
  - `service`: Foreign key to `core.Service`.
  - `is_active`: Boolean for service activation.
  - `purchased_date`: Auto-set date field for purchase date.
- **Meta**:
  - Unique together: (`company`, `service`).
  - Verbose name: "Company Service" / "Company Services".
- **String Representation**: Combines `company_title`, `service.name`, and active status.

---

## Admin Configuration

The `admin.py` file provides customized admin interfaces for managing the models.

### `LifeCycleAdmin`

- **Model**: `LifeCycle`.
- **List Display**: Shows `capital_providing`.
- **Inline**: Used in `CompanyProfile` via `LifeCycleInline` (stacked, min/max 1 instance).

### `LicenseAdmin`

- **Model**: `License`.
- **List Display**: Shows `name` and `code`.

### `CompanyAdmin`

- **Model**: `CompanyProfile`.
- **Features**:
  - **Autocomplete Fields**: `user`.
  - **Search Fields**: `company_title`, `manager_name`.
  - **List Display**: Includes `company_title`, `national_code`, `manager_name`, `tech_field`, `special_field_display`, `insurance_list`, `capital_providing_method_display`.
  - **Readonly Fields**: `id`.
  - **Filter Horizontal**: `capital_providing_method`, `license`.
  - **Custom Methods**:
    - `national_code`: Displays user's `national_code`.
    - `special_field_display`: Displays `special_field`.
    - `capital_providing_method_display`: Joins human-readable `capital_providing_method` values.

### `CompanyServiceAdmin`

- **Model**: `CompanyService`.
- **Features**:
  - **Autocomplete Fields**: `company`.
  - **List Display**: Shows `company`, `service`, `is_active`, `purchased_date`.
  - **Search Fields**: `company__company_title`, `service__description`, `purchased_date`.
  - **Actions**:
    - `activate_services`: Marks selected services as active.
    - `deactivate_services`: Marks selected services as inactive.

---

## Serializers

The `serializers.py` file defines REST framework serializers for API data handling.

### `CompanyServiceSerializer`

- **Purpose**: Serializes `CompanyService` data for API responses.
- **Fields**:
  - `service_name`: Char field.
  - `description`: Char field.
  - `price`: Decimal field (20 digits, 0 decimal places).
  - `is_active`: Boolean field.
  - `purchased_date`: Date field (nullable).

### `CompanyProfileSerializer`

- **Purpose**: Serializes `CompanyProfile` data, including related services.
- **Fields**:
  - `user_national_code`: Read-only from `user.national_code`.
  - `services`: Computed via `get_services` method.
  - `license`: Many-to-many relation with `License`.
  - Other model fields (e.g., `company_title`, `email`, etc.).
- **Method**:
  - `get_services`: Returns a list of all active services with details (ID, name, description, active status, purchase/expiration dates).

### `CompanyProfileCreateSerializer`

- **Purpose**: Handles creation and updating of `CompanyProfile` instances.
- **Fields**: Similar to `CompanyProfileSerializer`, excluding `services` and `user_national_code`.
- **Validation**:
  - `validate_email`: Ensures email uniqueness.
  - `validate_social_code`: Ensures social code uniqueness.
- **Methods**:
  - `create`: Creates or updates a `CompanyProfile`, handling `capital_providing_method` and `license` relations.
  - `update`: Updates an existing `CompanyProfile`, validating email and handling relations.

---

## Views

The `views.py` file defines REST API endpoints for company profiles and dashboard data.

### `CompanyProfileViewSet`

- **Purpose**: Manages CRUD operations for `CompanyProfile`.
- **Permission**: Requires `IsAuthenticated`.
- **Queryset**: Filters profiles by the authenticated user, with `select_related` for `user`.
- **Serializer**:
  - `CompanyProfileCreateSerializer` for create/update actions.
  - `CompanyProfileSerializer` for retrieve/list actions.
- **Features**:
  - Logs successful fetches and errors.
  - Raises `NotFound` if no profile exists.

### `DashboardViewSet`

- **Purpose**: Provides aggregated dashboard data (file counts, tickets, requests).
- **Permission**: Requires `IsAuthenticated`.
- **Features**:
  - Uses caching (`dashboard_data_{user_id}`) to reduce database queries.
  - Aggregates counts for:
    - `TaxDeclarationFile`
    - `BalanceReportFile`
    - `HumanResource`
    - `Ticket`
    - Request models (from `settings.APP_REQUEST_TYPES`).
  - Logs cache hits, successful fetches, and errors.
  - Returns a JSON response with counts or error messages.

---

## Signals

The `signals.py` file defines cache-clearing logic for related model updates.

### `clear_dashboard_cache`

- **Triggered By**: `post_save` and `post_delete` on `Ticket`, `TaxDeclarationFile`, `BalanceReportFile`.
- **Purpose**: Clears the dashboard cache (`dashboard_data_{user_id}`) when related models are updated.
- **Logging**: Logs cache clearance with user ID and model details.

---

## Tests

The `test_profiles.py` file contains pytest-based tests for profile retrieval and authentication.

### `TestRetrieveProfile`

- **Test Cases**:
  - `test_if_user_is_anonymous_returns_401`: Verifies that anonymous users receive a 401 Unauthorized response when accessing the profile endpoint.
  - `test_verify_a_user_with_an_invalid_otp_returns_400`: Ensures that an invalid OTP returns a 400 Bad Request response.
  - `test_gain_user_access_and_refresh_tokens_returns_tokens_and_200`: Tests successful OTP verification, expecting access/refresh tokens and a 200 OK response.
  - `test_authenticated_user_profile_access_returns_200`: Verifies that an authenticated user can access their profile with a 200 OK response.
- **Setup**:
  - Uses fixtures (`api_client`, `create_user`, `generate_otp`).
  - Defines constants for `phone_number`, `national_code`, `profile_url`, and `verify_url`.

---

## Dependencies

- **Django**: Core framework for models, admin, and views.
- **Django REST Framework**: For API views and serializers.
- **django-lifecycle**: For lifecycle hooks in `CompanyProfile`.
- **django-cache**: For caching profile and dashboard data.
- **pytest-django**: For testing.
- **External Models**:
  - `core.Service`
  - `core.Province`
  - `core.City`
  - `finance.TaxDeclarationFile`
  - `finance.BalanceReportFile`
  - `tickets.Ticket`
  - `management.HumanResource`
  - Dynamic request models from `settings.APP_REQUEST_TYPES`.

---

## Usage

1. **Admin Interface**:
   - Access the Django admin to manage companies, services, licenses, and lifecycles.
   - Use actions to activate/deactivate services in bulk.
2. **API**:
   - Use `/company/profile/` to manage company profiles (requires authentication).
   - Access the dashboard endpoint to retrieve aggregated data (cached for performance).
3. **Caching**:
   - Profile and dashboard data are cached to reduce database load.
   - Cache is cleared on relevant model updates (via signals or lifecycle hooks).
4. **Testing**:
   - Run `pytest` to execute the test suite, ensuring API endpoints and authentication work as expected.

---

## Notes

- The module uses internationalization (`gettext_lazy`) for translatable strings.
- Validation is enforced for unique fields (e.g., email, social code, phone numbers).
- The `CompanyProfile` model uses a UUID for the primary key.
- The dashboard aggregates data dynamically based on `settings.APP_REQUEST_TYPES`.
- TODO: Implement logic to remove expired services (noted in `serializers.py`).
