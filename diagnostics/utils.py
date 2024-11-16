import numpy as np
from django.utils.translation import gettext_lazy as _
from math import log2


def get_life_cycle(company):
    # Initialize x_vals and y_vals for graphical representation
    x_vals = [_("Start"), _("Introduction"), _("Growth"), _("Maturity"),
              _("Recession 1"), _("Recession 2"), _("Recession 3"),
              _("Decline 1"), _("Decline 2")]
    x_vals_numerical = [1, 1.5, 2, 2.5, 4, 4.5, 4, 3, 2]
    y_vals = [log2(x) for x in x_vals_numerical]

    # Get the life cycles associated with the company
    life_cycle = company.capital_providing_method.all()
    life_cycles_data = [str(lc) for lc in life_cycle]

    # Define mappings for capital_providing combinations
    cycle_mappings = {
        ('Operational', 'Finance'): 7,
        ('Operational', 'Invest'): 6,
        ('Finance', 'Invest'): 2,
        ('Operational',): 8,
        ('Finance',): 1,
        ('Invest',): 3
    }

    # Sort and tuple the life cycle values for lookup
    sorted_cycles = tuple(sorted(life_cycles_data))
    life_cycle_stage = cycle_mappings.get(
        sorted_cycles, 5) if len(sorted_cycles) <= 2 else 5

    return life_cycle_stage, x_vals, y_vals


