from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
#
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
#
from company.models import CompanyProfile
from .utils import GeneralUtils
from .models import OTP
from .serializers import (
    OTPVerifySerializer,
    OTPSendSerializer,
)

User = get_user_model()


class OTPViewSet(viewsets.ViewSet):
    """
    A ViewSet for sending and verifying OTP.
    """
    COOLDOWN_PERIOD = timedelta(minutes=3)

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
        util = GeneralUtils()

        serializer = OTPSendSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        national_code = serializer.validated_data['national_code']

        try:
            user = User.objects.get(phone_number=phone_number)

            if user.national_code != national_code:
                return Response({'error': 'The national code does not match the phone number.'}, status=status.HTTP_400_BAD_REQUEST)

            last_otp = OTP.objects.filter(user=user).last()

            if last_otp and timezone.now() < last_otp.created_at + self.COOLDOWN_PERIOD:
                time_remaining = (last_otp.created_at +
                                  self.COOLDOWN_PERIOD - timezone.now()).seconds

                return Response({
                    'error': f'You can`t request a new OTP.'
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        except User.DoesNotExist:
            user = User.objects.create(
                phone_number=phone_number, national_code=national_code)

        otp = OTP(user=user)

        otp_code = otp.generate_otp()

        otp.otp_code = otp_code

        otp.save()

        util.send_otp(phone_number, otp_code)

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
        serializer = OTPVerifySerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        otp_code = serializer.validated_data['otp_code']

        try:
            user = User.objects.get(phone_number=phone_number)

            otp = OTP.objects.filter(user=user).last()

            if otp and otp.is_valid() and otp.otp_code == otp_code:
                company, created = CompanyProfile.objects.get_or_create(
                    user=user)

                refresh = RefreshToken.for_user(user)

                access_token = str(refresh.access_token)

                otp.delete()

                return Response({
                    'message': 'OTP verified successfully.',
                    'refresh': str(refresh),
                    'access': access_token
                }, status=status.HTTP_200_OK)

            else:
                otp.delete()
                return Response({'error': 'Invalid or expired OTP.Try again after 3 Minutes'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
