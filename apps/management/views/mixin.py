from apps.company.models.company import ServiceName
from common import ViewSetMixin as _mixin


class ViewSetMixin(_mixin):
    service_attr = ServiceName.MANAGEMENT