class FinancialCalculations:
    def __init__(self, financial_asset):
        self.financial_asset = financial_asset
        # self.length = len(self.financial_assets)
        self.year = 0
        self.month = 0
        self.current_asset = 0
        self.non_current_asset = 0
        self.total_asset = 0
        self.total_debt = 0
        self.current_debt = 0
        self.non_current_debt = 0
        self.ownership_right_total = 0
        self.total_sum_equity_debt = 0
        self.inventory = 0
        self.net_sale = 0
        self.operational_profit = 0
        self.net_profit = 0
        self.proceed_profit = 0
        self.salary_fee = 0
        self.gross_profit = 0
        self.gross_profit_margin = 0
        self.profit_margin_ratio = 0
        self.sold_product_total_fee = 0
        self.consuming_material = 0
        self.production_fee = 0
        self.construction_overhead = 0
        self.production_total_price = 0
        self.salary_production_fee = 0
        self.accumulated_profit = 0
        self.equity_per_total_debt_ratio = 0
        self.equity_per_total_non_current_asset_ratio = 0
        self.usability = 0
        self.efficiency = 0
        self.roa = 0
        self.roab = 0
        self.roe = 0
        self.debt_ratio = 0
        self.capital_ratio = 0
        self.proprietary_ratio = 0
        self.current_ratio = 0
        self.instant_ratio = 0
        self.stock_turnover = 0
        self.capital_to_asset_ratio = 0
        self.accumulated_profit_to_asset_ratio = 0
        self.before_tax_profit_to_asset_ratio = 0
        self.equity_to_debt_ratio = 0
        self.sale_to_asset_ratio = 0
        self.altman_bankrupsy_ratio = 0

    def process_assets(self):
        # for financial_asset in self.financial_assets:
        sold_product_fee = self.financial_asset.sold_product_fees.first()
        profit_loss_statement = self.financial_asset.profit_loss_statements.first()
        balance_report = self.financial_asset.balance_reports.first()
        account_turnover = self.financial_asset.account_turnovers.first()

        if balance_report:
            self._process_balance_report(self.financial_asset, balance_report)

        if profit_loss_statement:
            self._process_profit_loss_statement(
                profit_loss_statement, balance_report)

        if sold_product_fee:
            self._process_sold_product_fee(
                sold_product_fee, profit_loss_statement)

        if account_turnover:
            self._process_account_turnover(account_turnover)

        self._calculate_ratios()
        return self

    def _process_balance_report(self, financial_asset, balance_report):

        current_asset_value = int(balance_report.total_current_asset)
        non_current_asset_value = int(balance_report.total_non_current_asset)
        total_asset_value = current_asset_value + non_current_asset_value

        current_debt_value = int(balance_report.total_current_debt)
        non_current_debt_value = int(balance_report.total_non_current_debt)
        total_debt_value = current_debt_value + non_current_debt_value
        ownership_right_total_value = int(balance_report.ownership_right_total)

        self.current_asset = (current_asset_value)
        self.non_current_asset = (non_current_asset_value)
        self.total_asset = (total_asset_value)
        self.total_debt = (total_debt_value)
        self.current_debt = (current_debt_value)
        self.non_current_debt = (non_current_debt_value)
        self.ownership_right_total = (ownership_right_total_value)
        self.total_sum_equity_debt = (
            total_debt_value + ownership_right_total_value)

        inventory_value = balance_report.inventory
        net_sale_value = balance_report.net_sale

        if inventory_value is not None:
            self.inventory = (int(inventory_value))
        if net_sale_value is not None:
            self.net_sale = (int(net_sale_value))

        return self

    def _process_profit_loss_statement(self, profit_loss_statement, balance_report):
        operational_profit_value = profit_loss_statement.operational_profit
        gross_profit_value = profit_loss_statement.gross_profit
        salary_fee_value = profit_loss_statement.salary_fee
        profit_after_tax_value = profit_loss_statement.profit_after_tax
        proceed_profit_value = profit_loss_statement.proceed_profit
        operational_income_value = profit_loss_statement.operational_income
        net_profit_value = (int(balance_report.net_profit)
                            if balance_report and balance_report.net_profit != 0
                            else int(profit_after_tax_value))

        self.operational_profit = (int(operational_profit_value))
        self.net_profit = (net_profit_value)
        self.proceed_profit = (int(proceed_profit_value))
        self.salary_fee = (int(salary_fee_value))
        self.gross_profit = (int(gross_profit_value))

        if operational_income_value and int(operational_income_value) != 0:
            self.gross_profit_margin = (
                gross_profit_value / int(operational_income_value))
            if balance_report and balance_report.net_profit:
                self.profit_margin_ratio = (
                    net_profit_value / int(operational_income_value))
        else:
            self.gross_profit_margin = (0)
            self.profit_margin_ratio = (0)
        return self

    def _process_sold_product_fee(self, sold_product_fee, profit_loss_statement):
        sold_product_total_fee_value = sold_product_fee.sold_product_total_price
        consuming_material_value = sold_product_fee.consuming_material
        production_fee_value = sold_product_fee.production_fee
        construction_overhead_value = sold_product_fee.construction_overhead
        production_total_price_value = sold_product_fee.production_total_price
        salary_production_fee_value = (int(profit_loss_statement.salary_fee + production_fee_value)
                                       if profit_loss_statement and production_fee_value else 0)

        self.sold_product_total_fee = (int(sold_product_total_fee_value))
        self.consuming_material = (int(consuming_material_value))
        self.production_fee = (int(production_fee_value))
        self.construction_overhead = (int(construction_overhead_value))
        self.production_total_price = (int(production_total_price_value))
        self.salary_production_fee = (salary_production_fee_value)
        return self

    def _process_account_turnover(self, account_turnover):
        accumulated_profit_value = account_turnover.end_year_accumulated_profit
        if accumulated_profit_value is not None:
            self.accumulated_profit = (int(accumulated_profit_value))
        else:
            self.accumulated_profit = (0)
        return self

    def _calculate_ratios(self):
        # for i in range(self.length):
        # Ensure no division by zero
        if self.net_sale != 0:
            self.usability = (self.net_profit / self.net_sale)
        else:
            self.usability = (0)

        if self.total_asset != 0:
            self.efficiency = (self.net_sale / self.total_asset)
        else:
            self.efficiency = (0)

        # ROA and ROE Calculations
        total_asset_mean = (self.total_asset) / 1
        # for i in range(self.length):
        self.roa = (
            self.net_profit / total_asset_mean if total_asset_mean != 0 else 0)
        self.roab = (self.usability * self.efficiency)
        self.roe = (self.net_profit / self.ownership_right_total
                    if self.ownership_right_total != 0 else 0)

        # Debt and Capital Ratios
        # for i in range(self.length):
        self.debt_ratio = (
            self.total_debt / self.total_asset if self.total_asset != 0 else 0)
        self.capital_ratio = (
            self.net_profit / self.ownership_right_total if self.ownership_right_total != 0 else 0)

        # Proprietary ratio
        # for i in range(self.length):
        # if len(self.proceed_profit) > 0:
        if self.proceed_profit != 0:
            self.proprietary_ratio = (
                self.total_asset / self.proceed_profit)
        else:
            self.proprietary_ratio = (0)

        # equity_per (total_debt_ratio , non_current_asset_ratio)
        # for i in range(self.length):
        if self.total_debt != 0:
            self.equity_per_total_debt_ratio = (
                self.ownership_right_total / self.total_debt
            )
        else:
            self.equity_per_total_debt_ratio = (0)
        if self.non_current_asset != 0:
            self.equity_per_total_non_current_asset_ratio = (
                self.ownership_right_total / self.non_current_asset
            )
        else:
            self.equity_per_total_non_current_asset_ratio = (0)

        # current ratio, instant ratio

        # for i in range(self.length):
        if self.current_debt != 0:
            self.current_ratio = (
                self.current_asset / self.current_debt)
        else:
            self.current_ratio = (0)
        if self.current_debt != 0:
            print(self.instant_ratio, self.current_asset,
                  self.inventory, self.current_debt)
            self.instant_ratio = (
                (self.current_asset - self.inventory)/self.current_debt
            )
        else:
            self.instant_ratio = (0)

        # missing cash ratio
        # missing ROI

        # stock turnover
        # for i in range(self.length):
        if np.mean(self.inventory) != 0:
            self.stock_turnover = (
                float(self.sold_product_total_fee / np.mean(self.inventory)))
        else:
            self.stock_turnover = (0)

        # for i in range(self.length):
        a = self.current_asset - self.current_debt
        if self.total_asset != 0:
            self.capital_to_asset_ratio = (a/self.total_asset)

            self.accumulated_profit_to_asset_ratio = (
                self.accumulated_profit / self.total_asset)

            self.before_tax_profit_to_asset_ratio = (
                self.proceed_profit / self.total_asset)

            self.equity_to_debt_ratio = (
                self.ownership_right_total / self.total_debt) if self.total_debt != 0 else 0

            self.sale_to_asset_ratio = (
                self.net_sale / self.total_asset)

        # for i in range(self.length):
        if self.total_asset != 0:
            self.capital_to_asset_ratio = (
                (self.current_asset - self.current_debt) / self.total_asset)
            self.accumulated_profit_to_asset_ratio = (
                self.accumulated_profit / self.total_asset)
            self.before_tax_profit_to_asset_ratio = (
                self.proceed_profit / self.total_asset)
            self.sale_to_asset_ratio = (
                self.net_sale / self.total_asset)

            if self.total_debt != 0:
                self.equity_to_debt_ratio = (
                    self.ownership_right_total / self.total_debt)
            else:
                self.equity_to_debt_ratio = (0)
            self.altman_bankrupsy_ratio = (
                1.2 * self.capital_to_asset_ratio +
                1.4 * self.accumulated_profit_to_asset_ratio +
                3.3 * self.before_tax_profit_to_asset_ratio +
                0.6 * (self.equity_per_total_debt_ratio) +
                self.sale_to_asset_ratio
            )
        else:
            self.capital_to_asset_ratio = (0)
            self.accumulated_profit_to_asset_ratio = (0)
            self.before_tax_profit_to_asset_ratio = (0)
            self.sale_to_asset_ratio = (0)
            self.altman_bankrupsy_ratio = (0)
        return self

    def get_results(self):
        return {
            'status': 'success',
            'data': {
                'current_asset': self.current_asset,
                'non_current_asset': self.non_current_asset,
                'total_asset': self.total_asset,
                'current_debt': self.current_debt,
                'non_current_debt': self.non_current_debt,
                'total_debt': self.total_debt,
                'total_equity': self.ownership_right_total,
                'total_sum_equity_debt': self.total_sum_equity_debt,
                'gross_profit': self.gross_profit,
                'net_sale': self.net_sale,
                'inventory': self.inventory,
                'operational_profit': self.operational_profit,
                'proceed_profit': self.proceed_profit,
                'net_profit': self.net_profit,
                'consuming_material': self.consuming_material,
                'production_fee': self.production_fee,
                'construction_overhead': self.construction_overhead,
                'production_total_price': self.production_total_price,
                'salary_fee': self.salary_fee,
                'salary_production_fee': self.salary_production_fee,
                'usability': self.usability,
                'efficiency': self.efficiency,
                'roa': self.roa,
                'roab': self.roab,
                'roe': self.roe,
                'gross_profit_margin': self.gross_profit_margin,
                'profit_margin_ratio': self.profit_margin_ratio,
                'debt_ratio': self.debt_ratio,
                'capital_ratio': self.capital_ratio,
                'proprietary_ratio': self.proprietary_ratio,
                'equity_per_total_debt_ratio': self.equity_per_total_debt_ratio,
                'equity_per_total_non_current_asset_ratio': self.equity_per_total_non_current_asset_ratio,
                'current_ratio': self.current_ratio,
                'instant_ratio': self.instant_ratio,
                'stock_turnover': self.stock_turnover,
                'altman_bankrupsy_ratio': self.altman_bankrupsy_ratio,
            }
        }


