from django.urls import path


from rest_framework.routers import DefaultRouter


from company.views import CompanyProfileViewSet, DashboardViewSet



router = DefaultRouter()

router.register(r'profile', CompanyProfileViewSet, basename='profile')

urlpatterns = router.urls

urlpatterns += [path('dashboard/',
                     DashboardViewSet.as_view(), name='dashboard')]
