from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from management.views import (
    ChartNodeViewSet,
    HumanResourceViewSet,
    OrganizationChartFileViewSet,
    PersonelInformationViewSet,
    SWOTMatrixViewSet,
    SWOTOptionViewSet,
    SWOTQuestionViewSet,
)

router = DefaultRouter()
router.register(r"human-resources", HumanResourceViewSet, basename="human-resources")
router.register(
    r"organization-chart-files",
    OrganizationChartFileViewSet,
    basename="organization-chart-files",
)
router.register(r"swot", SWOTMatrixViewSet, basename="swot")
router.register(r"swot/questions", SWOTQuestionViewSet, basename="swot-questions")
router.register(r"swot-options", SWOTOptionViewSet, basename="swot-options")


hr_nested_router = NestedDefaultRouter(
    router, r"human-resources", lookup="human_resource"
)
hr_nested_router.register(
    r"personel", PersonelInformationViewSet, basename="human-resource-personel"
)
hr_nested_router.register(r"graph", ChartNodeViewSet, basename="human-resource-graph")

urlpatterns = router.urls + hr_nested_router.urls