# class FinancialCalculations:
#     def __init__(self, financial_assets) -> None:
#         self.financial_assets = financial_assets
#         # self.length = len(self.financial_assets)
#         self.year = []
#         self.month = []
#         self.current_asset = []
#         self.non_current_asset = []
#         self.total_asset = []
#         self.total_debt = []
#         self.current_debt = []
#         self.non_current_debt = []
#         self.ownership_right_total = []
#         self.total_sum_equity_debt = []
#         self.inventory = []
#         self.net_sale = []
#         self.operational_profit = []
#         self.net_profit = []
#         self.proceed_profit = []
#         self.salary_fee = []
#         self.gross_profit = []
#         self.gross_profit_margin = []
#         self.profit_margin_ratio = []
#         self.sold_product_total_fee = []
#         self.consuming_material = []
#         self.production_fee = []
#         self.construction_overhead = []
#         self.production_total_price = []
#         self.salary_production_fee = []
#         self.accumulated_profit = []
#         self.equity_per_total_debt_ratio = []
#         self.equity_per_total_non_current_asset_ratio = []
#         self.usability = []
#         self.efficiency = []
#         self.roa = []
#         self.roab = []
#         self.roe = []
#         self.debt_ratio = []
#         self.capital_ratio = []
#         self.proprietary_ratio = []
#         self.current_ratio = []
#         self.instant_ratio = []
#         self.stock_turnover = []
#         self.capital_to_asset_ratio = []
#         self.accumulated_profit_to_asset_ratio = []
#         self.before_tax_profit_to_asset_ratio = []
#         self.equity_to_debt_ratio = []
#         self.sale_to_asset_ratio = []
#         self.altman_bankrupsy_ratio = []

