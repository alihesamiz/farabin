from rest_framework.decorators import action
from diagnostics.serializers import AssetChartSerializer, DebtChartSerializer, FinancialDataSerializer
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

    CHART_SERIALIZER_MAP = {
        'debt': DebtChartSerializer,
        'asset': AssetChartSerializer,
    }

    def get_serializer_class(self):
        if self.action == "chart":
            chart = self.kwargs.get('slug')
            serializer_class = self.CHART_SERIALIZER_MAP.get(chart)

            if serializer_class is None:
                # Raise a 404 error if the slug is not found in the map
                raise NotFound(
                    detail=f"No serializer found for slug '{chart}'.")

            return serializer_class

        return super().get_serializer_class()

    def get_queryset(self):

        company = self.request.user.company

        return FinancialData.objects.select_related('financial_asset').prefetch_related('analysis_reports').filter(financial_asset__company=company)

    @action(detail=False, methods=['get'], url_path='chart/(?P<slug>[^/.]+)', url_name='chart')
    def chart(self, request, slug=None):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Use the correct serializer and apply many=True if serializing a queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
