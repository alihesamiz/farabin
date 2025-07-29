from rest_framework.routers import DefaultRouter

from apps.salesdata.views import CompanyCustomerViewSet, CompanyProductViewSet
from apps.salesdata.views.views import (
    CompanyCustomerFileViewSet,
    CompanyProductFileViewSet,
    CompanyProductLogFileViewSet,
    CompanyProductLogViewSet,
)

router = DefaultRouter()
router.register("product/file", CompanyProductFileViewSet, basename="product-file")
router.register("product", CompanyProductViewSet, basename="product")

router.register("product-logs", CompanyProductLogViewSet, basename="product-log")
router.register(
    "product-logs-file", CompanyProductLogFileViewSet, basename="product-log-file"
)

router.register("customer/file", CompanyCustomerFileViewSet, basename="customer-file")
router.register("customer", CompanyCustomerViewSet, basename="customer")
urlpatterns = router.urls