#     def process_assets(self):
#         for financial_asset in self.financial_assets:
#             sold_product_fee = financial_asset.sold_product_fees.first()
#             profit_loss_statement = financial_asset.profit_loss_statements.first()
#             balance_report = financial_asset.balance_reports.first()
#             account_turnover = financial_asset.account_turnovers.first()

#             if balance_report:
#                 self._process_balance_report(financial_asset, balance_report)

#             if profit_loss_statement:
#                 self._process_profit_loss_statement(
#                     profit_loss_statement, balance_report)

#             if sold_product_fee:
#                 self._process_sold_product_fee(
#                     sold_product_fee, profit_loss_statement)

#             if account_turnover:
#                 self._process_account_turnover(account_turnover)
#         self._calculate_ratios()

#     def _process_balance_report(self, financial_asset, balance_report):
#         self.year.append(int(financial_asset.year))
#         self.month.append(int(financial_asset.month)
#                           if financial_asset.month else "")
#         current_asset_value = int(balance_report.total_current_asset)
#         non_current_asset_value = int(balance_report.total_non_current_asset)
#         total_asset_value = current_asset_value + non_current_asset_value

#         current_debt_value = int(balance_report.total_current_debt)
#         non_current_debt_value = int(balance_report.total_non_current_debt)
#         total_debt_value = current_debt_value + non_current_debt_value
#         ownership_right_total_value = int(balance_report.ownership_right_total)

