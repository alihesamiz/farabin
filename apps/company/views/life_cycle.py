from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework import status


from apps.company.serializers import (
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
    LifeCycleDecline,
    LifeCycleFeature,
    LifeCycleGrowth,
    LifeCycleIntroduction,
    LifeCycleMaturity,
    LifeCycleQuantitative,
    LifeCycleTheoretical,
)


class LifeCycleFeatureViewSet(ModelViewSet):
    queryset = LifeCycleFeature.objects.all()
    serializer_class = LifeCycleFeatureSerializer


class LifeCycleDeclineViewSet(ModelViewSet):
    queryset = LifeCycleDecline.objects.all()
    serializer_class = LifeCycleDeclineSerializer


class LifeCycleMaturityViewSet(ModelViewSet):
    queryset = LifeCycleMaturity.objects.all()
    serializer_class = LifeCycleMaturitySerializer


class LifeCycleGrowthViewSet(ModelViewSet):
    queryset = LifeCycleGrowth.objects.all()
    serializer_class = LifeCycleGrowthSerializer


class LifeCycleIntroductionViewSet(ModelViewSet):
    queryset = LifeCycleIntroduction.objects.all()
    serializer_class = LifeCycleIntroductionSerializer


class LifeCycleStateViewSet(ModelViewSet):
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
                return LifeCycleTheoreticalPlaceSerializer
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
