import pytest

from rest_framework import status


from tests.utils import APIClient


@pytest.mark.django_db
class TestCreateUser:
    phone_number = "09999999999"
    national_code = "11111111111"
    send_url = "http://127.0.0.1:8000/auth/send/"
    verify_url = "http://127.0.0.1:8000/auth/verify/"
    refresh_url = "http://127.0.0.1:8000/auth/refresh/"

    def test_create_a_new_user_returns_200(self, api_client: APIClient):
        response = api_client.post(
            self.send_url,
            {"phone_number": self.phone_number, "national_code": self.national_code},
        )

        assert response.status_code == status.HTTP_200_OK

    def test_verify_a_new_user_returns_200(
        self, api_client: APIClient, create_user, generate_otp
    ):
        # Arrange
        user = create_user(
            phone_number=self.phone_number, national_code=self.national_code
        )
        otp = generate_otp(user)
        # Act
        response = api_client.post(
            self.verify_url,
            {"phone_number": f"{self.phone_number}", "otp_code": f"{otp}"},
        )
        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_verify_a_user_with_an_invalid_otp_returns_400(
        self, api_client: APIClient, create_user
    ):
        # Arrange
        user = create_user(  # noqa: F841
            phone_number=self.phone_number, national_code=self.national_code
        )
        otp_code = "111111"
        # Act
        response = api_client.post(
            self.verify_url, {"phone_number": self.phone_number, "otp_code": otp_code}
        )
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_gain_user_credentials_returns_access_and_refresh_tokens_and_200(
        self, api_client: APIClient, create_user, generate_otp
    ):
        # Arrange
        user = create_user(
            phone_number=self.phone_number, national_code=self.national_code
        )
        otp_code = generate_otp(user)
        # Act
        response = api_client.post(
            self.verify_url, {"phone_number": self.phone_number, "otp_code": otp_code}
        )
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.json()
        assert "refresh" in response.json()

    def test_user_regain_access_token_with_refresh_token_returns_access_and_200(
        self, api_client: APIClient, create_user, generate_otp
    ):
        # Arrange
        user = create_user(
            phone_number=self.phone_number, national_code=self.national_code
        )
        otp_code = generate_otp(user)
        # Act
        response = api_client.post(
            self.verify_url, {"phone_number": self.phone_number, "otp_code": otp_code}
        )
        refresh_token = response.json().get("refresh")
        # Assert
        assert refresh_token
        assert response.status_code == status.HTTP_200_OK
        # Act: Use the refresh token to get a new access token
        response = api_client.post(self.refresh_url, {"refresh": refresh_token})
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.json()
