import time
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FinancialAsset, FinancialData
from .tasks import perform_calculations
from celery.result import AsyncResult
from .utils import FinancialCalculations

# Trigger task after FinancialAsset is saved or deleted


@receiver([post_save, post_delete], sender=FinancialAsset)
def trigger_calculation_task(sender, instance, **kwargs):
    # Collect all related financial asset IDs for the company
    financial_asset_ids = FinancialAsset.objects.filter(
        company=instance.company
    ).order_by('year', 'month').values_list('id', flat=True)
    print('asdasdasd')
    print(financial_asset_ids)
    print(instance.id)
    print(instance)
    # financial_assets = FinancialAsset.objects.filter(
    #     id__in=financial_asset_ids).order_by('year', 'month')
    financial_calculator = FinancialCalculations(instance).process_assets()
    results = financial_calculator.get_results()['data']
    FinancialData.objects.create(
        financial_asset=instance,
        current_asset=results['current_asset'],
        non_current_asset=results['non_current_asset'],
        total_asset=results['total_asset'],
        current_debt=results['current_debt'],
        non_current_debt=results['non_current_debt'],
        total_debt=results['total_debt'],
        total_equity=results['total_equity'],
        total_sum_equity_debt=results['total_sum_equity_debt'],
        gross_profit=results['gross_profit'],
        net_sale=results['net_sale'],
        inventory=results['inventory'],
        operational_profit=results['operational_profit'],
        proceed_profit=results['proceed_profit'],
        net_profit=results['net_profit'],
        consuming_material=results['consuming_material'],
        production_fee=results['production_fee'],
        construction_overhead=results['construction_overhead'],
        production_total_price=results['production_total_price'],
        salary_fee=results['salary_fee'],
        salary_production_fee=results['salary_production_fee'],
        usability=results['usability'],
        efficiency=results['efficiency'],
        roa=results['roa'],
        roab=results['roab'],
        roe=results['roe'],
        gross_profit_margin=results['gross_profit_margin'],
        profit_margin_ratio=results['profit_margin_ratio'],
        debt_ratio=results['debt_ratio'],
        capital_ratio=results['capital_ratio'],
        proprietary_ratio=results['proprietary_ratio'],
        equity_per_total_debt_ratio=results['equity_per_total_debt_ratio'],
        equity_per_total_non_current_asset_ratio=results[
            'equity_per_total_non_current_asset_ratio'],
        current_ratio=results['current_ratio'],
        instant_ratio=results['instant_ratio'],
        stock_turnover=results['stock_turnover'],
        altman_bankrupsy_ratio=results['altman_bankrupsy_ratio'],
    )

    # task = perform_calculations(
    #     financial_asset_ids=financial_asset_ids, company_id=instance.company.id)
    # print(task['data'])
