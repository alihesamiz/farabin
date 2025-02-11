import os

from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.files.storage import default_storage
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from django.db.transaction import atomic
from django.http import FileResponse
from django.core.cache import cache

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.views import APIView

import logging

from company.models import BalanceReport,  CompanyProfile, DiagnosticRequest, TaxDeclaration
from company.serializers import (
    BalanceReportCreateSerializer,
    BalanceReportSerializer,
    CompanyProfileSerializer,
    CompanyProfileCreateSerializer,
    DiagnosticRequestSerializer,
    TaxDeclarationCreateSerializer,
    TaxDeclarationSerializer
)

from ticket.models import Ticket


logger = logging.getLogger("company")


class CompanyProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cache_key = f"company_profile_{self.request.user.id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info("Cache hit for company profile", extra={
                        "user_id": self.request.user.id})
            return cached_data

        try:
            profile = CompanyProfile.objects.filter(user=self.request.user)
            cache.set(cache_key, profile)
            logger.info("Profile fetched from DB and cached",
                        extra={"user_id": self.request.user.id})
            return profile

        except Exception as e:
            logger.error("Failed to fetch profile", extra={
                         "user_id": self.request.user.id, "error": str(e)}, exc_info=True)
            raise NotFound(detail="Company profile not found.")

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CompanyProfileCreateSerializer
        return CompanyProfileSerializer

    @action(detail=True, methods=['get'])
    def retrieve_profile(self, request, pk=None):

        try:
            queryset = self.get_queryset()
            company_profile = get_object_or_404(queryset, pk=pk)
            serializer = CompanyProfileSerializer(company_profile)
            logger.info(
                "Company profile retrieved successfully",
                extra={"user_id": request.user.id, "profile_id": pk}
            )
            return Response(serializer.data)

        except Exception as e:
            logger.error(
                "Failed to retrieve company profile",
                extra={"user_id": request.user.id,
                       "profile_id": pk, "error": str(e)},
                exc_info=True
            )
            raise NotFound(detail=f"Company profile not found.{
                           e}", code=status.HTTP_404_NOT_FOUND)


class DashboardViewSet(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        cache_key = f"dashboard_data_{user_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info("Dashboard data retrieved from cache",
                        extra={"user_id": user_id})
            return Response(cached_data)

        try:
            company = CompanyProfile.objects.filter(
                user=self.request.user).first()

            if not company:
                logger.warning("Company profile not found",
                               extra={"user_id": user_id})
                return Response({"error": "Company profile not found"}, status=404)

            tax_files = TaxDeclaration.objects.filter(company=company)
            report_files = BalanceReport.objects.filter(
                company=company)
            tickets = Ticket.objects.filter(issuer=company).count()
            tax_files_count = tax_files.count()
            report_files_count = report_files.count()
            diagnostic_requests_count = DiagnosticRequest.objects.filter(
                company=company).count()
            total_uploaded_files = tax_files_count + report_files_count
            tickets = Ticket.objects.filter(
                issuer__user=self.request.user).count()
            response_data = {
                'tax_files_count': tax_files_count,
                'report_files_count': report_files_count,
                'all_uploaded_files': total_uploaded_files,
                "tickets": tickets,
                "diagnostic_requests": diagnostic_requests_count,
                "management_requests": 0,
                "marketing_requests": 0,
                "mis_requests": 0,
                "rad_requests": 0,
                "production_requests": 0,
            }

            cache.set(cache_key, response_data)
            logger.info("Dashboard data fetched from DB and cached",
                        extra={"user_id": user_id})
            return Response(response_data)

        except Exception as e:
            logger.error("Failed to fetch dashboard data", extra={
                         "user_id": user_id, "error": str(e)}, exc_info=True)
            return Response({"error": "An error occurred while fetching dashboard data"}, status=500)


class TaxDeclarationViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = TaxDeclaration.objects.filter(
            company__user=self.request.user).order_by('-year')
        logger.info("Fetched tax declarations", extra={
                    "user_id": user_id, "count": queryset.count()})
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return TaxDeclarationCreateSerializer
        return TaxDeclarationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def destroy(self, request, *args, **kwargs):
        user_id = request.user.id
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            logger.info("File deleted successfully", extra={
                        "user_id": user_id, "file_id": instance.id})
            return Response({"success": "file deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error("Failed to delete file", extra={
                         "user_id": user_id, "error": str(e)}, exc_info=True)
            return Response({"error": "Failed to delete file"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):

        try:
            file_path = instance.tax_file.path
            folder_path = os.path.dirname(file_path)
            if file_path and default_storage.exists(file_path):
                default_storage.delete(file_path)
            if folder_path and not os.listdir(folder_path):
                os.rmdir(folder_path)
            instance.delete()
            logger.info("File and file path deleted successfully",
                        extra={"file_id": instance.id})

        except Exception as e:
            logger.error("Failed to delete file or file path", extra={
                         "file_id": instance.id, "error": str(e)}, exc_info=True)

    @xframe_options_exempt
    @action(detail=True, methods=['get'], url_path='pdf')
    def pdf(self, request, pk=None,):
        tax_declaration = self.get_object()
        pdf_path = tax_declaration.tax_file.path

        if not os.path.exists(pdf_path):
            logger.warning("Requested PDF file not found", extra={
                           "user_id": request.user.id, "file_id": pk})
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        logger.info("Serving PDF file", extra={
                    "user_id": request.user.id, "file_id": pk})
        response = FileResponse(open(pdf_path, 'rb'),

                                content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{tax_declaration.tax_file.name}"'
        response['X-Frame-Options'] = 'ALLOWALL'
        return response

    @action(detail=False, methods=['get'])
    def year(self, request):

        tax_declarations = self.get_queryset()
        years = tax_declarations.values('year').distinct()
        logger.info("Fetched unique tax declaration years", extra={
                    "user_id": request.user.id, "years_count": len(years)})

        return Response(years, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put', 'patch'], url_path='send-experts')
    def send(self, request):
        """
        Update the 'is_sent' field to True for multiple TaxDeclaration instances.
        Expects a list of IDs in the request body.
        """
        user_id = request.user.id
        ids = request.data.get('ids', [])
        queryset = TaxDeclaration.objects.filter(
            id__in=ids, company__user=self.request.user
        )

        if not queryset.exists():
            logger.warning("No valid tax declarations found for send-experts action",
                           extra={"user_id": user_id, "ids": ids})
            return Response(
                {"error": "No valid tax declarations found for the provided IDs."},
                status=status.HTTP_404_NOT_FOUND,
            )

        updated_count = queryset.update(is_sent=True)

        for instance in queryset:
            post_save.send(sender=TaxDeclaration,
                           instance=instance, created=False)

        logger.info("Marked tax declarations as sent", extra={
                    "user_id": user_id, "updated_count": updated_count})
        return Response(
            {"success": f"{updated_count} files marked as sent."},
            status=status.HTTP_200_OK,
        )


class BalanceReportViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BalanceReport.objects.filter(company__user=self.request.user).order_by('-year', 'month').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BalanceReportCreateSerializer

        return BalanceReportSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @xframe_options_exempt
    @action(detail=True, methods=['get'], url_path='pdf')
    def pdf(self, request, pk=None):
        balance_report = self.get_object()
        file_name = request.query_params.get('file_name')

        if not file_name:
            return Response({"error": "file_name query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        file_paths = {
            "balance_report_file": balance_report.balance_report_file.path,
            "profit_loss_file": balance_report.profit_loss_file.path,
            "sold_product_file": balance_report.sold_product_file.path,
            "account_turnover_file": balance_report.account_turnover_file.path,
        }

        if file_name not in file_paths:
            return Response({"error": f"File {file_name} is not valid."}, status=status.HTTP_400_BAD_REQUEST)

        file_path = file_paths[file_name]
        if not os.path.exists(file_path):

            return Response({"error": f"File {file_name} not found."}, status=status.HTTP_404_NOT_FOUND)

        response = FileResponse(open(file_path, 'rb'),
                                content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{
            file_name}.pdf"'
        response['X-Frame-Options'] = 'ALLOWALL'
        return response

    def destroy(self, request, *args, **kwargs):
        try:
            with atomic():
                instance = self.get_object()
                self.perform_destroy(instance)
                logger.info(
                    f"Balance report {instance.id} deleted successfully by user {request.user.id}")
                return Response({"success": "files deleted"}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(
                f"Failed to delete balance report {instance.id} - User: {request.user.id}, Error: {e}", exc_info=True)
            return Response({"error": "Failed to delete files"}, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        try:
            with atomic():
                file_paths = [
                    instance.balance_report_file.path,
                    instance.profit_loss_file.path,
                    instance.sold_product_file.path,
                    instance.account_turnover_file.path,
                ]

                folder_path = os.path.dirname(file_paths[0])
                # Delete each file if it exists
                for file_path in file_paths:

                    if file_path and default_storage.exists(file_path):

                        default_storage.delete(file_path)

                # If the folder is empty, delete the folder
                if folder_path and not os.listdir(folder_path):
                    os.rmdir(folder_path)
                # Delete the instance
                instance.delete()
                logger.info(
                    f"Balance report {instance.id} and all associated files deleted by user {self.request.user.id}")

        except Exception as e:
            logger.error(
                f"Failed to delete balance report files {instance.id} - User: {self.request.user.id}, Error: {e}", exc_info=True)

    @action(detail=False, methods=['get'])
    def year(self, request):

        balance_reports = self.get_queryset()
        year_month_data = {}
        for entry in balance_reports.values('year', 'month').distinct():
            year = entry['year']
            month = entry['month']
            if year not in year_month_data:
                year_month_data[year] = []

            if month not in year_month_data[year]:
                year_month_data[year].append(month)

        formatted_data = [{'year': year, 'months': sorted(
            months)} for year, months in year_month_data.items()]
        return Response(formatted_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put', 'patch'], url_path='send-experts')
    def send(self, request):
        ids = request.data.get('ids', [])
        queryset = BalanceReport.objects.filter(
            id__in=ids, company__user=self.request.user
        )

        if not queryset.exists():
            return Response(
                {"error": "No valid tax declarations found for the provided IDs."},
                status=status.HTTP_404_NOT_FOUND,
            )

        updated_count = queryset.update(is_saved=True, is_sent=True)
        for instance in queryset:
            post_save.send(sender=BalanceReport,
                           instance=instance, created=False)
        return Response(
            {"success": f"{updated_count} files marked as sent."},
            status=status.HTTP_200_OK,
        )


class RequestViewSet(viewsets.ModelViewSet):
    REQUEST_TYPES = {
        'diagnostic': DiagnosticRequestSerializer,
    }

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company = self.request.user.company
        return DiagnosticRequest.objects.filter(company=company).order_by('-updated_at')

    def get_serializer_class(self):
        request_type = self.request.query_params.get('type')
        if request_type in self.REQUEST_TYPES:
            return self.REQUEST_TYPES[request_type]
        else:
            logger.warning(
                f"Invalid request type '{request_type}' requested by user {self.request.user.id}")
            raise NotFound("The requested type doesn't exist")
