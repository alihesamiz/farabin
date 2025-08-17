from rest_framework import status  # type: ignore
from rest_framework.exceptions import APIException  # type: ignore


class OTPExistsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "An OTP already exists for this user."
    default_code = "otp_exists"


class OTPValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid or expired OTP"
    default_code = "otp_invalid"


class OTPCooldownError(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = "OTP cooldown period is still active."
    default_code = "otp_cooldown"


class UserAlreadyExistsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A user with this phone number or social code already exists."
    default_code = "user_already_exists"


class UserNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User does not exist."
    default_code = "user_not_found"


class InvalidCredentialsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid phone number or password."
    default_code = "invalid_credentials"


class PasswordMismatchError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "New passwords do not match."
    default_code = "password_mismatch"


class CustomerAlreadyExistsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A customer with this name already exists."
    default_code = "customer_already_exists"


class ProductAlreadyExistsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A Product with this name already exists."
    default_code = "product_already_exists"


class ObjectNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "No object found"
    default_code = "object_not_found"


class NoCompanyAssignedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "No Company is assigned with the user"
    default_code = "no_company_assigned"


class FinancialDataNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "No Financial Data found for this period"
    default_code = "no_financial_data"


class FinancialChartNameError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No chart configuration found for this chart name"
    default_code = "no_chart_name"


class FileYearAlreadyExists(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "A file with this year already exists"
    default_code = "file_exists_duplicate"


class DeletionPermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You do not have permission to delete this file."
    default_code = "permission_denied"


class DatabaseSaveError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Could not save the changes to the database."
    default_code = "database_error"


class NoQueryParameterError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No query parameter provided"
    default_code = "no_query_parameter"
