from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import OTP
from django.contrib.auth import get_user_model
from .serializers import (
    OTPSendSerializer,
    OTPVerifySerializer,
    # UserSerializer,
)

User = get_user_model()

# {
#     "message": "OTP verified successfully.",
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMDE4Mjc5OCwiaWF0IjoxNzI5NTc3OTk4LCJqdGkiOiI2YTU5ZDg5YTI4M2M0ZGE3OTVhMDA1YTVkMWZmOTc4ZSIsInVzZXJfaWQiOjN9.A7alNS6kIC7Fwl7EgTRZ2K7hQ47TEEk57uEBsMbW7Vc",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5NjY0Mzk4LCJpYXQiOjE3Mjk1Nzc5OTgsImp0aSI6ImUzZWM5OTRhYjc3NzQ0OGE5ZTI1NzUzNzQwNWM4YjhlIiwidXNlcl9pZCI6M30.xaYHz_g6XOpHemgY1sjQQMYn1hwZ4azG2aIr4s4aKHo"
# }

class OTPViewSet(viewsets.ViewSet):
    """
    A ViewSet for sending and verifying OTP.
    """

    @extend_schema(
        request=OTPSendSerializer,
        responses={200: OpenApiExample(
            'Success',
            value={
                'message': 'OTP sent successfully.'
            }
        ), 400: OpenApiExample(
            'Validation error',
            value={
                'error': 'The national code does not match the phone number.'
            }
        )},
        summary="Send OTP",
        description="Sends a one-time password (OTP) to the user's phone number. If the phone number exists and the national code matches, OTP is generated; otherwise, a new user is created.",
        parameters=[
            OpenApiParameter(
                name="phone_number", description="The phone number of the user", required=True, type=str),
            OpenApiParameter(
                name="national_code", description="The national code of the user", required=True, type=str)
        ],
        examples=[
            OpenApiExample(
                'Valid Request',
                description='Send OTP to phone number',
                value={
                    'phone_number': '09123456789',
                    'national_code': '12345678901'
                }
            )
        ]
    )
    @action(detail=False, methods=['get', 'post'], url_path='send')
    def send_otp(self, request):
        serializer = OTPSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        national_code = serializer.validated_data['national_code']

        # Check if a user with the given phone number already exists
        try:
            user = User.objects.get(phone_number=phone_number)

            # If the user exists but the national code doesn't match
            if user.national_code != national_code:
                return Response({'error': 'The national code does not match the phone number.'}, status=status.HTTP_400_BAD_REQUEST)

            # If the phone number and national code match, proceed to OTP generation
        except User.DoesNotExist:
            # If the phone number does not exist, create a new user
            user = User.objects.create(
                phone_number=phone_number, national_code=national_code)

        # Generate OTP and save it
        otp = OTP(user=user)
        otp_code = otp.generate_otp()
        otp.otp_code = otp_code
        otp.save()

        print(f"sending {otp_code} to {phone_number}")

        return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)

    @extend_schema(
        request=OTPVerifySerializer,
        responses={
            200: OpenApiExample(
                'Success',
                value={
                    'message': 'OTP verified successfully.',
                    'refresh': 'token_string',
                    'access': 'access_token_string'
                }
            ),
            400: OpenApiExample(
                'Invalid or expired OTP',
                value={
                    'error': 'Invalid or expired OTP.'
                }
            ),
            404: OpenApiExample(
                'User does not exist',
                value={
                    'error': 'User does not exist.'
                }
            )
        },
        summary="Verify OTP",
        description="Verifies the OTP sent to the user. If valid, returns JWT tokens.",
        parameters=[
            OpenApiParameter(
                name="phone_number", description="The phone number of the user", required=True, type=str),
            OpenApiParameter(
                name="otp_code", description="The OTP code sent to the user", required=True, type=str)
        ],
        examples=[
            OpenApiExample(
                'Valid Request',
                description='Verify OTP for login',
                value={
                    'phone_number': '09123456789',
                    'otp_code': '123456'
                }
            )
        ]
    )
    @action(detail=False, methods=['get', 'post'], url_path='verify')
    def verify_otp(self, request):
        # Ensure the phone_number is included in the request data
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Access both phone_number and otp_code from validated data
        phone_number = serializer.validated_data['phone_number']
        otp_code = serializer.validated_data['otp_code']

        try:
            user = User.objects.get(phone_number=phone_number)
            otp = OTP.objects.filter(user=user).last()

            if otp and otp.is_valid() and otp.otp_code == otp_code:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    'message': 'OTP verified successfully.',
                    'refresh': str(refresh),
                    'access': access_token
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
