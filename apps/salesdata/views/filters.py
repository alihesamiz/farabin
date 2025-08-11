from django_filters import DateFilter
from django_filters.filterset import FilterSet


class DateFilter(FilterSet):
    first_purchase_date__gte = DateFilter(
        filed_name="first_purchase_date",
        look_up_expr="gte",
        label="First Purchase Data(start)",
    )
