from django.contrib.admin import site as admin_site
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View

from apps.company.models import CompanyProfile
from apps.finance.models import (
    FinancialData,
)


@method_decorator(staff_member_required, name="dispatch")
class CompanyFinancialDataView(View):
    def get(self, request, company_id):
        company = CompanyProfile.objects.get(id=company_id)

        cache_key = f"company_admin_financial_data_{company_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            financial_data = cached_data

        else:
            financial_data = (
                FinancialData.objects.select_related(
                    "financial_asset", "financial_asset__company"
                )
                .filter(financial_asset__company=company)
                .order_by("financial_asset__year", "financial_asset__month")
            )

        cache.set(cache_key, financial_data)

        admin_context = admin_site.each_context(request)
        admin_context["breadcrumbs"] = [
            {"name": _("Home"), "url": reverse("admin:index")},
            {"name": _("finance"), "url": "/admin/finance/"},
            {
                "name": _("Analysis Reports"),
                "url": reverse("admin:finance_analysisreport_changelist"),
            },
            {"name": company.title, "url": ""},
        ]

        year = []
        month = []
        net_sale = []
        non_current_asset = []
        current_asset = []
        total_asset = []
        non_current_debt = []
        current_debt = []
        total_debt = []
        altman_bankrupsy_ratio = []
        total_equity = []
        total_debt = []
        total_sum_equity_debt = []
        inventory = []
        salary_fee = []
        production_fee = []
        salary_production_fee = []
        roa = []
        roab = []
        roe = []
        usability = []
        efficiency = []
        gross_profit_margin = []
        profit_margin_ratio = []
        debt_ratio = []
        capital_ratio = []
        proprietary_ratio = []
        equity_per_total_debt_ratio = []
        equity_per_total_non_current_asset_ratio = []
        instant_ratio = []
        current_ratio = []
        stock_turnover = []
        gross_profit = []
        operational_profit = []
        proceed_profit = []
        net_profit = []
        construction_overhead = []
        consuming_material = []
        production_total_price = []

        for data in financial_data:
            year.append(float(data.financial_asset.year))
            month.append(
                float(data.financial_asset.month) if data.financial_asset.month else ""
            )
            net_sale.append(float(data.net_sale))
            non_current_asset.append(float(data.non_current_asset))
            current_asset.append(float(data.current_asset))
            total_asset.append(float(data.total_asset))
            non_current_debt.append(float(data.non_current_debt))
            current_debt.append(float(data.current_debt))
            altman_bankrupsy_ratio.append(float(data.altman_bankrupsy_ratio))
            total_equity.append(float(data.total_equity))
            total_debt.append(float(data.total_debt))
            total_sum_equity_debt.append(float(data.total_sum_equity_debt))
            inventory.append(float(data.inventory_average))
            salary_fee.append(float(data.salary_fee))
            production_fee.append(float(data.production_fee))
            salary_production_fee.append(float(data.salary_production_fee))
            roa.append(float(data.roa))
            roab.append(float(data.roab))
            roe.append(float(data.roe))
            usability.append(float(data.usability))
            efficiency.append(float(data.efficiency))
            gross_profit_margin.append(float(data.gross_profit_margin))
            profit_margin_ratio.append(float(data.profit_margin_ratio))
            debt_ratio.append(float(data.debt_ratio))
            capital_ratio.append(float(data.capital_ratio))
            proprietary_ratio.append(float(data.proprietary_ratio))
            equity_per_total_debt_ratio.append(float(data.equity_per_total_debt_ratio))
            equity_per_total_non_current_asset_ratio.append(
                float(data.equity_per_total_non_current_asset_ratio)
            )
            instant_ratio.append(float(data.instant_ratio))
            current_ratio.append(float(data.current_ratio))
            stock_turnover.append(float(data.stock_turnover))
            gross_profit.append(float(data.gross_profit))
            operational_profit.append(float(data.operational_profit))
            proceed_profit.append(float(data.proceed_profit))
            net_profit.append(float(data.net_profit))
            construction_overhead.append(float(data.construction_overhead))
            consuming_material.append(float(data.consuming_material))
            production_total_price.append(float(data.production_total_price))

        return render(
            request,
            "finance/company_financial_data.html",
            {
                "company": company,
                "financial_data": financial_data,
                "year": year,
                "month": month,
                "net_sale": net_sale,
                "non_current_asset": non_current_asset,
                "current_asset": current_asset,
                "total_asset": total_asset,
                "non_current_debt": non_current_debt,
                "current_debt": current_debt,
                "total_debt": total_debt,
                "altman_bankrupsy_ratio": altman_bankrupsy_ratio,
                "total_equity": total_equity,
                "total_sum_equity_debt": total_sum_equity_debt,
                "inventory": inventory,
                "salary_fee": salary_fee,
                "production_fee": production_fee,
                "salary_production_fee": salary_production_fee,
                "roa": roa,
                "roab": roab,
                "roe": roe,
                "efficiency": efficiency,
                "gross_profit_margin": gross_profit_margin,
                "profit_margin_ratio": profit_margin_ratio,
                "debt_ratio": debt_ratio,
                "capital_ratio": capital_ratio,
                "proprietary_ratio": proprietary_ratio,
                "equity_per_total_debt_ratio": equity_per_total_debt_ratio,
                "equity_per_total_non_current_asset_ratio": equity_per_total_non_current_asset_ratio,
                "instant_ratio": instant_ratio,
                "current_ratio": current_ratio,
                "stock_turnover": stock_turnover,
                "gross_profit": gross_profit,
                "operational_profit": operational_profit,
                "proceed_profit": proceed_profit,
                "net_profit": net_profit,
                "construction_overhead": construction_overhead,
                "consuming_material": consuming_material,
                "production_total_price": production_total_price,
                **admin_context,
            },
        )
