from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import NotFound, ValidationError

from .models import Dashboard, FinancialAsset, User, CompanyProfile, OTP
from .serializers import (
    DashboardSerializer,
    OTPSendSerializer,
    OTPVerifySerializer,
    UserSerializer,
    CompanyProfileSerializer,
    CompanyProfileCreateSerializer
)


class RegisterViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet for registering users. Allows only registration (create) 
    for unauthenticated users, but restricts listing/retrieving users to 
    authenticated users only.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Define permissions based on the action
    def get_permissions(self):
        if self.action == 'create':
            # Allow anyone to register (create)
            return [AllowAny()]
        else:
            # Require authentication for list and other actions
            return [IsAdminUser()]

    # Override the create method to handle registration
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {'message': 'User created successfully. Proceed to OTP verification.'},
            status=status.HTTP_201_CREATED
        )


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
# "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyOTQwNzg3MSwiaWF0IjoxNzI4ODAzMDcxLCJqdGkiOiI4ODY2ZDdmOGI3Yjk0ZGIwYTNkMThiYTljOTQxYjAxMiIsInVzZXJfaWQiOjJ9.Em6acSbVWrwYRKVrsH598-wybgLVLsLLfsfZ0y2L4oc"


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(methods=['post'], detail=False)
    def logout(self, request):
        # Step 1: Check if refresh_token is in the request data
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Step 2: Attempt to blacklist the token
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'detail': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError as e:
            # Handle case when the token is invalid or already blacklisted
            return Response({'detail': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # General exception handling for other errors
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


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


# class DashboardViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=['get'])
#     def dashboard(self, request):
#         # Get the user's financial assets and count them
#         try:
#             company_profile = CompanyProfile.objects.get(user=request.user)
#         except CompanyProfile.DoesNotExist:
#             return Response({'error': 'No company profile found for this user.'}, status=400)

#         # Get the user's financial assets and count them
#         financial_assets_count = FinancialAsset.objects.filter(
#             company=company_profile).aggregate(total_declarations=Count('id'))

#         # Return the count in the response
#         return Response({
#             'total_tax_declarations': financial_assets_count['total_declarations']
#         })


class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer

    def list(self, request, *args, **kwargs):
        # Example of adding aggregated data
        queryset = self.get_queryset().annotate(total_services=Count('company_service'))
        serializer = self.get_serializer(queryset, many=True)

        # Prepare response data
        response_data = serializer.data

        # Add custom aggregated field by looping over response data
        for data in response_data:
            # Access `company_service` field by using nested structure.
            company_id = Dashboard.objects.filter(id=data['id']).values_list(
                'company_service__company_id', flat=True).first()

            # Now, calculate total services for this company
            total_services = Dashboard.objects.filter(
                company_service__company_id=company_id).count()

            # Add `total_services` to the response data
            data['total_services'] = total_services

            declaration_files_count = FinancialAsset.objects.filter(
                company_id=company_id).count()
            data['declaration_files_count'] = declaration_files_count

        return Response(response_data, status=status.HTTP_200_OK)
