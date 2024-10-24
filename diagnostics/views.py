from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from rest_framework import viewsets
from .models import SoldProductFee, ProfitLossStatement, BalanceReport, AccountTurnOver, FinancialAsset
from .serializers import SoldProductFeeSerializer, ProfitLossStatementSerializer, BalanceReportSerializer, AccountTurnOverSerializer, FinancialAssetSerializer
from rest_framework.permissions import IsAuthenticated


# class SoldProductFeeViewSet(viewsets.ModelViewSet):
#     serializer_class = SoldProductFeeSerializer
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['get']

#     def get_queryset(self):
#         company = getattr(self.request.user, 'company', None)
#         if not company:
#             raise NotFound("Company profile not found for this user.")
#         return SoldProductFee.objects.filter(financial_asset__company=company)


# class ProfitLossStatementViewSet(viewsets.ModelViewSet):
#     serializer_class = ProfitLossStatementSerializer
#     http_method_names = ['get']
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         company = getattr(self.request.user, 'company', None)
#         if not company:
#             raise NotFound("Company profile not found for this user.")

#         return ProfitLossStatement.objects.filter(financial_asset__company=company)


# class BalanceReportViewSet(viewsets.ModelViewSet):
#     serializer_class = BalanceReportSerializer
#     http_method_names = ['get']
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         company = getattr(self.request.user, 'company', None)
#         if not company:
#             raise NotFound("Company profile not found for this user.")

#         return BalanceReport.objects.filter(financial_asset__company=company)


# class AccountTurnOverViewSet(viewsets.ModelViewSet):
#     serializer_class = AccountTurnOverSerializer
#     http_method_names = ['get']
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         company = getattr(self.request.user, 'company', None)
#         if not company:
#             raise NotFound("Company profile not found for this user.")

#         return AccountTurnOver.objects.filter(financial_asset__company=company)


# class FinancialAssetViewSet(viewsets.ModelViewSet):
#     serializer_class = FinancialAssetSerializer
#     http_method_names = ['get']
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         company = getattr(self.request.user, 'company', None)
#         if not company:
#             raise NotFound("Company profile not found for this user.")

#         return FinancialAsset.objects.filter(company=company)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

class FinancialDataView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        # Retrieve the company associated with the logged-in user
        company = getattr(self.request.user, 'company', None)
        if not company:
            raise NotFound("Company profile not found for this user.")

        # Get the 'type' query parameter to determine which data to return
        data_type = request.query_params.get('type')

        # Define possible serializers and querysets
        if data_type == 'sold_product_fee':
            queryset = SoldProductFee.objects.filter(financial_asset__company=company)
            serializer = SoldProductFeeSerializer(queryset, many=True)
        elif data_type == 'profit_loss_statement':
            queryset = ProfitLossStatement.objects.filter(financial_asset__company=company)
            serializer = ProfitLossStatementSerializer(queryset, many=True)
        elif data_type == 'balance_report':
            queryset = BalanceReport.objects.filter(financial_asset__company=company)
            serializer = BalanceReportSerializer(queryset, many=True)
        elif data_type == 'account_turnover':
            queryset = AccountTurnOver.objects.filter(financial_asset__company=company)
            serializer = AccountTurnOverSerializer(queryset, many=True)
        elif data_type == 'financial_asset':
            queryset = FinancialAsset.objects.filter(company=company)
            serializer = FinancialAssetSerializer(queryset, many=True)
        else:
            return Response({"detail": "Invalid data type specified."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)
