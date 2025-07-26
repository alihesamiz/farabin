from typing import Any

from django.contrib import admin
from django.db import transaction
from django.db.models import Max
from django.db.models.query import QuerySet
from django.db.transaction import atomic
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from apps.company.models import CompanyProfile
from apps.finance.models import (
    AccountTurnOver,
    AnalysisReport,
    BalanceReport,
    BalanceReportFile,
    FinanceExcelFile,
    FinancialAsset,
    FinancialData,
    Inflation,
    ProfitLossStatement,
    SoldProductFee,
    TaxDeclarationFile,
)


class ProfitStatementInline(admin.StackedInline):
    model = ProfitLossStatement
    extra = 0
    min_num = 1
    max_num = 1


class SaledProductInline(admin.StackedInline):
    model = SoldProductFee
    extra = 0
    min_num = 1
    max_num = 1


class AccountTurnOverInline(admin.StackedInline):
    model = AccountTurnOver
    extra = 0
    min_num = 1
    max_num = 1


class BalanceReportInline(admin.StackedInline):
    model = BalanceReport
    extra = 0
    min_num = 1
    max_num = 1


@admin.register(FinanceExcelFile)
class FinanceExcelFileAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "file",
        "is_saved",
        "is_sent",
    ]

    search_fields = ["company__title"]

    @admin.display(description=_("Company Title"), ordering="company__title")
    def title(self, finance_excel: FinanceExcelFile):
        return finance_excel.company.title if finance_excel.company.title else "-"

    def delete_model(self, request: HttpRequest, obj: Any):
        with atomic():
            if obj.file:
                obj.file.delete(save=False)
            return super().delete_model(request, obj)

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet) -> None:
        for obj in queryset:
            with atomic():
                if obj.file:
                    obj.file.delete(save=False)
        return super().delete_queryset(request, queryset)

    def get_queryset(self, request):
        # Get the original queryset
        qs = super().get_queryset(request)

        # Allow superuser to view all tickets
        if request.user.is_superuser:
            return qs

        # Filter tickets based on the agent's department
        return qs.filter(is_sent=True)


@admin.register(TaxDeclarationFile)
class TaxFileAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "year",
        "file",
        "is_saved",
        "is_sent",
    ]

    search_fields = ["company__title", "year"]

    @admin.display(description=_("Company Title"), ordering="company__title")
    def title(self, tax_declaration: TaxDeclarationFile):
        return tax_declaration.company.title if tax_declaration.company.title else "-"

    def delete_model(self, request: HttpRequest, obj: Any):
        with atomic():
            if obj.file:
                obj.file.delete(save=False)
            return super().delete_model(request, obj)

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet) -> None:
        for obj in queryset:
            with atomic():
                if obj.file:
                    obj.file.delete(save=False)
        return super().delete_queryset(request, queryset)

    def get_queryset(self, request):
        # Get the original queryset
        qs = super().get_queryset(request)

        # Allow superuser to view all tickets
        if request.user.is_superuser:
            return qs

        # Filter tickets based on the agent's department
        return qs.filter(is_sent=True)


@admin.register(BalanceReportFile)
class BalanceReportFileAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "month",
        "year",
        "balance_report_file",
        "profit_loss_file",
        "sold_product_file",
        "account_turnover_file",
        "is_saved",
        "is_sent",
    ]

    search_fields = ["company__title", "year", "month"]

    @admin.display(description=_("Company Title"), ordering="company__title")
    def title(self, tax_declaration: TaxDeclarationFile):
        return tax_declaration.company.title

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


@admin.register(FinancialAsset)
class FinancialAssestAdmin(admin.ModelAdmin):
    autocomplete_fields = ["company"]
    list_display = ["title", "year", "month"]
    inlines = [
        BalanceReportInline,
        ProfitStatementInline,
        SaledProductInline,
        AccountTurnOverInline,
    ]

    search_fields = ["company__title", "year", "month"]

    list_filter = ["company__title", "year", "month"]

    @admin.display(ordering="title", description=_("Company Title"))
    def title(self, financial_asset: FinancialAsset):
        return financial_asset.company.title


