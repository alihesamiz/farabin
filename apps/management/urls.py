from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from apps.management.views import (
    ChartNodeViewSet,
    HumanResourceViewSet,
    OrganizationChartFileViewSet,
    PersonnelInformationViewSet,
    SWOTAnalysisViewSet,
    SWOTMatrixViewSet,
    SWOTOptionViewSet,
    SWOTQuestionViewSet,
)

router = DefaultRouter()
# router.register(r"human-resources", HumanResourceViewSet, basename="human-resources")
# router.register(
#     r"organization-chart-files",
#     OrganizationChartFileViewSet,
#     basename="organization-chart-files",
# )
# router.register(r"swot", SWOTMatrixViewSet, basename="swot")
# router.register(r"swot-questions", SWOTQuestionViewSet, basename="swot-questions")
# router.register(r"swot-options", SWOTOptionViewSet, basename="swot-options")


# hr_nested_router = NestedDefaultRouter(
#     router, r"human-resources", lookup="human_resource"
# )
# hr_nested_router.register(
#     r"personel", PersonelInformationViewSet, basename="human-resource-personel"
# )
# hr_nested_router.register(r"graph", ChartNodeViewSet, basename="human-resource-graph")

# swot_nested_router = NestedDefaultRouter(router, r"swot", lookup="swot")
# swot_nested_router.register(r"analysis", SWOTAnalysisViewSet, basename="swot-analysis")

# urlpatterns = router.urls + hr_nested_router.urls + swot_nested_router.urls


# Human Resources
router.register(r"human-resources", HumanResourceViewSet, basename="human-resources")
router.register(
    r"organization-charts", OrganizationChartFileViewSet, basename="organization-charts"
)  # Renamed for clarity
router.register(
    r"personnel", PersonnelInformationViewSet, basename="personnel"
)  # Moved to top-level, corrected spelling

# SWOT Resources
router.register(
    r"swot-matrices", SWOTMatrixViewSet, basename="swot-matrices"
)  # Pluralized for clarity
router.register(r"swot-questions", SWOTQuestionViewSet, basename="swot-questions")
router.register(r"swot-options", SWOTOptionViewSet, basename="swot-options")

# Nested Routes
hr_nested_router = NestedDefaultRouter(
    router, r"human-resources", lookup="human_resource"
)
hr_nested_router.register(
    r"details", HumanResourceViewSet, basename="human-resource-details"
)  # More specific than 'personel'

swot_nested_router = NestedDefaultRouter(router, r"swot-matrices", lookup="matrix")
swot_nested_router.register(
    r"analyses", SWOTAnalysisViewSet, basename="swot-analyses"
)  # Pluralized for consistency

# Organization Chart Nodes (nested under organization-charts, not human-resources)
chart_nested_router = NestedDefaultRouter(
    router, r"organization-charts", lookup="chart"
)
chart_nested_router.register(
    r"nodes", ChartNodeViewSet, basename="chart-nodes"
)  # Renamed 'graph' to 'nodes'

urlpatterns = (
    router.urls
    + hr_nested_router.urls
    + swot_nested_router.urls
    + chart_nested_router.urls
)
