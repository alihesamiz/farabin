from rest_framework import status
from rest_framework.response import Response


class APIResponse:
    @staticmethod
    def _build_response(
        success: bool,
        message: str,
        data=None,
        status_code=status.HTTP_200_OK,
        errors=None,
        code=None,
    ):
        response = {
            "success": success,
            "message": message,
            "data": data,
        }
        if errors is not None:
            response["errors"] = errors
        if code is not None:
            response["code"] = code
        return Response(response, status=status_code)

    @staticmethod
    def success(data=None, message="Success", status_code=status.HTTP_200_OK):
        return APIResponse._build_response(True, message, data, status_code)

    @staticmethod
    def created(
        data=None, message="Object created", status_code=status.HTTP_201_CREATED
    ):
        return APIResponse._build_response(True, message, data, status_code)

    @staticmethod
    def error(
        message="An error occurred",
        data=None,
        status_code=status.HTTP_400_BAD_REQUEST,
        errors=None,
        code=None,
    ):
        return APIResponse._build_response(
            False, message, data, status_code, errors, code
        )

    @staticmethod
    def not_created(message="Object could not be created", data=None, errors=None):
        return APIResponse.error(
            message=message,
            data=data,
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=errors,
        )

    @staticmethod
    def no_content(message="Object softly deleted", data=None, errors=None):
        return APIResponse.error(
            message=message,
            data=data,
            status_code=status.HTTP_204_NO_CONTENT,
            errors=errors,
        )

    @staticmethod
    def internal_error(message="An internal error occurred", data=None, errors=None):
        return APIResponse.error(
            message=message,
            data=data,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            errors=errors,
        )

    @staticmethod
    def not_found(message="Resource not found", data=None):
        return APIResponse.error(
            message=message, data=data, status_code=status.HTTP_404_NOT_FOUND
        )

    @staticmethod
    def unauthorized(message="Unauthorized", data=None):
        return APIResponse.error(
            message=message, data=data, status_code=status.HTTP_401_UNAUTHORIZED
        )

    @staticmethod
    def forbidden(message="Forbidden", data=None):
        return APIResponse.error(
            message=message, data=data, status_code=status.HTTP_403_FORBIDDEN
        )

    @staticmethod
    def validation_error(message="Validation failed", data=None, errors=None):
        return APIResponse.error(
            message=message,
            data=data,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            errors=errors,
        )
