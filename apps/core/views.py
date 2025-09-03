import logging
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model  # type: ignore
from rest_framework import status
from rest_framework.decorators import action  # type: ignore
from rest_framework.permissions import AllowAny, IsAuthenticated  # type : ignore
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet, ViewSet  # type: ignore
from django.contrib.auth import login as auth_login
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
from constants.errors import (
    InvalidCredentialsError,
    OTPValidationError,
    PasswordMismatchError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from constants.responses import APIResponse
from drf_spectacular.utils import extend_schema

User = get_user_model()

logger = logging.getLogger("core")


logger = logging.getLogger(__name__) 



from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.conf import settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),  # Short-lived for security
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Longer for user convenience
    'ROTATE_REFRESH_TOKENS': True,                   # Issue new refresh token on refresh
    'BLACKLIST_AFTER_ROTATION': True,                # Blacklist old refresh tokens (requires db)
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',                            # Or 'RS256' for asymmetric keys
    'AUTH_HEADER_TYPES': ('Bearer',),                # For header-based auth (fallback if not using cookies)
    'AUTH_COOKIE': 'access_token',                   # Cookie name for access token
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_SECURE': True,                      # True in production (HTTPS)
    'AUTH_COOKIE_SAMESITE': "None",                   # Or 'Strict' for max security
    'REFRESH_COOKIE': 'refresh_token',               # Cookie name for refresh token
}


@extend_schema(
    summary="Login",
    description="Obtain JWT token pair"
)
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]  # Allow unauthenticated access to login

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            if access_token and refresh_token:
                # Set access token cookie
                # response.set_cookie(
                #     key=SIMPLE_JWT['AUTH_COOKIE'],
                #     value=access_token,
                #     max_age=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                #     httponly=SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                #     secure=SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                #     samesite= 'None'
                # )
                # Set refresh token cookie
                response.set_cookie(
                    key="refresh_token",
                    value=refresh_token,
                    max_age=SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                    httponly=SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    secure=SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    samesite="None"
                )
                

                response.data = {'message': 'Login successful', 'access':access_token}


 
@extend_schema(
    summary="Refresh Token",
    description="Refresh access token using refresh token"
)
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Extract refresh token from cookie (instead of body)
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({'error': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
    # Make a mutable copy of request.data
        data = request.data.copy()
        data['refresh'] = refresh_token

        data = request.data.copy()
        data['refresh'] = refresh_token
        request._full_data = data  # inject into request

        response = super().post(request, *args, **kwargs)


        if response.status_code == 200:
            access_token = response.data.get('access')
            new_refresh_token = response.data.get('refresh')  # If rotation enabled
            if access_token:
                # Update access token cookie
                response.set_cookie(
                    key=SIMPLE_JWT['AUTH_COOKIE'],
                    value=access_token,
                    max_age=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                    httponly=SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    secure=SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    samesite=SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                    
                )

                # # Update refresh token if rotated
                # if new_refresh_token:
                #     response.set_cookie(
                #         key=SIMPLE_JWT['REFRESH_COOKIE'],
                #         value=new_refresh_token,
                #         max_age=SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds(),
                #         httponly=SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                #         secure=SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                #         samesite=SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                #     )




                response.data = {'message': 'Token refreshed', 'access': access_token}
        return response

 
@extend_schema(
    summary="Logout",
    description="Logout user / revoke tokens"
)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get(SIMPLE_JWT['REFRESH_COOKIE'])
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
            response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
            # Delete cookies
            response.delete_cookie(SIMPLE_JWT['AUTH_COOKIE'])
            response.delete_cookie(SIMPLE_JWT['REFRESH_COOKIE'])
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Example protected view
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': f'Hello, {request.user.username}! This is protected.'})








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
    def request_otp(self, request: Request):
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
    def verify_otp(self, request: Request):
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

        return _auth_service.set_http_cookie_returns_access_response(
            refresh_token, access_token, user.is_profile_complete
        )




    @action(detail=False, methods=["post"], url_path="login2")
    def login(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]

        try:
            user = _user_service.check_user_password_returns_user(
                phone_number, password
            )
        except InvalidCredentialsError:
            return APIResponse.unauthorized("Invalid phone number or password.")
        except UserNotFoundError:
            return APIResponse.not_found("No User found with this credentials")
        access_token, refresh_token = _auth_service.generate_tokens_for_user(user)

        return _auth_service.set_http_cookie_returns_access_response(
            refresh_token, access_token, user.is_profile_complete
        )


    @action(
        detail=False,
        methods=["post"],
        url_path="reset-password",
        permission_classes=[IsAuthenticated],
    )
    def reset_password(self, request: Request):
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
            return APIResponse.error("New passwords do not match.")
        except Exception as e:
            logger.exception(f"Unexpected error during password reset: {e}")
            return APIResponse.internal_error("Unable to reset password.")

        return APIResponse.success(message="Password reset successfully.")




    # @action(
    #     detail=False,
    #     methods=["post"],
    #     url_path="refresh",
    #     permission_classes=[AllowAny],
    # )
    # def gain_access(self, request: Request):
    #     refresh_token = request.COOKIES.get("refresh")
    #     if refresh_token is None:
    #         return APIResponse.error(
    #             message="No refresh token provided, proceed to login"
    #         )

    #     try:
    #         access = _auth_service.generate_new_access_with_refresh(refresh_token)
    #         return APIResponse.success(
    #             message="Valid Refresh Token", data={"access": access}
    #         )
    #     except Exception:
    #         return APIResponse.unauthorized(message="Invalid token")


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
    http_method_names = ["get"]
    serializer_class = CitySerializer
    queryset = City.objects.select_related("province").all()


class ProvinceViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    http_method_names = ["get"]
    serializer_class = ProvinceSerializer
    queryset = Province.objects.all()
