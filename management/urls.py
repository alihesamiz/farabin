from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from management.views import ChartNodeViewSet, HumanResourceViewSet, OrganizationChartFileViewSet, PersonelInformationViewSet


router = DefaultRouter()
router.register(r'human-resources', HumanResourceViewSet,
                basename='human-resources')

personel_router = NestedDefaultRouter(
    router, r'human-resources', lookup='human_resource')

personel_router.register(
    r'personel', PersonelInformationViewSet, basename='human-resource-personel')


personel_router.register(
    r'graph', ChartNodeViewSet, basename='human-resource-graph')

chart_file_router = DefaultRouter()
chart_file_router.register(r'organization-chart-files',
                           OrganizationChartFileViewSet, basename='organization-chart-files')

urlpatterns = router.urls + personel_router.urls + chart_file_router.urls
