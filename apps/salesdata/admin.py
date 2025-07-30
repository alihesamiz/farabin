from django.contrib import admin

from apps.salesdata.models import (
    CustomerSaleData,
    CustomerSaleFile,
    DomesticSaleData,
    ProductData,
    ProductDataFile,
    ProductLog,
    ProductLogFile,
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


@admin.register(ProductLogFile)
class ProductLogFileAdmin(admin.ModelAdmin):
    list_display = ["company", "file"]


@admin.register(ProductLog)
class ProductLogAdmin(admin.ModelAdmin):
    list_display = ["product", "production_date"]


@admin.register(DomesticSaleData)
class DomesticSaleDataAdmin(admin.ModelAdmin):
    list_display = [
        "company",
    ]
