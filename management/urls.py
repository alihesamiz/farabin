from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from management.views import ChartNodeViewSet, HumanResourceViewSet, OrganizationChartFileViewSet, PersonelInformationViewSet, SWOTStrengthOptionViewSet, SWOTWeaknessOptionViewSet, SWOTOppotunityOptionViewSet, SWOTThreatOptionViewSet, SWOTMatrixViewSet

router = DefaultRouter()
router.register(r'human-resources', HumanResourceViewSet,
                basename='human-resources')
router.register(r'organization-chart-files',
                OrganizationChartFileViewSet, basename='organization-chart-files')

nested_router = NestedDefaultRouter(
    router, r'human-resources', lookup='human_resource')
nested_router.register(r'personel', PersonelInformationViewSet,
                       basename='human-resource-personel')
nested_router.register(r'graph', ChartNodeViewSet,
                       basename='human-resource-graph')
nested_router.register(r'swot', SWOTMatrixViewSet, basename='swot')
nested_router.register(
    r'strength', SWOTStrengthOptionViewSet, basename='swot-strength')


urlpatterns = router.urls + nested_router.urls
