import importlib
import logging

from django.core.cache import cache
from django.db.models import Count
from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status


from apps.company.serializers import (
    CompanyProfileSerializer,
    CompanyProfileCreateSerializer,
    LifeCycleDeclineSerializer,
    LifeCycleFeatureSerializer,
    LifeCycleGrowthSerializer,
    LifeCycleIntroductionSerializer,
    LifeCycleMaturitySerializer,
    LifeCycleQuantitativePlaceCreateUpdateSerializer,
    LifeCycleQuantitativePlaceSerializer,
    LifeCycleTheoreticalPlaceCreateUpdateSerializer,
    LifeCycleTheoreticalPlaceSerializer,
)
from apps.company.models import (
    CompanyProfile,
    LifeCycleDecline,
    LifeCycleFeature,
    LifeCycleGrowth,
    LifeCycleIntroduction,
    LifeCycleMaturity,
    LifeCycleQuantitative,
    LifeCycleTheoretical,
)

from apps.finance.models import TaxDeclarationFile, BalanceReportFile
from apps.management.models import HumanResource
from apps.tickets.models import Ticket

logger = logging.getLogger("company")


class CompanyProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            queryset = CompanyProfile.objects.select_related("user").filter(
                user=self.request.user
            )

            if not queryset.exists():
                raise NotFound("Company profile not found.")

            logger.info(
                "Profile fetched from DB and cached",
                extra={"user_id": self.request.user.id},
            )
            return queryset

        except Exception as e:
            logger.error(
                "Failed to fetch profile",
                extra={"user_id": self.request.user.id, "error": str(e)},
                exc_info=True,
            )
            raise NotFound(detail="Company profile not found.")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return CompanyProfileCreateSerializer

        return CompanyProfileSerializer


class DashboardViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        cache_key = f"dashboard_data_{user_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(
                "Dashboard data retrieved from cache", extra={"user_id": user_id}
            )
            return Response(cached_data)

        try:
            company = (
                CompanyProfile.objects.select_related("user")
                .filter(user=request.user)
                .first()
            )

            if not company:
                logger.warning("Company profile not found", extra={"user_id": user_id})
                return Response({"error": "Company profile not found"}, status=404)

            tax_file_count = TaxDeclarationFile.objects.filter(
                company=company
            ).aggregate(tax_files_count=Count("id"))
            report_file_count = BalanceReportFile.objects.filter(
                company=company
            ).aggregate(report_files_count=Count("id"))
            human_resource_count = HumanResource.objects.filter(
                company=company
            ).aggregate(human_resource_files_count=Count("id"))

            tickets_count = Ticket.objects.filter(issuer=company).count()

            total_uploaded_files_count = (
                tax_file_count["tax_files_count"]
                + report_file_count["report_files_count"]
                + human_resource_count["human_resource_files_count"]
            )

            requests_count = {}
            for app in settings.APP_REQUEST_TYPES:
                model = getattr(
                    importlib.import_module("request.models"), f"{app.title()}Request"
                )
                requests_count[f"{app.lower()}_request_count"] = model.objects.filter(
                    company=company
                ).count()

            response_data = {
                "all_uploaded_files_count": total_uploaded_files_count,
                "report_files_count": report_file_count["report_files_count"],
                "tax_files_count": tax_file_count["tax_files_count"],
                "requests_count": requests_count,
                "tickets_count": tickets_count,
            }

            cache.set(cache_key, response_data)
            logger.info(
                "Dashboard data fetched from DB and cached", extra={"user_id": user_id}
            )
            return Response(response_data)

        except Exception as e:
            logger.error(
                "Failed to fetch dashboard data",
                extra={"user_id": user_id, "error": str(e)},
                exc_info=True,
            )
            return Response(
                {"error": "An error occurred while fetching dashboard data"}, status=500
            )


class LifeCycleFeatureViewSet(viewsets.ModelViewSet):
    queryset = LifeCycleFeature.objects.all()
    serializer_class = LifeCycleFeatureSerializer


class LifeCycleDeclineViewSet(viewsets.ModelViewSet):
    queryset = LifeCycleDecline.objects.all()
    serializer_class = LifeCycleDeclineSerializer


class LifeCycleMaturityViewSet(viewsets.ModelViewSet):
    queryset = LifeCycleMaturity.objects.all()
    serializer_class = LifeCycleMaturitySerializer


class LifeCycleGrowthViewSet(viewsets.ModelViewSet):
    queryset = LifeCycleGrowth.objects.all()
    serializer_class = LifeCycleGrowthSerializer


class LifeCycleIntroductionViewSet(viewsets.ModelViewSet):
    queryset = LifeCycleIntroduction.objects.all()
    serializer_class = LifeCycleIntroductionSerializer


class LifeCycleStateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        kind = self.request.query_params.get("kind")
        match kind:
            case "theoretical":
                if self.action in ["update", "partial_update", "create"]:
                    return LifeCycleTheoreticalPlaceCreateUpdateSerializer
                return LifeCycleTheoreticalPlaceSerializer
            case "quantitative":
                if self.action in ["update", "partial_update", "create"]:
                    return LifeCycleQuantitativePlaceCreateUpdateSerializer
                return LifeCycleQuantitativePlaceSerializer
            case _:
                raise NotFound(
                    detail="Kind not recognized.",
                    code=status.HTTP_404_NOT_FOUND,
                )

    def get_queryset(self):
        company = getattr(self.request.user, "company", None)
        if not company:
            raise NotFound(
                detail="User is not associated with any company.",
                code=status.HTTP_404_NOT_FOUND,
            )

        kind = self.request.query_params.get("kind")
        match kind:
            case "theoretical":
                return LifeCycleTheoretical.objects.select_related(
                    "company",
                    "feature",
                    "decline",
                    "maturity",
                    "growth",
                    "introduction",
                ).filter(company=company)
            case "quantitative":
                return (
                    LifeCycleQuantitative.objects.select_related("company")
                    .prefetch_related("resource")
                    .filter(company=company)
                )
            case _:
                raise NotFound(
                    detail='Kind not recognized. choices are: "theoretical", "quantitative" ',
                    code=status.HTTP_404_NOT_FOUND,
                )
