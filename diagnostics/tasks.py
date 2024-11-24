from celery import shared_task
import numpy as np
from company.models import CompanyProfile
from diagnostics.models import FinancialData, FinancialAsset
from .utils import get_life_cycle, FinancialCalculations


@shared_task
def perform_calculations(financial_asset_ids, company_id):

    financial_assets = FinancialAsset.objects.filter(
        id__in=financial_asset_ids).order_by('year', 'month')
    financial_calculator = FinancialCalculations(financial_assets)
    financial_calculator.process_assets()
    results = financial_calculator.get_results()['data']
    data = []
    for idx, asset in enumerate(financial_assets):
        data = [
            FinancialData(
                financial_asset=asset,
                current_asset=results['current_asset'][idx],
                non_current_asset=results['non_current_asset'][idx],
                total_asset=results['total_asset'][idx],
                current_debt=results['current_debt'][idx],
                non_current_debt=results['non_current_debt'][idx],
                total_debt=results['total_debt'][idx],
                total_equity=results['total_equity'][idx],
                total_sum_equity_debt=results['total_sum_equity_debt'][idx],
                gross_profit=results['gross_profit'][idx],
                net_sale=results['net_sale'][idx],
                inventory=results['inventory'][idx],
                operational_profit=results['operational_profit'][idx],
                proceed_profit=results['proceed_profit'][idx],
                net_profit=results['net_profit'][idx],
                consuming_material=results['consuming_material'][idx],
                production_fee=results['production_fee'][idx],
                construction_overhead=results['construction_overhead'][idx],
                production_total_price=results['production_total_price'][idx],
                salary_fee=results['salary_fee'][idx],
                salary_production_fee=results['salary_production_fee'][idx],
                usability=results['usability'][idx],
                efficiency=results['efficiency'][idx],
                roa=results['roa'][idx],
                roab=results['roab'][idx],
                roe=results['roe'][idx],
                gross_profit_margin=results['gross_profit_margin'][idx],
                profit_margin_ratio=results['profit_margin_ratio'][idx],
                debt_ratio=results['debt_ratio'][idx],
                capital_ratio=results['capital_ratio'][idx],
                proprietary_ratio=results['proprietary_ratio'][idx],
                equity_per_total_debt_ratio=results['equity_per_total_debt_ratio'][idx],
                equity_per_total_non_current_asset_ratio=results[
                    'equity_per_total_non_current_asset_ratio'][idx],
                current_ratio=results['current_ratio'][idx],
                instant_ratio=results['instant_ratio'][idx],
                stock_turnover=results['stock_turnover'][idx],
                altman_bankrupsy_ratio=results['altman_bankrupsy_ratio'][idx],
            )
        ]
    FinancialData.objects.bulk_create(data)
    company = CompanyProfile.objects.get(id=company_id)
    life_cycle_stage, x_positions, y_positions = get_life_cycle(company)
    results['life_cycle_stage'] = life_cycle_stage
    results['x_positions'] = x_positions
    results['y_positions'] = y_positions
    return {'data': results
            }
