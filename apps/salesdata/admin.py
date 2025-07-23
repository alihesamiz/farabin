from django.contrib import admin

from apps.salesdata.models import (
    ProductDataFile,
    ProductData,
    CustomerSaleData,
    ForeignSaleData,
    DomesticSaleData,
    CustomerSaleFile,
)


@admin.register(ProductData)
class ProductDataAdmin(admin.ModelAdmin):
    list_display = ["company", "code", "name"]


@admin.register(CustomerSaleData)
class CustomerSaleDataAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "name",
        "sale_area",
        "channel",
    ]


@admin.register(CustomerSaleFile)
class CustomerSaleFileAdmin(admin.ModelAdmin):
    list_display = ["company", "file"]


@admin.register(ProductDataFile)
class ProductDataFileAdmin(admin.ModelAdmin):
    list_display = ["company", "file"]
