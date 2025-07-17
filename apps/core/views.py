import logging

from django.contrib.auth import get_user_model  # type: ignore

from rest_framework.viewsets import ModelViewSet, ViewSet  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type : ignore
from rest_framework.decorators import action  # type: ignore

from constants.responses import APIResponse

from apps.core.permissions import Unautherized
from apps.core.services import (
    AuthService as _auth_service,
    UserService as _user_service,
)
from apps.core.repositories import UserRepository as _user_repo
from apps.core.tasks import send_otp_task
from apps.core.serializers import (
    LoginSerializer,
    OTPSendSerializer,
    OTPVerifySerializer,
    PasswordResetSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)


User = get_user_model()

logger = logging.getLogger("core")


class AuthViewSet(ViewSet):
    """
    A ViewSet for sending and verifying OTP.
    """

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

    permission_classes = [Unautherized]

    @action(detail=False, methods=["get", "post"], url_path="send", url_name="otp-send")
    def request_otp(self, request):
        logger.info("Received OTP send request.", extra={"request_data": request.data})

        serializer = OTPSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        social_code = serializer.validated_data["social_code"]

        user = _user_service.create_user_with_phone_number(phone_number, social_code)
        _auth_service.otp_expiry_check(user)
        send_otp_task.delay(user.id, phone_number)
        logger.info(
            f"OTP for user {user.id} sent successfully.", extra={"user_id": user.id}
        )

        _user_service.create_company_user()

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

        user = _auth_service.otp_validation_returns_user(phone_number, otp_code)
        access_token, refresh_token = _auth_service.generate_tokens_for_user(user)

        logger.info(
            f"OTP for user {user.id} verified successfully.", extra={"user_id": user.id}
        )

        return APIResponse.success(
            message="OTP verified successfully.",
            data={
                "access": access_token,
                "refresh": refresh_token,
            },
        )

    # TODO: After the user verified its otp, it most be redirected to the company profile page to create a new profile

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]

        user = _user_service.check_user_password_returns_user(phone_number, password)
        access_token, refresh_token = _auth_service.generate_tokens_for_user(user)

        return APIResponse.success(
            message="Login successful.",
            data={
                "access": access_token,
                "refresh": refresh_token,
                "completed_profile": user.is_profile_complete,
            },
        )

    @action(detail=False, methods=["post"], url_path="reset-password")
    def reset_password(self, request):
        self.permission_classes = [IsAuthenticated]
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cpwd = serializer.validated_data["current_password"]
        npwd = serializer.validated_data["new_password"]
        npwd1 = serializer.validated_data["new_password2"]

        phone_number = self.request.user.phone_number

        _user_service.reset_user_password(phone_number, cpwd, npwd, npwd1)

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
