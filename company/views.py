from management.models import HumanResource
import importlib
import logging

from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.db.models import Count
from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework.views import APIView


from company.serializers import CompanyProfileSerializer, CompanyProfileCreateSerializer
from company.models import CompanyProfile

from finance.models import TaxDeclarationFile, BalanceReportFile
from tickets.models import Ticket

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
            queryset = CompanyProfile.objects.select_related(
                "user").filter(user=self.request.user)

            queryset_list = list(queryset)

            cache.set(cache_key, queryset_list)

            logger.info("Profile fetched from DB and cached",
                        extra={"user_id": self.request.user.id})
            return queryset_list
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
            queryset = self.queryset
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
            company = CompanyProfile.objects.select_related(
                "user").filter(user=request.user).first()

            if not company:
                logger.warning("Company profile not found",
                               extra={"user_id": user_id})
                return Response({"error": "Company profile not found"}, status=404)

            tax_file_count = TaxDeclarationFile.objects.filter(company=company).aggregate(
                tax_files_count=Count("id")
            )
            report_file_count = BalanceReportFile.objects.filter(company=company).aggregate(
                report_files_count=Count("id")
            )
            human_resource_count = HumanResource.objects.filter(company=company).aggregate(
                human_resource_files_count=Count("id")
            )

            tickets_count = Ticket.objects.filter(issuer=company).count()

            total_uploaded_files_count = tax_file_count["tax_files_count"] + report_file_count["report_files_count"] + human_resource_count["human_resource_files_count"]

            requests_count = {}
            for app in settings.APP_REQUEST_TYPES:
                model = getattr(importlib.import_module(
                    "request.models"), f"{app.title()}Request")
                requests_count[f"{app.lower()}_request_count"] = model.objects.filter(
                    company=company).count()

            response_data = {
                'all_uploaded_files_count': total_uploaded_files_count,
                'report_files_count': report_file_count["report_files_count"],
                'tax_files_count': tax_file_count["tax_files_count"],
                "requests_count": requests_count,
                "tickets_count": tickets_count,
            }

            cache.set(cache_key, response_data)
            logger.info("Dashboard data fetched from DB and cached",
                        extra={"user_id": user_id})
            return Response(response_data)

        except Exception as e:
            logger.error("Failed to fetch dashboard data", extra={
                         "user_id": user_id, "error": str(e)}, exc_info=True)
            return Response({"error": "An error occurred while fetching dashboard data"}, status=500)