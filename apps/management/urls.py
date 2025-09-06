from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from apps.management.views import (
    ChartNodeViewSet,
    HumanResourceViewSet,
    OrganizationChartFileViewSet,
    PersonelInformationViewSet,
)

router = DefaultRouter()

# Human Resources
router.register(
    r"human-resources",
    HumanResourceViewSet,
    basename="human-resources",
)
router.register(
    r"organization-charts",
    OrganizationChartFileViewSet,
    basename="organization-charts",
)
router.register(
    r"personnel",
    PersonelInformationViewSet,     
    basename="personnel",
)


# Nested Routes
hr_nested_router = NestedDefaultRouter(
    router,
    r"human-resources",
    lookup="human_resource",
)
hr_nested_router.register(
    r"details",
    HumanResourceViewSet,
    basename="human-resource-details",
)

# Organization Chart Nodes (nested under organization-charts, not human-resources)
chart_nested_router = NestedDefaultRouter(
    router, r"organization-charts", lookup="chart"
)
chart_nested_router.register(
    r"nodes", ChartNodeViewSet, basename="chart-nodes"
)  # Renamed 'graph' to 'nodes'

urlpatterns = router.urls + hr_nested_router.urls + chart_nested_router.urls
