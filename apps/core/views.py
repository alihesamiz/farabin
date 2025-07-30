import logging

from django.contrib.auth import get_user_model  # type: ignore
from rest_framework import status
from rest_framework.decorators import action  # type: ignore
from rest_framework.permissions import AllowAny, IsAuthenticated  # type : ignore
from rest_framework.viewsets import ModelViewSet, ViewSet  # type: ignore

from apps.core.models import City, Province
from apps.core.permissions import Unautherized
from apps.core.repositories import UserRepository as _user_repo
from apps.core.serializers import (
    CitySerializer,
    LoginSerializer,
    OTPSendSerializer,
    OTPVerifySerializer,
    PasswordResetSerializer,
    ProvinceSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)
from apps.core.services import (
    AuthService as _auth_service,
)
from apps.core.services import (
    UserService as _user_service,
)
from apps.core.tasks import send_otp_task
from constants.errors.api_exception import (
    InvalidCredentialsError,
    OTPValidationError,
    PasswordMismatchError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from constants.responses import APIResponse

User = get_user_model()

logger = logging.getLogger("core")


logger = logging.getLogger(__name__)


class AuthViewSet(ViewSet):
    """
    A ViewSet for sending and verifying OTP.
    """

    permission_classes = [Unautherized]

    def get_serializer_class(self):
        if self.action == "request_otp":
            return OTPSendSerializer
        elif self.action == "verify_otp":
            return OTPVerifySerializer
        elif self.action == "login":
            return LoginSerializer
        elif self.action == "reset_password":
            return PasswordResetSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["get", "post"], url_path="send", url_name="otp-send")
    def request_otp(self, request):
        logger.info("Received OTP send request.", extra={"request_data": request.data})

        serializer = OTPSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        social_code = serializer.validated_data["social_code"]

        try:
            user = _user_service.create_user_with_phone_number(
                phone_number, social_code
            )
        except UserAlreadyExistsError:
            return APIResponse.error(
                "User already exists.", status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            _auth_service.otp_expiry_check(user)
            send_otp_task.delay(user.id, phone_number)
            _user_service.create_company_user(user)
        except Exception as e:
            logger.exception(f"Failed to send OTP: {e}")
            return APIResponse.internal_error("Failed to send OTP.")

        logger.info(
            f"OTP for user {user.id} sent successfully.", extra={"user_id": user.id}
        )
        return APIResponse.success(
            message="OTP sent successfully.", data={"user_id": user.id}
        )

    @action(
        detail=False, methods=["get", "post"], url_path="verify", url_name="otp-verify"
    )
    def verify_otp(self, request):
        logger.info(
            "Received OTP verification request.", extra={"request_data": request.data}
        )

        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        otp_code = serializer.validated_data["otp_code"]

        try:
            user = _auth_service.otp_validation_returns_user(phone_number, otp_code)
        except OTPValidationError:
            return APIResponse.error(
                "Invalid or expired OTP.", status_code=status.HTTP_400_BAD_REQUEST
            )
        finally:
            _ = _user_service.create_company_returns_company(user)

        access_token, refresh_token = _auth_service.generate_tokens_for_user(user)

        logger.info(
            f"OTP for user {user.id} verified successfully.", extra={"user_id": user.id}
        )

        return APIResponse.success(
            message="OTP verified successfully.",
            data={
                "access": access_token,
                "refresh": refresh_token,
                "completed_profile": user.is_profile_complete,
            },
        )

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]

        try:
            user = _user_service.check_user_password_returns_user(
                phone_number, password
            )
        except (UserNotFoundError, InvalidCredentialsError):
            return APIResponse.unauthorized("Invalid phone number or password.")

        access_token, refresh_token = _auth_service.generate_tokens_for_user(user)

        return APIResponse.success(
            message="Login successful.",
            data={
                "access": access_token,
                "refresh": refresh_token,
                "completed_profile": user.is_profile_complete,
            },
        )

    @action(
        detail=False,
        methods=["post"],
        url_path="reset-password",
        permission_classes=[IsAuthenticated],
    )
    def reset_password(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cpwd = serializer.validated_data["current_password"]
        npwd = serializer.validated_data["new_password"]
        npwd1 = serializer.validated_data["new_password2"]

        phone_number = request.user.phone_number

        try:
            _user_service.reset_user_password(phone_number, cpwd, npwd, npwd1)
        except InvalidCredentialsError:
            return APIResponse.unauthorized("Current password is incorrect.")
        except PasswordMismatchError:
            return APIResponse.error(
                "New passwords do not match.", status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.exception(f"Unexpected error during password reset: {e}")
            return APIResponse.internal_error("Unable to reset password.")

        return APIResponse.success(message="Password reset successfully.")


class UserProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UserProfileUpdateSerializer
        return UserProfileSerializer

    def get_queryset(self):
        return _user_repo.get_user_by_id(self.request.user.id)


class CityViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = CitySerializer

    queryset = City.objects.select_related("province").all()


class ProvinceViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ProvinceSerializer
    queryset = Province.objects.all()
