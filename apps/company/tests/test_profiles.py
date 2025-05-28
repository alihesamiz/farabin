import pytest

from rest_framework.test import APIClient
from rest_framework import status


from tests.utils import APIClient  # noqa: F811


@pytest.mark.django_db
class TestRetrieveProfile:
    phone_number = "09999999999"
    national_code = "11111111111"
    profile_url = "http://127.0.0.1:8000/company/profile/"
    verify_url = "http://127.0.0.1:8000/auth/verify/"

    def test_if_user_is_anonymous_returns_401(self, api_client: APIClient):
        # arrange
        # act
        response = api_client.get(self.profile_url)
        # assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_verify_a_user_with_an_invalid_otp_returns_400(
        self, create_user, api_client: APIClient
    ):
        # Arrange
        user = create_user(self.phone_number, self.national_code)  # noqa: F841
        otp_code = "111111"
        # Act
        response = api_client.post(
            self.verify_url,
            {"phone_number": f"{self.phone_number}", "otp_code": f"{otp_code}"},
        )
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_gain_user_access_and_refresh_tokens_returns_tokens_and_200(
        self, create_user, generate_otp, api_client: APIClient
    ):
        user = create_user(
            phone_number=self.phone_number, national_code=self.national_code
        )
        otp = generate_otp(user)
        # Act
        response = api_client.post(
            self.verify_url,
            {"phone_number": f"{self.phone_number}", "otp_code": f"{otp}"},
        )
        access_token = response.json()["access"]
        refresh_token = response.json()["refresh"]

        assert access_token
        assert refresh_token
        assert response.status_code == status.HTTP_200_OK

        self.access = access_token
        self.refresh = refresh_token

    def test_authenticated_user_profile_access_returns_200(
        self, create_user, generate_otp, api_client: APIClient
    ):
        # Arrenge
        user = create_user(
            phone_number=self.phone_number, national_code=self.national_code
        )
        otp = generate_otp(user)
        # Act
        response = api_client.post(
            self.verify_url,
            {"phone_number": f"{self.phone_number}", "otp_code": f"{otp}"},
        )
        access_token = response.json()["access"]
        refresh_token = response.json()["refresh"]
        # Assert
        assert access_token
        assert refresh_token
        assert response.status_code == status.HTTP_200_OK
        # Arrange
        access = access_token
        refresh = refresh_token  # noqa: F841
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        # Act
        response = api_client.get(self.profile_url)
        # Assert
        assert response.status_code == status.HTTP_200_OK