#         self.current_asset.append(current_asset_value)
#         self.non_current_asset.append(non_current_asset_value)
#         self.total_asset.append(total_asset_value)
#         self.total_debt.append(total_debt_value)
#         self.current_debt.append(current_debt_value)
#         self.non_current_debt.append(non_current_debt_value)
#         self.ownership_right_total.append(ownership_right_total_value)
#         self.total_sum_equity_debt.append(
#             total_debt_value + ownership_right_total_value)

#         inventory_value = balance_report.inventory
#         net_sale_value = balance_report.net_sale

#         if inventory_value is not None:
#             self.inventory.append(int(inventory_value))
#         if net_sale_value is not None:
#             self.net_sale.append(int(net_sale_value))

#     def _process_profit_loss_statement(self, profit_loss_statement, balance_report):
#         operational_profit_value = profit_loss_statement.operational_profit
#         gross_profit_value = profit_loss_statement.gross_profit
#         salary_fee_value = profit_loss_statement.salary_fee
#         profit_after_tax_value = profit_loss_statement.profit_after_tax
#         proceed_profit_value = profit_loss_statement.proceed_profit
#         operational_income_value = profit_loss_statement.operational_income
#         net_profit_value = (int(balance_report.net_profit)
#                             if balance_report and balance_report.net_profit != 0
#                             else int(profit_after_tax_value))

#         self.operational_profit.append(int(operational_profit_value))
#         self.net_profit.append(net_profit_value)
#         self.proceed_profit.append(int(proceed_profit_value))
#         self.salary_fee.append(int(salary_fee_value))
#         self.gross_profit.append(int(gross_profit_value))

#         if operational_income_value and int(operational_income_value) != 0:
#             self.gross_profit_margin.append(
#                 gross_profit_value / int(operational_income_value))
#             if balance_report and balance_report.net_profit:
#                 self.profit_margin_ratio.append(
#                     net_profit_value / int(operational_income_value))
#         else:
#             self.gross_profit_margin.append(0)
#             self.profit_margin_ratio.append(0)

#     def _process_sold_product_fee(self, sold_product_fee, profit_loss_statement):
#         sold_product_total_fee_value = sold_product_fee.sold_product_total_price
#         consuming_material_value = sold_product_fee.consuming_material
#         production_fee_value = sold_product_fee.production_fee
#         construction_overhead_value = sold_product_fee.construction_overhead
#         production_total_price_value = sold_product_fee.production_total_price
#         salary_production_fee_value = (int(profit_loss_statement.salary_fee + production_fee_value)
#                                        if profit_loss_statement and production_fee_value else 0)

#         self.sold_product_total_fee.append(int(sold_product_total_fee_value))
#         self.consuming_material.append(int(consuming_material_value))
#         self.production_fee.append(int(production_fee_value))
#         self.construction_overhead.append(int(construction_overhead_value))
#         self.production_total_price.append(int(production_total_price_value))
#         self.salary_production_fee.append(salary_production_fee_value)

