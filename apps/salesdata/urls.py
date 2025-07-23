from rest_framework.routers import DefaultRouter

from apps.salesdata.views import CompanyProductViewSet
from apps.salesdata.views import CompanyCustomerViewSet
from apps.salesdata.views.views import (
    CompanyCustomerFileViewSet,
    CompanyProductFileViewSet,
)


router = DefaultRouter()
router.register("product/file", CompanyProductFileViewSet, basename="product-file")
router.register("product", CompanyProductViewSet, basename="product")

router.register("customer/file", CompanyCustomerFileViewSet, basename="customer-file")
router.register("customer", CompanyCustomerViewSet, basename="customer")
urlpatterns = router.urls
