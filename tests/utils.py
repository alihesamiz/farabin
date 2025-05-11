import pytest

from rest_framework.test import APIClient

from core.models import OTP, User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(phone_number, national_code):
        user = User.objects.create(
            phone_number=phone_number, national_code=national_code
        )
        return user

    return _create_user


@pytest.fixture
def generate_otp():
    def _generate_otp(user):
        otp = OTP(user=user)
        otp_code = otp.generate_otp()
        otp.otp_code = otp_code
        otp.save()
        return otp_code

    return _generate_otp
