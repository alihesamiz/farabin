from django_filters import DateFilter
from django_filters.filterset import FilterSet
from django_filters.rest_framework import DateFromToRangeFilter

from apps.salesdata.models import DomesticSaleData


class DateFilter(FilterSet):
    first_purchase_date__gte = DateFilter(
        filed_name="first_purchase_date",
        look_up_expr="gte",
        label="First Purchase Data(start)",
    )


class CompanyDomesticSaleFilter(FilterSet):
    sold_at = DateFromToRangeFilter()

    class Meta:
        model = DomesticSaleData
        fields = ["sold_at"]
