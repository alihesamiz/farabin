from diagnostics.serializers import FinancialDataSerializer
from .models import AnalysisReport, FinancialData
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from celery.result import AsyncResult

from company.models import CompanyProfile
from diagnostics.utils import get_life_cycle
from .models import FinancialAsset
from .tasks import perform_calculations


# class DiagnosticAnalysisView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request, *args, **kwargs):

#         company_id = CompanyProfile.objects.get(user=self.request.user).id

#         financial_asset_ids = list(FinancialAsset.objects.filter(
#             company_id=company_id
#         ).order_by('year').values_list('id', flat=True))

#         task = perform_calculations.delay(financial_asset_ids ,company_id)

#         return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)

#     def get(self, request, *args, **kwargs):
#         task_id = request.query_params.get('task_id')

#         if not task_id:
#             return Response({"error": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Fetch the task result using the task ID
#         task_result = AsyncResult(task_id)

#         if task_result.ready():
#             return Response({"result": task_result.result}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "Processing"}, status=status.HTTP_202_ACCEPTED)


class DiagnosticAnalysisViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = FinancialDataSerializer

    def get_queryset(self):
        company = self.request.user.company
        return FinancialData.objects.select_related('financial_asset').prefetch_related('analysis_reports').filter(financial_asset__company=company)


# class AnalysisReportViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = AnalysisReportSerializer

#     def get_queryset(self):
#         # Access the user's company through the related financial asset data
#         user_company = self.request.user.company
#         return AnalysisReport.objects.select_related(
#             'calculated_data__financial_asset'
#         ).filter(
#             calculated_data__financial_asset__company=user_company
#         )
