# from django.core.cache import cache

from apps.finance.repositories import FinanceRepository as _repo


class FinanceService:
    def __init__(self, company):
        self.company = company

    def get_analysis_summary_data(self):
        all_analysis_items = _repo.get_financial_analysis_for_company(self.company)

        monthly_items = [item for item in all_analysis_items if item.period == "m"]
        yearly_items = [item for item in all_analysis_items if item.period == "y"]

        latest_monthly_reports = {
            item.chart_name: item for item in reversed(monthly_items)
        }
        latest_yearly_reports = {
            item.chart_name: item for item in reversed(yearly_items)
        }

        result = {
            "monthly_analysis": latest_monthly_reports,
            "yearly_analysis": latest_yearly_reports,
        }

        return result
