import numpy as np
from diagnostics.models import FinancialAsset
from celery import shared_task


@shared_task
def perform_calculations(financial_asset_ids):

    financial_assets = FinancialAsset.objects.filter(
        id__in=financial_asset_ids).order_by('year')

    year = []
    current_asset = []
    non_current_asset = []
    total_asset = []
    current_debt = []
    non_current_debt = []
    total_debt = []
    ownership_right_total = []
    total_sum_equity_debt = []
    gross_profit = []
    net_sale = []
    inventory = []
    operational_profit = []
    proceed_profit = []
    net_profit = []
    consuming_material = []
    production_fee = []
    construction_overhead = []
    production_total_price = []
    salary_fee = []
    sold_product_total_fee = []
    salary_production_fee = []
    usability = []
    efficiency = []
    roa = []
    roab = []
    roe = []
    gross_profit_margin = []
    profit_margin_ratio = []
    debt_ratio = []
    capital_ratio = []
    proprietary_ratio = []
    equity_per_total_debt_ratio = []
    equity_per_total_non_current_asset_ratio = []
    current_ratio = []
    instant_ratio = []
    cash_ratio = []
    stock_turnover = []
    altman_bankrupsy_ratio = []
    accumulated_profit = []
    capital_to_asset_ratio = []
    accumulated_profit_to_asset_ratio = []
    before_tax_profit_to_asset_ratio = []
    equity_to_debt_ratio = []
    sale_to_asset_ratio = []

    for financial_asset in financial_assets:
        # Access related data through the financial_asset instance
        sold_product_fee = financial_asset.sold_product_fees.first()
        profit_loss_statement = financial_asset.profit_loss_statements.first()
        balance_report = financial_asset.balance_reports.first()
        account_turnover = financial_asset.account_turnovers.first()

        if balance_report:
            year.append(int(financial_asset.year))
            current_asset_value = int(balance_report.total_current_asset)
            non_current_asset_value = int(
                balance_report.total_non_current_asset)
            total_asset_value = current_asset_value + non_current_asset_value

            current_debt_value = int(balance_report.total_current_debt)
            non_current_debt_value = int(balance_report.total_non_current_debt)
            total_debt_value = current_debt_value + non_current_debt_value
            ownership_right_total_value = int(
                balance_report.ownership_right_total)

            total_sum_equity_debt_value = total_debt_value + ownership_right_total_value

            # Append calculated values to lists
            current_asset.append(current_asset_value)
            non_current_asset.append(non_current_asset_value)
            total_asset.append(total_asset_value)
            current_debt.append(current_debt_value)
            non_current_debt.append(non_current_debt_value)
            ownership_right_total.append(ownership_right_total_value)
            total_sum_equity_debt.append(total_sum_equity_debt_value)

            inventory_value = balance_report.inventory
            net_sale_value = balance_report.net_sale

            # Append only if they are valid (non-null)
            if inventory_value is not None:
                inventory.append(int(inventory_value))
            if net_sale_value is not None:
                net_sale.append(int(net_sale_value))

        if profit_loss_statement:
            operational_profit_value = profit_loss_statement.operational_profit
            gross_profit_value = profit_loss_statement.gross_profit
            salary_fee_value = profit_loss_statement.salary_fee
            profit_after_tax_value = profit_loss_statement.profit_after_tax
            proceed_profit_value = profit_loss_statement.proceed_profit

            operational_income_value = profit_loss_statement.operational_income
            net_profit_value = (
                int(balance_report.net_profit) if balance_report and balance_report.net_profit != 0
                else int(profit_after_tax_value)
            )

            # Append calculated values to lists
            operational_profit.append(int(operational_profit_value))
            net_profit.append(net_profit_value)
            proceed_profit.append(int(proceed_profit_value))
            salary_fee.append(int(salary_fee_value))
            gross_profit.append(int(gross_profit_value))

            # Avoid division by zero in margin calculations
            if operational_income_value and int(operational_income_value) != 0:
                gross_profit_margin.append(
                    gross_profit_value / int(operational_income_value))
                if balance_report and balance_report.net_profit:
                    profit_margin_ratio.append(
                        net_profit_value / int(operational_income_value))
            else:
                gross_profit_margin.append(0)
                profit_margin_ratio.append(0)
        if sold_product_fee:
            sold_product_total_fee_value = sold_product_fee.sold_product_total_price
            consuming_material_value = sold_product_fee.consuming_material
            production_fee_value = sold_product_fee.production_fee
            construction_overhead_value = sold_product_fee.construction_overhead
            production_total_price_value = sold_product_fee.production_total_price

            salary_production_fee_value = (
                int(profit_loss_statement.salary_fee + production_fee_value)
                if profit_loss_statement and production_fee_value else 0
            )

            # Append calculated values to lists
            sold_product_total_fee.append(int(sold_product_total_fee_value))
            consuming_material.append(int(consuming_material_value))
            production_fee.append(int(production_fee_value))
            construction_overhead.append(int(construction_overhead_value))
            production_total_price.append(int(production_total_price_value))
            salary_production_fee.append(salary_production_fee_value)

        if account_turnover:
            accumulated_profit_value = account_turnover.end_year_accumulated_profit
            if accumulated_profit_value is not None:
                accumulated_profit.append(int(accumulated_profit_value))
    for i in range(len(financial_assets)):
        if total_debt[i] != 0:
            equity_per_total_debt_ratio.append(
                ownership_right_total[i]/total_debt[i]
            )
        equity_per_total_debt_ratio.append(0)
        if non_current_asset[i] != 0:
            equity_per_total_non_current_asset_ratio.append(
                ownership_right_total[i]/non_current_asset[i]
            )
        equity_per_total_non_current_asset_ratio.append(0)

    # Usability and Efficiency Calculations
    for i in range(len(financial_assets)):
        # Ensure no division by zero
        if net_sale[i] != 0:
            usability.append(net_profit[i] / net_sale[i])
        else:
            usability.append(0)

        if total_asset[i] != 0:
            efficiency.append(net_sale[i] / total_asset[i])
        else:
            efficiency.append(0)

    # ROA and ROE Calculations
    total_asset_mean = sum(total_asset) / \
        len(total_asset) if total_asset else 0
    for i in range(len(financial_assets)):
        roa.append(
            net_profit[i] / total_asset_mean if total_asset_mean != 0 else 0)
        roab.append(usability[i] * efficiency[i])
        roe.append(net_profit[i] / ownership_right_total[i]
                   if ownership_right_total[i] != 0 else 0)

    # Debt and Capital Ratios
    for i in range(len(financial_assets)):
        debt_ratio.append(
            total_debt[i] / total_asset[i] if total_asset[i] != 0 else 0)
        capital_ratio.append(
            net_profit[i] / ownership_right_total[i] if ownership_right_total[i] != 0 else 0)

    # Proprietary ratio
    for i in range(len(financial_assets)):
        if len(proceed_profit) > 0:
            if proceed_profit[i] != 0:
                proprietary_ratio.append(total_asset[i]/proceed_profit[i])
            else:
                proprietary_ratio.append(0)

    # equity_per (total_debt_ratio , non_current_asset_ratio)
    for i in range(len(financial_assets)):
        if total_debt[i] != 0:
            equity_per_total_debt_ratio.append(
                ownership_right_total[i]/total_debt[i]
            )
        equity_per_total_debt_ratio.append(0)
        if non_current_asset[i] != 0:
            equity_per_total_non_current_asset_ratio.append(
                ownership_right_total[i]/non_current_asset[i]
            )
        equity_per_total_non_current_asset_ratio.append(0)

    # current ratio, instant ratio

    for i in range(len(financial_assets)):
        if current_debt[i] != 0:
            current_ratio.append(current_asset[i]/current_debt[i])
        else:
            current_ratio.append(0)
        if current_debt[i] != 0:
            instant_ratio.append(
                (current_asset[i]-inventory[i])/current_debt[i]
            )
        else:
            instant_ratio.append(0)

    # missing cash ratio
    # missing ROI

    # stock turnover
    for i in range(len(financial_assets)):
        if np.mean(inventory) != 0:
            stock_turnover.append(
                float(sold_product_total_fee[i]/np.mean(inventory)))
        else:
            stock_turnover.append(0)

    for i in range(len(financial_assets)):
        a = current_asset[i]-current_debt[i]
        if total_asset[i] != 0:
            capital_to_asset_ratio.append(a/total_asset[i])

            accumulated_profit_to_asset_ratio.append(
                accumulated_profit[i]/total_asset[i])

            before_tax_profit_to_asset_ratio.append(
                proceed_profit[i]/total_asset[i])

            equity_to_debt_ratio.append(
                ownership_right_total[i]/total_debt[i] if total_debt[i] != 0 else 0)
            # if total_debt[i] != 0:
            #     equity_to_debt_ratio.append(
            #         ownership_right_total[i]/total_debt[i])
            # else:
            #     equity_to_debt_ratio.append(0)

            sale_to_asset_ratio.append(net_sale[i]/total_asset[i])

            altman_bankrupsy_ratio.append(
                1.2 * (capital_to_asset_ratio[i]) +
                1.4 * (accumulated_profit_to_asset_ratio[i]) +
                3.3 * (before_tax_profit_to_asset_ratio[i]) +
                .6 * (equity_per_total_debt_ratio[i]) +
                sale_to_asset_ratio[i]
            )
        else:
            capital_to_asset_ratio.append(0)

            accumulated_profit_to_asset_ratio.append(
                0)

            before_tax_profit_to_asset_ratio.append(
                0)

            if total_debt[i] != 0:
                equity_to_debt_ratio.append(
                    ownership_right_total[i]/total_debt[i])
            else:
                equity_to_debt_ratio.append(0)

            sale_to_asset_ratio.append(0)

            altman_bankrupsy_ratio.append(
                1.2 * (capital_to_asset_ratio[i]) +
                1.4 * (accumulated_profit_to_asset_ratio[i]) +
                3.3 * (before_tax_profit_to_asset_ratio[i]) +
                .6 * (equity_per_total_debt_ratio[i]) +
                sale_to_asset_ratio[i])

    return {
        'year': year,
        'current_asset': current_asset,
        'non_current_asset': non_current_asset,
        'total_asset': total_asset,
        'current_debt': current_debt,
        'non_current_debt': non_current_debt,
        'total_debt': total_debt,
        'total_equity': ownership_right_total,
        'total_sum_equity_debt': total_sum_equity_debt,
        'gross_profit': gross_profit,
        'net_sale': net_sale,
        'inventory': inventory,
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
