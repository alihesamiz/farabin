from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore


class APIResponse:
    @staticmethod
    def success(
        data=None,
        message: str = "Success",
        status_code: int = status.HTTP_200_OK,
    ) -> Response:
        return Response(
            {"success": True, "message": message, "data": data},
            status=status_code,
        )

    @staticmethod
    def created(
        data=None,
        message: str = "Object created",
        status_code: int = status.HTTP_201_CREATED,
    ) -> Response:
        return Response(
            {"status": True, "message": message, "data": data},
            status=status_code,
        )

    @staticmethod
    def not_created(
        data=None,
        message: str = "Object did not created",
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        return Response(
            {"success": False, "message": message, "data": data},
            status=status_code,
        )

    @staticmethod
    def internal_error(
        data=None,
        message: str = "An internal error occured",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ) -> Response:
        return Response(
            {"success": False, "message": message, "data": data},
            status=status_code,
        )

    @staticmethod
    def not_found(
        data=None,
        message: str = "Object/objects did not found",
        status_code: int = status.HTTP_404_NOT_FOUND,
    ) -> Response:
        return Response(
            {"success": False, "message": message, "data": data},
            status=status_code,
        )
