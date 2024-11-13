from django.db.transaction import atomic
from django.core.files.storage import default_storage
from django.views.decorators.clickjacking import xframe_options_exempt
from django.utils.decorators import method_decorator
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework import status
from PyPDF2 import PdfReader, PdfWriter
import os
from .models import BalanceReport,  CompanyProfile, TaxDeclaration
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
            # tax_files_data = TaxDeclarationSerializer(
            #     tax_files, many=True).data
            # report_files_data = BalanceReportSerializer(
            #     report_files, many=True).data

            # Return a structured JSON response with both file types
            response_data = {
                'tax_files_count': tax_files_count,
                'report_files_count': report_files_count*4,
                'all_uploaded_files': tax_files_count + report_files_count*4,
                "tickets": 0
            }

            return Response(response_data)

        except CompanyProfile.DoesNotExist:
            return Response({"error": "Company profile not found"}, status=404)


class TaxDeclarationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaxDeclaration.objects.filter(company__user=self.request.user).order_by('-year').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return TaxDeclarationCreateSerializer
        return TaxDeclarationSerializer

    def get_serializer_context(self):
        # Pass the request to the serializer context
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            print('asdklashjdlkashdkj')
            return Response({"success": "file deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
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

        except Exception as e:
            pass

    @xframe_options_exempt
    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None,):
        tax_declaration = self.get_object()
        pdf_path = tax_declaration.tax_file.path  # Adjust based on your file field

        # Ensure the file exists
        if not os.path.exists(pdf_path):
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        response = FileResponse(open(pdf_path, 'rb'),
                                content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{
            tax_declaration.tax_file.name}"'
        # Customize X-Frame-Options if needed for frontend embedding compatibility
        response['X-Frame-Options'] = 'ALLOWALL'

        return response

    @action(detail=False, methods=['get'])
    def year(self, request):
        tax_declarations = self.get_queryset()
        years = tax_declarations.values('year').distinct()
        return Response(years, status=status.HTTP_200_OK)


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

    @method_decorator(xframe_options_exempt, name='pdf')
    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        balance_report = self.get_object()

        pdf_files = [
            balance_report.balance_report_file.path,
            balance_report.profit_loss_file.path,
            balance_report.sold_product_file.path,
            balance_report.account_turnover_file.path,
        ]

        pdf_writer = PdfWriter()

        for pdf_path in pdf_files:
            if os.path.exists(pdf_path):
                try:
                    pdf_reader = PdfReader(pdf_path)

                    if len(pdf_reader.pages) > 0:
                        pdf_writer.add_page(pdf_reader.pages[0])

                except Exception as e:
                    return Response({"error": f"Error processing {pdf_path}: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                return Response({"error": f"File not found: {pdf_path}"}, status=status.HTTP_404_NOT_FOUND)

        # Save the new PDF with the first pages
        response_pdf_path = 'first_pages.pdf'
        with open(response_pdf_path, 'wb') as output_pdf_file:
            pdf_writer.write(output_pdf_file)

        # Serve the response PDF file
        response = FileResponse(
            open(response_pdf_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="first_pages.pdf"'
        response['X-Frame-Options'] = 'ALLOWALL'  # Customize as needed

        return response

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

    def destroy(self, request, *args, **kwargs):
        try:
            with atomic():
                instance = self.get_object()
                self.perform_destroy(instance)
                return Response({"success": "files deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
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

                for file_path in file_paths:
                    if file_path and default_storage.exists(file_path):
                        default_storage.delete(file_path)

                if file_path and default_storage.exists(file_path):
                    default_storage.delete(file_path)

                if folder_path and not os.listdir(folder_path):
                    os.rmdir(folder_path)

                instance.delete()

        except Exception as e:
            pass
