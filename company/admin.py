from django.contrib import messages
from django.db.transaction import atomic
from django.db import transaction
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from .models import BalanceReport, CompanyProfile, CompanyService, LifeCycle, DiagnosticRequest, TaxDeclaration, BalanceReport
# Register your models here.


class LifeCycleInline(admin.StackedInline):
    model = LifeCycle
    extra = 0
    min_num = 1
    max_num = 1


class BalanceReprotInline(admin.TabularInline):
    model = BalanceReport
    extra = 0
    min_num = 1
    max_num = 1


@admin.register(LifeCycle)
class LifeCycleAdmin(admin.ModelAdmin):
    list_display = ['capital_providing',]


@admin.register(CompanyProfile)
class CompanyAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    search_fields = ['company_title', 'manager_name']
    list_display = ['company_title', 'national_code', 'manager_name',
                    'tech_field', 'special_field_display', 'license', 'insurance_list', 'capital_providing_method_display']

    readonly_fields = ['id']

    filter_horizontal = ('capital_providing_method',)

    @admin.display(ordering='national_code')
    def national_code(self, company_profile: CompanyProfile):
        return company_profile.user.national_code
    national_code.short_description = _("National Code")

    def special_field_display(self, company_profile: CompanyProfile):
        return company_profile.special_field  # Ensure this matches the field name
    special_field_display.short_description = _("Special Field")

    @admin.display(description=_("Capital Providing Method"), ordering='capital_providing_method_display')
    def capital_providing_method_display(self, company_profile: CompanyProfile):
        return ", ".join([cycle.get_capital_providing_display() for cycle in company_profile.capital_providing_method.all()])


@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    autocomplete_fields = ['company']
    list_display = ['company', 'service', 'is_active', 'purchased_date']

    search_fields = ['company__company_title',
                     'service__description', 'purchased_date']

    @admin.action(description=_("Activate selected services"))
    def activate_services(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request,
            _("{} service(s) were successfully marked as active.").format(
                updated_count),
            messages.SUCCESS
        )

    @admin.action(description=_("Deactivate selected services"))
    def deactivate_services(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request,
            _("{} service(s) were successfully marked as deactive.").format(
                updated_count),
            messages.SUCCESS
        )

    # Add the action to the actions list
    actions = [activate_services, deactivate_services]


@admin.register(TaxDeclaration)
class TaxFileAdmin(admin.ModelAdmin):
    list_display = ['company_title', 'year', 'tax_file',
                    'is_saved',
                    'is_sent',]

    search_fields = ['company__company_title', 'year']

    @admin.display(ordering='company__company_title')
    def company_title(self, tax_declaration: TaxDeclaration):
        return tax_declaration.company.company_title
    company_title.short_description = _("Company Title")

    def delete_model(self, request: HttpRequest, obj: Any):
        with atomic():
            if obj.tax_file:
                obj.tax_file.delete(save=False)
            return super().delete_model(request, obj)

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet) -> None:
        for obj in queryset:
            with atomic():
                if obj.tax_file:
                    obj.tax_file.delete(save=False)
        return super().delete_queryset(request, queryset)

    def get_queryset(self, request):
        # Get the original queryset
        qs = super().get_queryset(request)

        # Allow superuser to view all tickets
        if request.user.is_superuser:
            return qs

        # Filter tickets based on the agent's department
        return qs.filter(is_sent=True)


@admin.register(BalanceReport)
class BalanceReportFileAdmin(admin.ModelAdmin):
    list_display = ['company_title', 'month', 'year', 'balance_report_file', 'profit_loss_file',
                    'sold_product_file',
                    'account_turnover_file',
                    'is_saved',
                    'is_sent',]

    search_fields = ['company__company_title', 'year', 'month']

    @admin.display(ordering='company__company_title')
    def company_title(self, tax_declaration: TaxDeclaration):
        return tax_declaration.company.company_title
    company_title.short_description = _("Company Title")

    def delete_model(self, request: HttpRequest, obj: Any) -> None:

        if obj:
            with transaction.atomic():
                obj.balance_report_file.delete(save=False)
                obj.profit_loss_file.delete(save=False)
                obj.sold_product_file.delete(save=False)
                obj.account_turnover_file.delete(save=False)

        return super().delete_model(request, obj)

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet) -> None:

        for obj in queryset:
            with transaction.atomic():
                obj.balance_report_file.delete(save=False)
                obj.profit_loss_file.delete(save=False)
                obj.sold_product_file.delete(save=False)
                obj.account_turnover_file.delete(save=False)

        return super().delete_queryset(request, queryset)

    def get_queryset(self, request):
        # Get the original queryset
        qs = super().get_queryset(request)

        # Allow superuser to view all tickets
        if request.user.is_superuser:
            return qs

        # Filter tickets based on the agent's department
        return qs.filter(is_sent=True)


@admin.register(DiagnosticRequest)
class CompanyDiagnosticRequestAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "status",
        "created_at",
        "updated_at",
        "service",
        "tax_record",
        "balance_record"
    ]