#     def _process_account_turnover(self, account_turnover):
#         accumulated_profit_value = account_turnover.end_year_accumulated_profit
#         if accumulated_profit_value is not None:
#             self.accumulated_profit.append(int(accumulated_profit_value))
#         else:
#             self.accumulated_profit.append(0)

#     def _calculate_ratios(self):
#         # for i in range(self.length):
#             # Ensure no division by zero
#         if self.net_sale[i] != 0:
#             self.usability.append(self.net_profit[i] / self.net_sale[i])
#         else:
#             self.usability.append(0)

#         if self.total_asset[i] != 0:
#             self.efficiency.append(self.net_sale[i] / self.total_asset[i])
#         else:
#             self.efficiency.append(0)

#         # ROA and ROE Calculations
#         total_asset_mean = sum(self.total_asset) / \
#             len(self.total_asset) if self.total_asset else 0
#         # for i in range(self.length):
#         self.roa.append(
#             self.net_profit[i] / total_asset_mean if total_asset_mean != 0 else 0)
#         self.roab.append(self.usability[i] * self.efficiency[i])
#         self.roe.append(self.net_profit[i] / self.ownership_right_total[i]
#                         if self.ownership_right_total[i] != 0 else 0)

#             # Debt and Capital Ratios
#         # for i in range(self.length):
#         self.debt_ratio.append(
#             self.total_debt[i] / self.total_asset[i] if self.total_asset[i] != 0 else 0)
#         self.capital_ratio.append(
#             self.net_profit[i] / self.ownership_right_total[i] if self.ownership_right_total[i] != 0 else 0)

#         # Proprietary ratio
#         # for i in range(self.length):
#         if len(self.proceed_profit) > 0:
#             if self.proceed_profit[i] != 0:
#                 self.proprietary_ratio.append(
#                     self.total_asset[i]/self.proceed_profit[i])
#             else:
#                 self.proprietary_ratio.append(0)

#         # equity_per (total_debt_ratio , non_current_asset_ratio)
#         # for i in range(self.length):
#         if self.total_debt[i] != 0:
#             self.equity_per_total_debt_ratio.append(
#                 self.ownership_right_total[i]/self.total_debt[i]
#             )
#         else:
#             self.equity_per_total_debt_ratio.append(0)
#         if self.non_current_asset[i] != 0:
#             self.equity_per_total_non_current_asset_ratio.append(
#                 self.ownership_right_total[i]/self.non_current_asset[i]
#             )
#         else:
#             self.equity_per_total_non_current_asset_ratio.append(0)

#         # current ratio, instant ratio

#         # for i in range(self.length):
#         if self.current_debt[i] != 0:
#             self.current_ratio.append(
#                 self.current_asset[i]/self.current_debt[i])
#         else:
#             self.current_ratio.append(0)
#         if self.current_debt[i] != 0:
#             self.instant_ratio.append(
#                 (self.current_asset[i] -
#                     self.inventory[i])/self.current_debt[i]
#             )
#         else:
#             self.instant_ratio.append(0)

#         # missing cash ratio
#         # missing ROI

#         # stock turnover
#         # for i in range(self.length):
#         if np.mean(self.inventory) != 0:
#             self.stock_turnover.append(
#                 float(self.sold_product_total_fee[i]/np.mean(self.inventory)))
#         else:
#             self.stock_turnover.append(0)

#         # for i in range(self.length):
#         a = self.current_asset[i]-self.current_debt[i]
#         if self.total_asset[i] != 0:
#             self.capital_to_asset_ratio.append(a/self.total_asset[i])

#             self.accumulated_profit_to_asset_ratio.append(
#                 self.accumulated_profit[i]/self.total_asset[i])

#             self.before_tax_profit_to_asset_ratio.append(
#                 self.proceed_profit[i]/self.total_asset[i])

