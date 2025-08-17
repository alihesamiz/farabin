from typing import Tuple

from django.conf import settings  # type: ignore
from django.db.transaction import atomic  # type: ignore
from django.utils import timezone  # type: ignore
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.models import OTP
from apps.core.repositories import AuthRepository as _auth_repo
from constants.errors.api_exception import OTPCooldownError, OTPExistsError
from constants.responses.responses import APIResponse
from constants.typing import ModelType, UserType


class AuthService:
    cooldown_period = settings.COOLDOWN_PERIOD

    @staticmethod
    def generate_tokens_for_user(user: UserType) -> Tuple[str, str]:
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)  # type: ignore

        return (access_token, str(refresh_token))

    @staticmethod
    def generate_new_access_with_refresh(refresh: str) -> str:
        return str(RefreshToken(refresh).access_token)

    @staticmethod
    def otp_activation_check(otp: ModelType):
        if not otp.is_active:
            raise OTPExistsError("OTP already exists, proceed to login with password")

    @staticmethod
    def deactivate_otp(otp: OTP):
        with atomic():
            otp.is_active = False
            otp.save()

    @classmethod
    def otp_expiry_check(cls, user: UserType):
        last_otp = OTP.objects.filter(user=user).last()
        if last_otp:
            cls.otp_activation_check(last_otp)
            if last_otp and timezone.now() < last_otp.created_at + cls.cooldown_period:
                raise OTPCooldownError("OTP cooldown in effect. Try again later.")

    @classmethod
    def otp_validation_returns_user(cls, phone_number: str, otp_code: str) -> UserType:
        otp = _auth_repo.get_user_otp(phone_number, otp_code)
        if not otp or not otp.is_valid() or otp.otp_code != otp_code:
            raise ValueError("Invalid OTP")

        cls.deactivate_otp(otp)

        return otp.user

    @classmethod
    def set_http_cookie_returns_access_response(
        cls, refresh: str, access: str, user_profile_status: bool
    ) -> Response:
        response = APIResponse.success(
            message="OTP verified successfully.",
            data={
                "access": access,
                "refresh": refresh,
                "completed_profile": user_profile_status,
            },
        )
        response.set_cookie(
            key="refresh",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=7 * 24 * 3600,
        )
        response.set_cookie(
            key="access",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=1 * 3600,
        )
        return response
