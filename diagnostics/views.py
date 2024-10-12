from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound, ValidationError

from .models import User, CompanyProfile, OTP
from .serializers import (
    OTPSendSerializer,
    OTPVerifySerializer,
    UserSerializer,
    # OTPSerializer,
    CompanyProfileSerializer,
    CompanyProfileCreateSerializer
)


# Register User and OTP Handling with ModelViewSet
# class RegisterViewSet(viewsets.ViewSet):
#     """
#     A ViewSet for registering users and handling OTP operations.
#     """

#     def create(self, request):
#         phone_number = request.data.get('phone_number')

#         if not phone_number:
#             return Response({'error': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

#         user, created = User.objects.get_or_create(phone_number=phone_number)

#         if created:
#             user.set_unusable_password()
#             user.save()
#             return Response({'message': 'User created successfully. Proceed to OTP verification.'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'message': 'User already exists.'}, status=status.HTTP_200_OK)


# class OTPViewSet(viewsets.ViewSet):
#     """
#     A ViewSet for sending and verifying OTP.
#     """

#     def send_otp(self, request):
#         phone_number = request.data.get('phone_number')

#         try:
#             user = User.objects.get(phone_number=phone_number)
#         except User.DoesNotExist:
#             return Response({'error': 'User with this phone number does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         # Generate OTP and save it
#         otp = OTP(user=user)
#         otp_code = otp.generate_otp()
#         otp.otp_code = otp_code
#         otp.save()

#         print(f"sending {otp_code} to {phone_number}")

#         return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)

#     def verify_otp(self, request):
#         phone_number = request.data.get('phone_number')
#         otp_code = request.data.get('otp_code')

#         try:
#             user = User.objects.get(phone_number=phone_number)
#             otp = OTP.objects.filter(user=user).last()

#             if otp and otp.is_valid() and otp.otp_code == otp_code:
#                 refresh = RefreshToken.for_user(user)
#                 access_token = str(refresh.access_token)

#                 return Response({
#                     'message': 'OTP verified successfully.',
#                     'refresh': str(refresh),
#                     'access': access_token
#                 }, status=status.HTTP_200_OK)
#             else:
#                 return Response({'error': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

#         except User.DoesNotExist:
#             return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)


class RegisterViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for registering users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'message': 'User created successfully. Proceed to OTP verification.'}, status=status.HTTP_201_CREATED)


class OTPViewSet(viewsets.ViewSet):
    """
    A ViewSet for sending and verifying OTP.
    """
    @action(detail=False, methods=['post', 'get'])
    def send_otp(self, request):
        serializer = OTPSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'error': 'User with this phone number does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP and save it
        otp = OTP(user=user)
        otp_code = otp.generate_otp()
        otp.otp_code = otp_code
        otp.save()

        print(f"sending {otp_code} to {phone_number}")

        return Response({'message': 'OTP sent successfully.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post', 'get'])
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
# Customer Profile ViewSet


class CompanyProfileViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling company profiles. Allows creating, retrieving, and updating profiles.
    """
    queryset = CompanyProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CompanyProfileCreateSerializer  # Use create serializer for POST requests
        return CompanyProfileSerializer  # Use normal serializer for retrieve/update

    def get_object(self):
        try:
            # Return the company profile for the authenticated user
            return CompanyProfile.objects.get(user=self.request.user)
        except CompanyProfile.DoesNotExist:
            raise NotFound("Customer profile not found. Please create one.")

    def perform_create(self, serializer):
        # Ensure a customer does not already exist for the user
        if CompanyProfile.objects.filter(user=self.request.user).exists():
            raise ValidationError("Customer profile already exists.")
        # Link the authenticated user to the newly created customer
        serializer.save(user=self.request.user)
