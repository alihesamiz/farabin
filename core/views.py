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
from rest_framework.exceptions import AuthenticationFailed

from .tasks import send_otp_task
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
    util = GeneralUtils()
    COOLDOWN_PERIOD = timedelta(minutes=3)

    @action(detail=False, methods=['get', 'post'], url_path='send')
    def send_otp(self, request):

        serializer = OTPSendSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        national_code = serializer.validated_data['national_code']

        try:
            user, created = User.objects.get_or_create(
                phone_number=phone_number,
                defaults={'national_code': national_code}
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not user.is_active:
            raise AuthenticationFailed('User account is disabled.')
        
        
        if not created and user.national_code != national_code:
            return Response({'error': 'The national code does not match the phone number.'}, status=status.HTTP_400_BAD_REQUEST)

        last_otp = OTP.objects.filter(user=user).last()

        if last_otp and timezone.now() < last_otp.created_at + self.COOLDOWN_PERIOD:

            return Response({
                'error': f'You can`t request a new OTP.'
            }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        send_otp_task.delay(user.id, phone_number)

        # otp = OTP.objects.create(user=user, otp_code=OTP.generate_otp(self))

        # self.util.send_otp(phone_number, otp.otp_code)

        return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)

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
                
                if not user.is_active:
                    raise AuthenticationFailed('User account is disabled.')

                refresh = RefreshToken.for_user(user)

                access_token = str(refresh.access_token)

                otp.delete()

                return Response({
                    'message': 'OTP verified successfully.',
                    'refresh': str(refresh),
                    'access': access_token
                }, status=status.HTTP_200_OK)

            else:
                if otp:
                    otp.delete()
                return Response({'error': 'Invalid or expired OTP.Try again after 3 Minutes'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
