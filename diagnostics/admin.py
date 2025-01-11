from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.contrib import admin
from django.urls import reverse

from .models import (
    AccountTurnOver, AnalysisReport, FinancialData, FinancialAsset,
    ProfitLossStatement, SoldProductFee, BalanceReport
)
from company.models import CompanyProfile


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


class BalanceReportInline(admin.StackedInline):
    model = BalanceReport
    extra = 0
    min_num = 1
    max_num = 1


class AccountTurnOverInline(admin.StackedInline):
    model = AccountTurnOver
    extra = 0
    min_num = 1
    max_num = 1


@admin.register(FinancialAsset)
class FinancialAssestAdmin(admin.ModelAdmin):
    autocomplete_fields = ['company']
    list_display = ['company_title', 'year', 'month']
    inlines = [BalanceReportInline, ProfitStatementInline, SaledProductInline,
               AccountTurnOverInline]

    search_fields = [
        'company__company_title', 'year', 'month']

    list_filter = [
        'company__company_title', 'year', 'month']

    @admin.display(ordering='company_title')
    def company_title(self, financial_asset: FinancialAsset):
        return financial_asset.company.company_title
    company_title.short_description = _("Company Title")
    company_title.admin_order_field = 'company_title'


@admin.register(FinancialData)
class CalculatedDataAdmin(admin.ModelAdmin):
    autocomplete_fields = ['financial_asset']
    list_display = ['company_title', 'financial_year',
                    'financial_month', 'is_published']
    search_fields = [
        'financial_asset__company__company_title', 'financial_asset__year', 'financial_asset__month', 'is_published', "financial_asset__company__company_title"]

    list_filter = [
        'financial_asset__company__company_title', 'financial_asset__year', 'financial_asset__month', "financial_asset__company", "is_published"]

    sortable_by = ['company_title', 'financial_year', 'financial_month']

    def company_title(self, obj):
        return obj.financial_asset.company.company_title
    company_title.short_description = _('Company Title')  # Custom column name

    def financial_year(self, obj):
        return obj.financial_asset.year
    financial_year.short_description = _(
        'Year')  # Custom column name

    def financial_month(self, obj):
        return obj.financial_asset.month if obj.financial_asset.month else '-'
    financial_month.short_description = _("Month")

    def make_published(self, request, queryset):
        updated_count = queryset.update(is_published=True)
        self.message_user(request, _(
            f'{updated_count} record(s) were successfully marked as published.'))

    make_published.short_description = _('Mark selected as Published')

    # Add the custom action to the admin
    actions = ['make_published']


@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    list_display = [
        "calculated_data",
        "chart_name",
        'period',
        "text",
    ]

    autocomplete_fields = ['calculated_data']
    search_fields = [
        'calculated_data__financial_asset__company__company_title', 'chart_name', 'period']
    # list_filter = [
    #     'calculated_data__financial_asset__company__company_title', 'is_published', 'period', 'chart_name']

    actions = ['mark_as_published', 'mark_as_unpublished']

    def get_search_results(self, request, queryset, search_term):
        """
        Customize search to return only the last report for each company
        based on the search term.
        """
        company_id = request.GET.get('company')

        company_queryset = CompanyProfile.objects.filter(
            company_title__icontains=search_term)

        if company_id:
            company = CompanyProfile.objects.get(id=company_id)
            queryset = FinancialData.objects.filter(
                calculated_data__financial_asset__company=company
            ).order_by('-created_at')
        else:
            queryset = AnalysisReport.objects.filter(
                calculated_data__financial_asset__company__in=company_queryset
            ).annotate(
                latest_report=Max('created_at')
            ).order_by('-latest_report')

        return queryset, False

    def changelist_view(self, request, extra_context=None):
        companies = CompanyProfile.objects.all()

        company_financial_data = []

        for company in companies:
            financial_data = AnalysisReport.objects.filter(
                calculated_data__financial_asset__company=company
            ).last()
            company_financial_data.append({
                "company": company,
                "chart": self.chart(financial_data)
            })

        extra_context = extra_context or {}
        extra_context["company_financial_data"] = company_financial_data

        return super().changelist_view(request, extra_context=extra_context)

    def chart(self, obj):
        if obj and obj.calculated_data and obj.calculated_data.financial_asset:
            company = obj.calculated_data.financial_asset.company
            if company:
                url = reverse('company_financial_data', args=[company.id])
                return format_html('<a href="{}">{}</a>', url, company.company_title)
        return format_html('<a href="#">{}</a>', _("No data available"))
    chart.short_description = _("Chart")

    @admin.action(description=_("Mark selected reports as Published"))
    def mark_as_published(self, request, queryset):
        queryset = queryset.order_by()  # Remove ordering to allow updates
        updated_count = queryset.update(is_published=True)
        self.message_user(
            request,
            _("%d analysis report(s) marked as published.") % updated_count
        )

    @admin.action(description=_("Mark selected reports as Unpublished"))
    def mark_as_unpublished(self, request, queryset):
        queryset = queryset.order_by()  # Remove ordering to allow updates
        updated_count = queryset.update(is_published=False)
        self.message_user(
            request,
            _("%d analysis report(s) marked as unpublished.") % updated_count
        )
