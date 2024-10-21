from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import NotFound, ValidationError
from .models import Dashboard, CompanyProfile
from diagnostics.models import FinancialAsset
from .serializers import (
    DashboardSerializer,
    CompanyProfileSerializer,
    CompanyProfileCreateSerializer
)
# Create your views here.


# class CompanyProfileViewSet(viewsets.ModelViewSet):
#     """
#     A ViewSet for handling company profiles. Allows creating, retrieving, and updating profiles.
#     """
#     # queryset = CompanyProfile.objects.all()
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return CompanyProfile.objects.filter(user=user)

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return CompanyProfileCreateSerializer  # Use create serializer for POST requests
#         return CompanyProfileSerializer  # Use normal serializer for retrieve/update

#     def get_object(self):
#         try:
#             # Return the company profile for the authenticated user
#             return CompanyProfile.objects.get(user=self.request.user)
#         except CompanyProfile.DoesNotExist:
#             raise NotFound("Customer profile not found. Please create one.")

#     def perform_create(self, serializer):
#         # Ensure a customer does not already exist for the user
#         if CompanyProfile.objects.filter(user=self.request.user).exists():
#             raise ValidationError("Customer profile already exists.")
#         # Link the authenticated user to the newly created customer
#         serializer.save(user=self.request.user)

class CompanyProfileViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling company profiles. Allows creating, retrieving, and updating profiles.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CompanyProfile.objects.filter(user=user)

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
