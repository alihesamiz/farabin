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
            tax_files_data = TaxDeclarationSerializer(
                tax_files, many=True).data
            report_files_data = BalanceReportSerializer(
                report_files, many=True).data

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

    def perform_destroy(self, instance):
        try:
            instance.delete()
            return Response({"success": "file deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "Failed to delete file"}, status=status.HTTP_400_BAD_REQUEST)

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

    # @method_decorator(xframe_options_exempt, name='pdf')
    # @action(detail=True, methods=['get'])
    # def pdf(self, request, pk=None):
    #     tax_declaration = self.get_object()
    #     pdf_path = tax_declaration.tax_file.path  # Adjust based on your file field

    #     # Ensure the file exists
    #     if not os.path.exists(pdf_path):
    #         return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    #     # Read the PDF and extract the first page
    #     try:
    #         pdf_reader = PdfReader(pdf_path)
    #         pdf_writer = PdfWriter()

    #         if len(pdf_reader.pages) > 0:  # Check if the PDF has at least one page
    #             # Add the first page to the writer
    #             pdf_writer.add_page(pdf_reader.pages[0])

    #             # Create a response PDF file in memory
    #             response_pdf_path = 'first_page.pdf'
    #             with open(response_pdf_path, 'wb') as output_pdf_file:
    #                 pdf_writer.write(output_pdf_file)

    #             # Serve the response PDF file
    #             response = FileResponse(
    #                 open(response_pdf_path, 'rb'), content_type='application/pdf')
    #             response['Content-Disposition'] = f'attachment; filename="{
    #                 tax_declaration.tax_file.name}"'
    #             response['X-Frame-Options'] = 'ALLOWALL'  # Customize as needed

    #             return response
    #         else:
    #             return Response({"error": "PDF has no pages"}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as e:
    #         return Response({"error": f"Error processing the PDF: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # @method_decorator(xframe_options_exempt, name='pdf')
    # @action(detail=True, methods=['get'])
    # def pdf(self, request, pk=None):
    #     tax_declaration = self.get_object()
    #     pdf_path = tax_declaration.tax_file.path  # Adjust based on your file field

    #     # Ensure the file exists
    #     if not os.path.exists(pdf_path):
    #         return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    #     try:
    #         # Convert the first page of the PDF to an image
    #         images = convert_from_path(pdf_path, first_page=1, last_page=1)
    #         if images:
    #             # Use BytesIO to create an in-memory binary stream for the image
    #             img_stream = BytesIO()
    #             images[0].save(img_stream, format='PNG')
    #             # Move the cursor to the beginning of the stream
    #             img_stream.seek(0)

    #             # Create an HTTP response with the image
    #             response = HttpResponse(
    #                 img_stream.read(), content_type='image/png')
    #             response['Content-Disposition'] = f'inline; filename="{
    #                 tax_declaration.tax_file.name}.png"'
    #             response['X-Frame-Options'] = 'ALLOWALL'  # Customize as needed

    #             return response
    #         else:
    #             return Response({"error": "PDF has no pages"}, status=status.HTTP_404_NOT_FOUND)

    #     except Exception as e:
    #         return Response({"error": f"Error processing the PDF: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BalanceReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BalanceReport.objects.filter(company__user=self.request.user).order_by('-year', '-month').all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return BalanceReportCreateSerializer
        return BalanceReportSerializer

    def get_serializer_context(self):
        # Pass the request to the serializer context
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @method_decorator(xframe_options_exempt, name='pdf')
    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        balance_report = self.get_object()

        # Paths to each of the PDF files
        pdf_files = [
            balance_report.balance_report_file.path,
            balance_report.profit_loss_file.path,
            balance_report.sold_product_file.path,
            balance_report.account_turnover_file.path,
        ]

        pdf_writer = PdfWriter()

        for pdf_path in pdf_files:
            if os.path.exists(pdf_path):
                # Read the PDF and extract the first page
                try:
                    pdf_reader = PdfReader(pdf_path)
                    if len(pdf_reader.pages) > 0:  # Check if the PDF has at least one page
                        # Add the first page to the writer
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

        # Format the data for the response
        formatted_data = [{'year': year, 'months': sorted(
            months)} for year, months in year_month_data.items()]

        return Response(formatted_data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        try:
            instance.delete()
            return Response({"success": "file deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": "Failed to delete file"}, status=status.HTTP_400_BAD_REQUEST)
