from django.contrib import admin


from request.models import FinanceRequest



@admin.register(FinanceRequest)
class FinanceRequestAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "status",
        "created_at",
        "updated_at",
        "service",
        "tax_record",
        "balance_record"
    ]
