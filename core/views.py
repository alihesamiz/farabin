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


# class RegisterViewSet(viewsets.ModelViewSet):
#     """
#     A ModelViewSet for registering users. Allows only registration (create)
#     for unauthenticated users, but restricts listing/retrieving users to
#     authenticated users only.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

#     # Define permissions based on the action
#     def get_permissions(self):
#         if self.action == 'create':
#             # Allow anyone to register (create)
#             return [AllowAny()]
#         else:
#             # Require authentication for list and other actions
#             return [IsAdminUser()]

#     # Override the create method to handle registration
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response(
#             {'message': 'User created successfully. Proceed to OTP verification.'},
#             status=status.HTTP_201_CREATED
#         )


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


class LogoutViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False, url_path='')
    def logout(self, request):
        """
        Handles logout by blacklisting the refresh token.
        """
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
