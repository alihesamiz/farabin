import logging
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.db.models import Count
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import NotFound, ValidationError
from .models import BalanceReport, Dashboard, CompanyProfile, TaxDeclaration
from diagnostics.models import FinancialAsset
from .serializers import (
    BalanceReportCreateSerializer,
    BalanceReportSerializer,
    DashboardSerializer,
    CompanyProfileSerializer,
    CompanyProfileCreateSerializer,
    TaxDeclarationCreateSerializer,
    TaxDeclarationSerializer
)


class CompanyProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CompanyProfile.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CompanyProfileCreateSerializer
        return CompanyProfileSerializer

    @action(detail=True, methods=['get'])
    def retrieve_profile(self, request, pk=None):
        queryset = self.get_queryset()
        company_profile = get_object_or_404(queryset, pk=pk)
        serializer = CompanyProfileSerializer(company_profile)
        return Response(serializer.data)


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


logger = logging.getLogger(__name__)

# TaxDeclaration ViewSet


# class TaxDeclarationViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = TaxDeclarationSerializer
#     queryset = TaxDeclaration.objects.all()

#     def get_serializer_context(self):
#         # Pass the request to the serializer context
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context

#     def perform_destroy(self, instance):
#         try:
#             instance.delete()
#             print(True)
#         except Exception as e:
#             print(False)
# # BalanceReport ViewSet


# class BalanceReportViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = BalanceReport.objects.all()
#     serializer_class = BalanceReportSerializer

#     def get_serializer_context(self):
#         # Pass the request to the serializer context
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context


class TaxDeclarationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TaxDeclaration.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return TaxDeclarationCreateSerializer
        return TaxDeclarationSerializer

    def get_serializer_context(self):
        # Pass the request to the serializer context
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_destroy(self, instance):
        try:
            instance.delete()
            print(True)
        except Exception as e:
            print(False)


class BalanceReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BalanceReport.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BalanceReportCreateSerializer
        return BalanceReportSerializer

    def get_serializer_context(self):
        # Pass the request to the serializer context
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
