from celery.result import AsyncResult
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status

from company.models import CompanyProfile
from .serializers import SoldProductFeeSerializer, ProfitLossStatementSerializer, BalanceReportSerializer, AccountTurnOverSerializer, FinancialAssetSerializer
from .models import SoldProductFee, ProfitLossStatement, BalanceReport, AccountTurnOver, FinancialAsset
from .tasks import perform_calculations

# class FinancialDataView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         # Retrieve the company associated with the logged-in user
#         company = getattr(self.request.user, 'company', None)
#         if not company:
#             raise NotFound("Company profile not found for this user.")

#         # Get the 'type' query parameter to determine which data to return
#         data_type = request.query_params.get('type')

#         # Define possible serializers and querysets
#         if data_type == 'sold_product_fee':
#             queryset = SoldProductFee.objects.filter(
#                 financial_asset__company=company)
#             serializer = SoldProductFeeSerializer(queryset, many=True)
#         elif data_type == 'profit_loss_statement':
#             queryset = ProfitLossStatement.objects.filter(
#                 financial_asset__company=company)
#             serializer = ProfitLossStatementSerializer(queryset, many=True)
#         elif data_type == 'balance_report':
#             queryset = BalanceReport.objects.filter(
#                 financial_asset__company=company)
#             serializer = BalanceReportSerializer(queryset, many=True)
#         elif data_type == 'account_turnover':
#             queryset = AccountTurnOver.objects.filter(
#                 financial_asset__company=company)
#             serializer = AccountTurnOverSerializer(queryset, many=True)
#         elif data_type == 'financial_asset':
#             queryset = FinancialAsset.objects.filter(company=company)
#             serializer = FinancialAssetSerializer(queryset, many=True)
#         else:
#             return Response({"detail": "Invalid data type specified."}, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.data)


class DiagnosticAnalysisView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        company_id = CompanyProfile.objects.get(user=self.request.user).id

        financial_asset_ids = list(FinancialAsset.objects.filter(
            company_id=company_id
        ).order_by('year').values_list('id', flat=True))

        # financial_assets = FinancialAsset.objects.filter(
        #     company_id=company_id).order_by('year')

        # Trigger the background task
        # task = perform_calculations.delay(financial_asset_ids)
        task = perform_calculations.delay(financial_asset_ids)
        print(task)

        # Return task ID for tracking
        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)

    def get(self, request, *args, **kwargs):
        task_id = request.query_params.get('task_id')

        if not task_id:
            return Response({"error": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the task result using the task ID
        task_result = AsyncResult(task_id)

        if task_result.ready():
            return Response({"result": task_result.result}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "Processing"}, status=status.HTTP_202_ACCEPTED)