#             self.equity_to_debt_ratio.append(
#                 self.ownership_right_total[i]/self.total_debt[i]) if self.total_debt[i] != 0 else 0

#             self.sale_to_asset_ratio.append(
#                 self.net_sale[i]/self.total_asset[i])

#         # for i in range(self.length):
#         if self.total_asset[i] != 0:
#             self.capital_to_asset_ratio.append(
#                 (self.current_asset[i] - self.current_debt[i]) / self.total_asset[i])
#             self.accumulated_profit_to_asset_ratio.append(
#                 self.accumulated_profit[i] / self.total_asset[i])
#             self.before_tax_profit_to_asset_ratio.append(
#                 self.proceed_profit[i] / self.total_asset[i])
#             self.sale_to_asset_ratio.append(
#                 self.net_sale[i] / self.total_asset[i])

#             if self.total_debt[i] != 0:
#                 self.equity_to_debt_ratio.append(
#                     self.ownership_right_total[i] / self.total_debt[i])
#             else:
#                 self.equity_to_debt_ratio.append(0)
#             self.altman_bankrupsy_ratio.append(
#                 1.2 * self.capital_to_asset_ratio[i] +
#                 1.4 * self.accumulated_profit_to_asset_ratio[i] +
#                 3.3 * self.before_tax_profit_to_asset_ratio[i] +
#                 0.6 * (self.equity_per_total_debt_ratio[i] if i < len(self.equity_per_total_debt_ratio) else 0) +
#                 self.sale_to_asset_ratio[i]
#             )
#         else:
#             self.capital_to_asset_ratio.append(0)
#             self.accumulated_profit_to_asset_ratio.append(0)
#             self.before_tax_profit_to_asset_ratio.append(0)
#             self.sale_to_asset_ratio.append(0)
#             self.altman_bankrupsy_ratio.append(0)

#     def get_results(self):
#         return {
#             'status': 'success',
#             'data': {
#                 'year': self.year,
#                 'month': self.month,
#                 'current_asset': self.current_asset,
#                 'non_current_asset': self.non_current_asset,
#                 'total_asset': self.total_asset,
#                 'current_debt': self.current_debt,
#                 'non_current_debt': self.non_current_debt,
#                 'total_debt': self.total_debt,
#                 'total_equity': self.ownership_right_total,
#                 'total_sum_equity_debt': self.total_sum_equity_debt,
#                 'gross_profit': self.gross_profit,
#                 'net_sale': self.net_sale,
#                 'inventory': self.inventory,
#                 'operational_profit': self.operational_profit,
#                 'proceed_profit': self.proceed_profit,
#                 'net_profit': self.net_profit,
#                 'consuming_material': self.consuming_material,
#                 'production_fee': self.production_fee,
#                 'construction_overhead': self.construction_overhead,
#                 'production_total_price': self.production_total_price,
#                 'salary_fee': self.salary_fee,
#                 'salary_production_fee': self.salary_production_fee,
#                 'usability': self.usability,
#                 'efficiency': self.efficiency,
#                 'roa': self.roa,
#                 'roab': self.roab,
#                 'roe': self.roe,
#                 'gross_profit_margin': self.gross_profit_margin,
#                 'profit_margin_ratio': self.profit_margin_ratio,
#                 'debt_ratio': self.debt_ratio,
#                 'capital_ratio': self.capital_ratio,
#                 'proprietary_ratio': self.proprietary_ratio,
#                 'equity_per_total_debt_ratio': self.equity_per_total_debt_ratio,
#                 'equity_per_total_non_current_asset_ratio': self.equity_per_total_non_current_asset_ratio,
#                 'current_ratio': self.current_ratio,
#                 'instant_ratio': self.instant_ratio,
#                 'stock_turnover': self.stock_turnover,
#                 'altman_bankrupsy_ratio': self.altman_bankrupsy_ratio,
#             }
#         }