@admin.register(FinancialData)
class CalculatedDataAdmin(admin.ModelAdmin):
    autocomplete_fields = ["financial_asset"]
    list_display = [
        "title",
        "financial_year",
        "financial_month",
        "is_published",
    ]
    search_fields = [
        "financial_asset__company__title",
        "financial_asset__year",
        "financial_asset__month",
        "is_published",
        "financial_asset__company__title",
    ]

    list_filter = [
        "financial_asset__company__title",
        "financial_asset__year",
        "financial_asset__month",
        "financial_asset__company",
        "is_published",
    ]

    sortable_by = ["title", "financial_year", "financial_month"]

    def title(self, obj):
        return obj.financial_asset.company.title

    title.short_description = _("Company Title")  # Custom column name

    def financial_year(self, obj):
        return obj.financial_asset.year

    financial_year.short_description = _("Year")  # Custom column name

    def financial_month(self, obj):
        return obj.financial_asset.month if obj.financial_asset.month else "-"

    financial_month.short_description = _("Month")

    def make_published(self, request, queryset):
        updated_count = queryset.update(is_published=True)
        self.message_user(
            request,
            _(f"{updated_count} record(s) were successfully marked as published."),
        )

    make_published.short_description = _("Mark selected as Published")

    # Add the custom action to the admin
    actions = ["make_published"]


@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    list_display = [
        "calculated_data",
        "chart_name",
        "period",
        "text",
    ]

    autocomplete_fields = ["calculated_data"]
    search_fields = [
        "calculated_data__financial_asset__company__title",
        "chart_name",
        "period",
    ]
    # list_filter = [
    #     'calculated_data__financial_asset__company__title', 'is_published', 'period', 'chart_name']

    actions = ["mark_as_published", "mark_as_unpublished"]

    def get_search_results(self, request, queryset, search_term):
        """
        Customize search to return only the last report for each company
        based on the search term.
        """
        company_id = request.GET.get("company")

        company_queryset = CompanyProfile.objects.filter(title__icontains=search_term)

        if company_id:
            company = CompanyProfile.objects.get(id=company_id)
            queryset = FinancialData.objects.filter(
                calculated_data__financial_asset__company=company
            ).order_by("-created_at")
        else:
            queryset = (
                AnalysisReport.objects.filter(
                    calculated_data__financial_asset__company__in=company_queryset
                )
                .annotate(latest_report=Max("created_at"))
                .order_by("-latest_report")
            )

        return queryset, False

    def changelist_view(self, request, extra_context=None):
        companies = CompanyProfile.objects.all()

        company_financial_data = []

        for company in companies:
            financial_data = AnalysisReport.objects.filter(
                calculated_data__financial_asset__company=company
            ).last()
            company_financial_data.append(
                {"company": company, "chart": self.chart(financial_data)}
            )

        extra_context = extra_context or {}
        extra_context["company_financial_data"] = company_financial_data

        return super().changelist_view(request, extra_context=extra_context)

    def chart(self, obj):
        if obj and obj.calculated_data and obj.calculated_data.financial_asset:
            company = obj.calculated_data.financial_asset.company
            if company:
                url = reverse("company_financial_data", args=[company.id])
                return format_html('<a href="{}">{}</a>', url, company.title)
        return format_html('<a href="#">{}</a>', _("No data available"))

    chart.short_description = _("Chart")

    @admin.action(description=_("Mark selected reports as Published"))
    def mark_as_published(self, request, queryset):
        queryset = queryset.order_by()  # Remove ordering to allow updates
        updated_count = queryset.update(is_published=True)
        self.message_user(
            request, _("%d analysis report(s) marked as published.") % updated_count
        )

    @admin.action(description=_("Mark selected reports as Unpublished"))
    def mark_as_unpublished(self, request, queryset):
        queryset = queryset.order_by()  # Remove ordering to allow updates
        updated_count = queryset.update(is_published=False)
        self.message_user(
            request, _("%d analysis report(s) marked as unpublished.") % updated_count
        )


@admin.register(Inflation)
class InflationAdmin(admin.ModelAdmin):
    list_display = ["year", "cpi_value", "inflation_rate"]
    search_fields = ["year"]
    list_per_page = 20
