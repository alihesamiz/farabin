from rest_framework import filters

from apps.company.models import ServiceName
from apps.salesdata.views.pagination import BasePagination
from common import ViewSetMixin as _mixin


class ViewSetMixin(_mixin):
    service_attr = ServiceName.MARKETING
    pagination_class = BasePagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
