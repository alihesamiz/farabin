from django.urls import path, include

# from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from management.views import HumanResourceViewSet, OrganizationChartFileViewSet, PersonelInformationViewSet


router = DefaultRouter()
router.register(r'human-resources', HumanResourceViewSet,
                basename='human-resources')

personel_router = NestedDefaultRouter(
    router, r'human-resources', lookup='human_resource')
personel_router.register(
    r'personel', PersonelInformationViewSet, basename='human-resource-personel')

chart_file_router = DefaultRouter()
chart_file_router.register(r'organization-chart-files',
                           OrganizationChartFileViewSet, basename='organization-chart-files')

urlpatterns = router.urls + personel_router.urls + chart_file_router.urls
