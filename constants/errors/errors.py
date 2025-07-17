from rest_framework.exceptions import APIException  # type: ignore
from rest_framework import status  # type: ignore


class OTPExistsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "An OTP already exists for this user."
    default_code = "otp_exists"


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
