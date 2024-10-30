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
from .models import BalanceReport,  CompanyProfile, TaxDeclaration
from diagnostics.models import FinancialAsset
from .serializers import (
    BalanceReportCreateSerializer,
    BalanceReportSerializer,
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


class DashboardViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Fetch the company profile associated with the authenticated user
            company = CompanyProfile.objects.get(user=self.request.user)

            # Retrieve TaxDeclaration and BalanceReport files related to this company
            tax_files = TaxDeclaration.objects.filter(company=company)

            report_files = BalanceReport.objects.filter(
                company=company)

            tax_files_count = tax_files.count()
            report_files_count = report_files.count()
            # Serialize the data
            tax_files_data = TaxDeclarationSerializer(
                tax_files, many=True).data
            report_files_data = BalanceReportSerializer(
                report_files, many=True).data

            # Return a structured JSON response with both file types
            response_data = {
                "tax_files": {'tax_files': tax_files_data, 'tax_files_count': tax_files_count},
                "balance_reports": {'report_files': report_files_data, 'report_files_count': report_files_count}
            }

            return Response(response_data)

        except CompanyProfile.DoesNotExist:
            return Response({"error": "Company profile not found"}, status=404)


class TaxDeclarationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        return TaxDeclaration.objects.filter(company__user=self.request.user).all()

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
            return Response({"success": "file deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "Failed to delete file"}, status=status.HTTP_400_BAD_REQUEST)


class BalanceReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BalanceReport.objects.filter(company__user=self.request.user).all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BalanceReportCreateSerializer
        return BalanceReportSerializer

    def get_serializer_context(self):
        # Pass the request to the serializer context
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_destroy(self, instance):
        try:
            instance.delete()
            return Response({"success": "file deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "Failed to delete file"}, status=status.HTTP_400_BAD_REQUEST)
