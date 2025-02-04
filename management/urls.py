from django.urls import path, include

from rest_framework.routers import DefaultRouter

from management.views import HumanResourceViewSet, OrganizationChartFileViewSet,PersonelInformationViewSet


hr_router = DefaultRouter()
hr_router.register(r'human-resources', HumanResourceViewSet, basename='human-resources')

personel_router = DefaultRouter()
personel_router.register(r'personel', PersonelInformationViewSet, basename='human-resource-personel')

chart_file_router = DefaultRouter()
chart_file_router.register(r'organization-chart-files', OrganizationChartFileViewSet, basename='organization-chart-files')

urlpatterns = hr_router.urls + personel_router.urls+chart_file_router.urls

