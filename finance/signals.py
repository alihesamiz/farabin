from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from finance.models import AnalysisReport, FinancialAsset, FinancialData
from finance.utils_1 import FinancialCalculations
from finance.tasks import generate_analysis
# Trigger task after FinancialAsset is saved or deleted


@receiver([post_save, post_delete], sender=FinancialAsset)
def trigger_calculation_task(sender, instance, **kwargs):

    if kwargs.get('signal') == post_delete:
        FinancialData.objects.filter(financial_asset=instance).delete()

    else:
        financial_assets = FinancialAsset.objects.filter(
            company=instance.company, is_tax_record=True
        ).prefetch_related('sold_product_fees',
                           'profit_loss_statements',
                           'balance_reports',
                           'account_turnovers',).order_by('year', 'month')
        financial_calculator = FinancialCalculations(financial_assets)
        results = financial_calculator.get_results()['data']
        data = []
        for idx, asset in enumerate(financial_assets):
            current_asset = results['current_asset'][idx]
            non_current_asset = results['non_current_asset'][idx]
            total_asset = results['total_asset'][idx]
            current_debt = results['current_debt'][idx]
            non_current_debt = results['non_current_debt'][idx]
            total_debt = results['total_debt'][idx]
            total_equity = results['total_equity'][idx]
            total_sum_equity_debt = results['total_sum_equity_debt'][idx]
            gross_profit = results['gross_profit'][idx]
            net_sale = results['net_sale'][idx]
            inventory_average = results['inventory'][idx]
            trade_payable = results['trade_payable'][idx]
            advance = results['advance'][idx]
            reserves = results['reserves'][idx]
            long_term_payable = results['long_term_payable'][idx]
            employee_termination_benefit_reserve = results['employee_termination_benefit_reserve'][idx]
            operational_profit = results['operational_profit'][idx]
            proceed_profit = results['proceed_profit'][idx]
            net_profit = results['net_profit'][idx]
            consuming_material = results['consuming_material'][idx]
            production_fee = results['production_fee'][idx]
            construction_overhead = results['construction_overhead'][idx]
            production_total_price = results['production_total_price'][idx]
            equity_per_total_debt_ratio = results['equity_per_total_debt_ratio'][idx]
            equity_per_total_non_current_asset_ratio = results[
                'equity_per_total_non_current_asset_ratio'][idx]
            salary_fee = results['salary_fee'][idx]
            salary_production_fee = results['salary_production_fee'][idx]
            usability = results['usability'][idx]
            efficiency = results['efficiency'][idx]
            operational_income_expense = results['operational_income_expense'][idx]
            marketing_fee = results['marketing_fee'][idx]
            roa = results['roa'][idx]
            roab = results['roab'][idx]
            roe = results['roe'][idx]
            gross_profit_margin = results['gross_profit_margin'][idx]
            profit_margin_ratio = results['profit_margin_ratio'][idx]
            debt_ratio = results['debt_ratio'][idx]
            capital_ratio = results['capital_ratio'][idx]
            proprietary_ratio = results['proprietary_ratio'][idx]
            current_ratio = results['current_ratio'][idx]
            instant_ratio = results['instant_ratio'][idx]
            stock_turnover = results['stock_turnover'][idx]
            altman_bankrupsy_ratio = results['altman_bankrupsy_ratio'][idx]

            financial_data, created = FinancialData.objects.update_or_create(
                financial_asset=asset,
                defaults={
                    'is_published': False,
                    'current_asset': current_asset,
                    'non_current_asset': non_current_asset,
                    'total_asset': total_asset,
                    'current_debt': current_debt,
                    'non_current_debt': non_current_debt,
                    'total_debt': total_debt,
                    'total_equity': total_equity,
                    'total_sum_equity_debt': total_sum_equity_debt,
                    'gross_profit': gross_profit,
                    'net_sale': net_sale,
                    'trade_payable': trade_payable,
                    'advance': advance,
                    'reserves': reserves,
                    'long_term_payable': long_term_payable,
                    'employee_termination_benefit_reserve': employee_termination_benefit_reserve,
                    'inventory_average': inventory_average,
                    'operational_profit': operational_profit,
                    'proceed_profit': proceed_profit,
                    'net_profit': net_profit,
                    'consuming_material': consuming_material,
                    'production_fee': production_fee,
                    'construction_overhead': construction_overhead,
                    'production_total_price': production_total_price,
                    'salary_fee': salary_fee,
                    'salary_production_fee': salary_production_fee,
                    'usability': usability,
                    'efficiency': efficiency,
                    'roa': roa,
                    'roab': roab,
                    'roe': roe,
                    'operational_income_expense': operational_income_expense,
                    'marketing_fee': marketing_fee,
                    'gross_profit_margin': gross_profit_margin,
                    'profit_margin_ratio': profit_margin_ratio,
                    'debt_ratio': debt_ratio,
                    'capital_ratio': capital_ratio,
                    'proprietary_ratio': proprietary_ratio,
                    'equity_per_total_debt_ratio': equity_per_total_debt_ratio,
                    'equity_per_total_non_current_asset_ratio': equity_per_total_non_current_asset_ratio,
                    'current_ratio': current_ratio,
                    'instant_ratio': instant_ratio,
                    'stock_turnover': stock_turnover,
                    'altman_bankrupsy_ratio': altman_bankrupsy_ratio,
                }
            )

        print("Update/Creation complete.")


@receiver(post_save, sender=FinancialData)
def populating_reports(sender, instance, **kwargs):
    company = instance.financial_asset.company.id
    if instance.is_published:
        i = 0
        for chart_name, _ in AnalysisReport.CHART_CHOICES:
            if chart_name != "life_cycle":
                # for chart_name in AnalysisReport.CHART_CHOICES:
                # i += 1
                # if i != 10:
                print(chart_name)
                generate_analysis.delay(company, chart_name)
                # else:
                #     i=0
                #     time.sleep(60)


@receiver(post_save, sender=FinancialData)
@receiver(post_delete, sender=FinancialData)
def clear_chart_yearly_cache(sender, instance, **kwargs):
    company = instance.financial_asset.company.id
    chart_types = ['debt', 'asset', 'sale', 'equity', 'bankrupsy', 'profitability',
                   'inventory', 'agility', 'liquidity', 'leverage', 'cost', 'profit', 'salary']
    for chart in chart_types:
        cache_key = f"finance_analysis_chart_yearly_{chart}_{company}"
        cache.delete(cache_key)


@receiver(post_save, sender=FinancialData)
@receiver(post_delete, sender=FinancialData)
def clear_chart_monthly_cache(sender, instance, **kwargs):
    company = instance.financial_asset.company.id
    chart_types = ['debt', 'asset', 'sale', 'equity', 'bankrupsy', 'profitability',
                   'inventory', 'agility', 'liquidity', 'leverage', 'cost', 'profit', 'salary']
    for chart in chart_types:
        cache_key = f"finance_analysis_chart_monthly_{chart}_{company}"
        cache.delete(cache_key)
