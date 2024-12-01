import decimal
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
    def __init__(self, financial_assets):
        self.financial_assets = financial_assets
        self.length = len(self.financial_assets)
        # non-calculations
        self.year = []
        self.month = []
        self.current_asset = []
        self.non_current_asset = []
        self.total_asset = []
        self.total_debt = []
        self.current_debt = []
        self.non_current_debt = []
        self.ownership_right_total = []
        self.inventory = []
        self.net_sale = []
        self.operational_profit = []
        self.net_profit = []
        self.proceed_profit = []
        self.salary_fee = []
        self.gross_profit = []
        self.construction_overhead = []
        self.consuming_material = []
        self.production_total_price = []
        self.direct_wage = []
        self.accumulated_profit = []
        self.total_equity = []

        self.gross_profit_margin_ratio = []
        self.net_profit_margin_ratio = []
        self.total_sum_equity_debt = []
        self.sold_product_total_fee = []
        self.salary_production_fee = []
        self.equity_per_total_debt_ratio = []
        self.equity_per_total_non_current_asset_ratio = []
        self.usability = []
        self.efficiency = []
        self.roa = []
        self.roab = []
        self.roe = []
        self.debt_ratio = []
        self.capital_ratio = []
        self.total_debt_to_proceed_profit_ratio = []
        self.current_debt_to_proceed_profit_ratio = []
        self.proprietary_ratio = []
        self.current_ratio = []
        self.instant_ratio = []
        self.total_asset_turnover_ratio = []
        self.stock_turnover = []
        self.capital_to_asset_ratio = []
        self.accumulated_profit_to_asset_ratio = []
        self.before_tax_profit_to_asset_ratio = []
        self.equity_to_debt_ratio = []
        self.sale_to_asset_ratio = []
        self.altman_bankrupsy_ratio = []

        self.process_assets()

    def process_assets(self):
        try:
            for i in range(self.length):
                account_turnover = self.financial_assets[i].account_turnovers.first(
                )
                balance_report = self.financial_assets[i].balance_reports.first(
                )
                sold_product_fee = self.financial_assets[i].sold_product_fees.first(
                )
                profit_loss_statement = self.financial_assets[i].profit_loss_statements.first(
                )

                self.current_asset_function(balance_report)
                self.non_current_asset_function(balance_report)
                self.total_asset_function(balance_report)
                self.current_debt_function(balance_report)
                self.non_current_debt_function(balance_report)
                self.ownership_right_total_function(balance_report)
                self.inventory_function(balance_report)
                self.net_sale_function(balance_report)
                self.net_profit_function(balance_report)
                self.accumulated_profit_function(balance_report)
                self.total_equity_function(balance_report)

                self.operational_profit_function(profit_loss_statement)
                self.gross_profit_function(profit_loss_statement)
                self.proceed_profit_function(profit_loss_statement)
                self.salary_fee_function(profit_loss_statement)

                self.consuming_material_function(sold_product_fee)
                self.construction_overhead_function(sold_product_fee)
                self.production_total_price_function(sold_product_fee)
                self.direct_wage_function(sold_product_fee)
                self.sold_product_total_fee_function(sold_product_fee)

            self.usability_function()
            self.efficiency_function()
            self.roa_function()
            self.roab_function()
            self.roe_function()
            self.total_debt_function()

            self.gross_profit_margin_ratio_function()
            self.net_profit_margin_ratio_function()
            self.debt_ratio_function()
            self.capital_ratio_function()
            self.total_debt_to_proceed_profit_ratio_function()
            self.current_debt_to_proceed_profit_ratio_function()
            self.properitary_ratio_function()
            self.equity_per_total_debt_ratio_function()
            self.current_ratio_function()
            self.instant_ratio_function()
            self.total_asset_turnover_ratio_function()
            self.total_sum_equity_debt_function()
            self.stock_turn_over_ratio_function()
            self.equity_per_total_non_current_asset_ratio_function()
            self.capital_to_asset_ratio_function()
            self.accumulated_profit_to_asset_ratio_function()
            self.before_tax_profit_to_asset_ratio_function()
            self.sale_to_asset_ratio_function()
            self.equity_to_debt_ratio_function()
            self.altman_bankruptcy_ratio_function()
            self.salary_production_fee_function()

        except Exception as e:
            print(f"Error occurred while processing assets: {e}")
            return {'status': 'failed',
                    'data': {}}

    #########################
    # Assets Functions      #
    #########################
    def current_asset_function(self, balance_report):
        """
        Current Asset calculation
        """
        if balance_report:

            self.current_asset.append(balance_report.total_current_asset)
        else:
            self.current_asset.append(0)  # or some other default value

    def non_current_asset_function(self, balance_report):
        """
        Non-Current Asset Mean calculation
        """
        if balance_report:
            self.non_current_asset.append(
                balance_report.total_non_current_asset)
        else:
            self.non_current_asset.append(0)

    def total_asset_function(self, balance_report):
        """
        Total Asset calculation
        """
        if balance_report:
            self.total_asset.append(
                balance_report.total_non_current_asset + balance_report.total_current_asset)
        else:
            self.total_asset.append(0)

    #########################
    # Debt Functions        #
    #########################
    def current_debt_function(self, balance_report):
        """
        Current debt calculation
        """
        if balance_report:
            self.current_debt.append(
                balance_report.total_current_debt)
        else:
            self.current_debt.append(0)

    def non_current_debt_function(self, balance_report):
        """
        Non Current debt calculation
        """
        if balance_report:
            self.non_current_debt.append(
                balance_report.total_non_current_debt)
        else:
            self.non_current_debt.append(0)

    def total_debt_function(self):
        """
        Total debt calculation
        """
        for i in range(self.length):
            self.total_debt.append(
                self.current_debt[i] + self.non_current_debt[i]
            )

    def ownership_right_total_function(self, balance_report):
        """
        Total ownership right calculation
        """
        if balance_report:
            self.ownership_right_total.append(
                balance_report.ownership_right_total)
        else:
            self.ownership_right_total.append(0)

    def inventory_function(self, balance_report):
        """
        Inventory calculation
        """
        if balance_report:
            self.inventory.append(balance_report.inventory)
        else:
            self.inventory.append(0)

    def net_sale_function(self, balance_report):
        """
        Net Sale calculation
        """
        if balance_report:
            self.net_sale.append(balance_report.net_sale)
        else:
            self.net_sale.append(0)

    def net_profit_function(self, balance_report):
        """
        Net Profit calculation
        """
        if balance_report:
            self.net_profit.append(balance_report.net_profit)
        else:
            self.net_profit.append(0)

    def consuming_material_function(self, sold_product_fee):
        """
        Consuming Material calculation
        """
        if sold_product_fee:
            self.consuming_material.append(sold_product_fee.consuming_material)
        else:
            self.consuming_material.append(0)

    def operational_profit_function(self, profit_loss_statement):
        """
        Operational Profit calculation
        """
        if profit_loss_statement:
            self.operational_profit.append(
                profit_loss_statement.operational_profit)
        else:
            self.operational_profit.append(0)

    def gross_profit_function(self, profit_loss_statement):
        """
        Gross Profit Mean calculation
        """
        if profit_loss_statement:
            self.gross_profit.append(profit_loss_statement.gross_profit)
        else:
            self.gross_profit.append(0)

    def proceed_profit_function(self, profit_loss_statement):
        """
        Proceed Profit calculation
        """
        if profit_loss_statement:
            self.proceed_profit.append(profit_loss_statement.proceed_profit)
        else:
            self.proceed_profit.append(0)

    def salary_fee_function(self, profit_loss_statement):
        """Salary Fee calculation
        """
        if profit_loss_statement:
            self.salary_fee.append(profit_loss_statement.salary_fee)
        else:
            self.salary_fee.append(0)

    def construction_overhead_function(self, sold_product_fee):
        """
        Construction Overhead calculation
        """
        if sold_product_fee:
            self.construction_overhead.append(
                sold_product_fee.construction_overhead)
        else:
            self.construction_overhead.append(0)

    def production_total_price_function(self, sold_product_fee):
        """
        Production Total Price calculation
        """
        if sold_product_fee:
            self.production_total_price.append(
                sold_product_fee.production_total_price)
        else:
            self.production_total_price.append(0)

    def direct_wage_function(self, sold_product_fee):
        """
        Direct Wage calculation
        """
        if sold_product_fee:
            self.direct_wage.append(sold_product_fee.direct_wage)
        else:
            self.direct_wage.append(0)

    def sold_product_total_fee_function(self, sold_product_fee):
        """Sold Product Total Fee calculation"""
        if sold_product_fee:
            self.sold_product_total_fee.append(
                sold_product_fee.sold_product_total_price or 0)

    def accumulated_profit_function(self, balance_report):
        """
        Accumulated Profit/Loss calculation
        """
        if balance_report:
            self.accumulated_profit.append(
                balance_report.accumulated_profit_loss)
        else:
            self.accumulated_profit.append(0)

    def total_equity_function(self, balance_report):
        """
        Non-Current Asset Mean calculation
        """
        if balance_report:
            self.total_equity.append(
                balance_report.ownership_right_total)
        else:
            self.total_equity.append(0)

    def year_function(self):
        """Year calculation"""
        for i in range(self.length):
            self.year.append(self.financial_assets[i].year)

    def roi_function():
        """Return of Investments (ROI) calculation
        """
        pass

    def usability_function(self):
        """
        Usability calculation
        """
        for i in range(self.length):
            self.usability.append(
                self.net_profit[i]/self.net_sale[i] if self.net_sale[i] != 0 else 0)

    def efficiency_function(self):
        """
        Efficiency calculation
        """
        for i in range(self.length):
            self.efficiency.append(self.net_sale[i]/self.total_asset[i]
                                   if self.total_asset[i] != 0 else 0)

    def roa_function(self):
        """
        Return on Assets (ROA) calculation
        """
        for i in range(self.length):
            self.roa.append(
                self.net_profit[i]/self.total_asset[i] if self.total_asset[i] != 0 else 0)

    def roab_function(self):
        """
        Return on Assets (ROA) secondary
        """
        for i in range(self.length):
            self.roab.append(
                self.usability[i]*self.efficiency[i])

    def roe_function(self):
        """Return on Equity (ROE) calculation"""
        for i in range(self.length):
            self.roe.append(
                self.net_profit[i]/self.total_equity[i] if self.total_equity[i] != 0 else 0)

    def equity_per_total_non_current_asset_ratio_function(self):
        for i in range(self.length):
            self.equity_per_total_non_current_asset_ratio.append(
                self.total_equity[i]/self.non_current_asset[i]
                if self.non_current_asset[i] != 0 else 0)

    def gross_profit_margin_ratio_function(self):
        """
        Gross Profit Margin Ratio calculation
        """
        for i in range(self.length):
            self.gross_profit_margin_ratio.append(
                self.gross_profit[i]/self.net_sale[i] if self.net_sale[i] != 0 else 0)

    def net_profit_margin_ratio_function(self):
        """
        Net Profit Margin Ratio calculation
        """
        for i in range(self.length):
            self.net_profit_margin_ratio.append(
                self.net_profit[i]/self.net_sale[i] if self.net_sale[i] != 0 else 0)

    def operational_profit_margin_function(self):
        """Operational Profit Margin calculation
        """
        pass

    def total_sum_equity_debt_function(self):
        """Total Sum of Equity and Debt calculation
        """
        for i in range(self.length):
            self.total_sum_equity_debt.append(
                self.total_equity[i] + self.total_debt[i])

    def debt_ratio_function(self):
        """
        Debt Ratio calculation
        """
        for i in range(self.length):
            self.debt_ratio.append(
                self.total_debt[i]/self.total_asset[i] if self.total_asset[i] != 0 else 0)

    def salary_production_fee_function(self):
        for i in range(self.length):
            print(self.direct_wage[i] + self.salary_fee[i])
            print('asdasdasd')
            self.salary_production_fee.append(
                self.direct_wage[i] + self.salary_fee[i])

    def profit_coverage_ratio_function(self):
        """Profit Coverage Ratio calculation
        """
        pass

    def capital_ratio_function(self):
        """
        Capital Ratio calculation
        """
        for i in range(self.length):
            self.capital_ratio.append(
                self.net_profit[i]/self.total_equity[i] if self.total_equity[i] != 0 else 0)

    def fixed_asset_to_proceed_profit_ratio_function(self):
        """Fixed Asset to Proceed Profit Ratio calculation"""
        pass

    def total_debt_to_proceed_profit_ratio_function(self):
        """Total Debt to Proceed Profit Ratio calculation"""
        for i in range(self.length):
            self.total_debt_to_proceed_profit_ratio.append(
                self.total_debt[i]/self.proceed_profit[i] if self.proceed_profit[i] != 0 else 0)

    def current_debt_to_proceed_profit_ratio_function(self):
        """Current Debt to Proceed Profit Ratio calculation"""
        for i in range(self.length):
            self.current_debt_to_proceed_profit_ratio.append(
                self.current_debt[i]/self.proceed_profit[i] if self.proceed_profit[i] != 0 else 0)

    def properitary_ratio_function(self):
        """Proprietary Ratio calculation"""
        for i in range(self.length):
            self.proprietary_ratio.append(
                self.total_asset[i]/self.proceed_profit[i] if self.proceed_profit[i] != 0 else 0)

    def equity_per_total_debt_ratio_function(self):
        """Equity Per Total Debt Ratio calculation"""
        for i in range(self.length):
            self.equity_per_total_debt_ratio.append(
                self.total_equity[i]/self.total_debt[i] if self.total_debt[i] != 0 else 0)

    def equity_per_total_fixed_asset_ratio_function(self):
        """Equity Per Total Fixed Asset Ratio calculation"""
        pass

    def current_ratio_function(self):
        """Current Ratio calculation"""
        for i in range(self.length):
            self.current_ratio.append(
                self.current_asset[i]/self.current_debt[i] if self.current_debt[i] != 0 else 0)

    def instant_ratio_function(self):
        """Current Ratio calculation"""
        for i in range(self.length):
            self.instant_ratio.append(
                (self.current_asset[i]-self.inventory[i])/self.current_debt[i] if self.current_debt[i] != 0 else 0)

    def liquidity_ratio_function(self):
        """Liquidity Ratio calculation"""
        pass

    def stock_turn_over_ratio_function(self):
        """Stock Turnover Ratio calculation"""
        for i in range(self.length):
            avg_inventory = np.mean(
                self.inventory[:i+1]) if i != 0 else self.inventory[i]
            self.stock_turnover.append(
                self.sold_product_total_fee[i] / avg_inventory if avg_inventory != 0 else 0)


    def received_turn_over_ratio_function(self):
        """Received Turnover Ratio calculation"""
        pass

    def average_collection_period_function(self):
        """Average Collection Period calculation"""
        pass

    def total_asset_turnover_ratio_function(self):
        """Total Asset Turnover Ratio calculation"""
        total_asset_mean = np.mean(self.total_asset)
        for i in range(self.length):
            self.total_asset_turnover_ratio.append(
                self.net_sale[i]/total_asset_mean if total_asset_mean != 0 else 0)

    def potential_growth_ratio_function(self):
        """Growth Potential Ratio calculation"""
        pass

    def sale_growth_ratio_function(self):
        """Sale Growth Ratio calculation"""
        pass

    def net_profit_growth_ratio_function(self):
        """Net Profit Growth Ratio calculation"""
        pass

    def capital_to_asset_ratio_function(self):
        for i in range(self.length):
            self.capital_to_asset_ratio.append(
                (self.current_asset[i] - self.current_debt[i]) / self.total_asset[i] if self.total_asset[i] != 0 else 0)

    def accumulated_profit_to_asset_ratio_function(self):
        """
        Accumulated Profit to Asset Ratio calculation
        """

        for i in range(self.length):
            self.accumulated_profit_to_asset_ratio.append(
                self.accumulated_profit[i] / self.total_asset[i] if self.total_asset[i] != 0 else 0)

    def before_tax_profit_to_asset_ratio_function(self):
        """
        Before Tax Profit to Asset Ratio calculation
        """
        for i in range(self.length):
            self.before_tax_profit_to_asset_ratio.append(
                self.proceed_profit[i] / self.total_asset[i] if self.total_asset[i] != 0 else 0)

    def sale_to_asset_ratio_function(self):
        """
        Sale to Asset Ratio calculation
        """
        for i in range(self.length):
            self.sale_to_asset_ratio.append(
                self.net_sale[i] / self.total_asset[i] if self.total_asset[i] != 0 else 0)

    def equity_to_debt_ratio_function(self):
        """
        Equity to Debt Ratio calculation
        """
        for i in range(self.length):
            self.equity_to_debt_ratio.append(
                self.total_equity[i] / self.total_debt[i] if self.total_debt[i] != 0 else 0)

    def altman_bankruptcy_ratio_function(self):
        """Altman Bankruptcy Ratio calculation"""
        from decimal import Decimal
        for i in range(self.length):
            self.altman_bankrupsy_ratio.append(
                (Decimal(1.2) * self.capital_to_asset_ratio[i]) +
                (Decimal(1.4) * self.accumulated_profit_to_asset_ratio[i]) +
                (Decimal(3.3) * self.before_tax_profit_to_asset_ratio[i]) +
                (Decimal(0.6) * self.equity_per_total_debt_ratio[i]) +
                self.sale_to_asset_ratio[i]
            )

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
                'production_fee': self.direct_wage,
                'construction_overhead': self.construction_overhead,
                'production_total_price': self.production_total_price,
                'salary_fee': self.salary_fee,
                'salary_production_fee': self.salary_production_fee,
                'usability': self.usability,
                'efficiency': self.efficiency,
                'roa': self.roa,
                'roab': self.roab,
                'roe': self.roe,
                'gross_profit_margin': self.gross_profit_margin_ratio,
                'profit_margin_ratio': self.net_profit_margin_ratio,
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


# import numpy as np
# from django.utils.translation import gettext_lazy as _
# from math import log2


# def get_life_cycle(company):
#     # Initialize x_vals and y_vals for graphical representation
#     x_vals = [_("Start"), _("Introduction"), _("Growth"), _("Maturity"),
#               _("Recession 1"), _("Recession 2"), _("Recession 3"),
#               _("Decline 1"), _("Decline 2")]
#     x_vals_numerical = [1, 1.5, 2, 2.5, 4, 4.5, 4, 3, 2]
#     y_vals = [log2(x) for x in x_vals_numerical]

#     # Get the life cycles associated with the company
#     life_cycle = company.capital_providing_method.all()
#     life_cycles_data = [str(lc) for lc in life_cycle]

#     # Define mappings for capital_providing combinations
#     cycle_mappings = {
#         ('Operational', 'Finance'): 7,
#         ('Operational', 'Invest'): 6,
#         ('Finance', 'Invest'): 2,
#         ('Operational',): 8,
#         ('Finance',): 1,
#         ('Invest',): 3
#     }

#     # Sort and tuple the life cycle values for lookup
#     sorted_cycles = tuple(sorted(life_cycles_data))
#     life_cycle_stage = cycle_mappings.get(
#         sorted_cycles, 5) if len(sorted_cycles) <= 2 else 5

#     return life_cycle_stage, x_vals, y_vals

# class FinancialCalculations:
    def __init__(self, financial_assets) -> None:
        self.financial_assets = financial_assets
        self.length = len(self.financial_assets)
        self.year = []
        self.month = []
        self.current_asset = []
        self.non_current_asset = []
        self.total_asset = []
        self.total_debt = []
        self.current_debt = []
        self.non_current_debt = []
        self.ownership_right_total = []
        self.total_sum_equity_debt = []
        self.inventory = []
        self.net_sale = []
        self.operational_profit = []
        self.net_profit = []
        self.proceed_profit = []
        self.salary_fee = []
        self.gross_profit = []
        self.gross_profit_margin = []
        self.profit_margin_ratio = []
        self.sold_product_total_fee = []
        self.consuming_material = []
        self.production_fee = []
        self.construction_overhead = []
        self.production_total_price = []
        self.salary_production_fee = []
        self.accumulated_profit = []
        self.equity_per_total_debt_ratio = []
        self.equity_per_total_non_current_asset_ratio = []
        self.usability = []
        self.efficiency = []
        self.roa = []
        self.roab = []
        self.roe = []
        self.debt_ratio = []
        self.capital_ratio = []
        self.proprietary_ratio = []
        self.current_ratio = []
        self.instant_ratio = []
        self.stock_turnover = []
        self.capital_to_asset_ratio = []
        self.accumulated_profit_to_asset_ratio = []
        self.before_tax_profit_to_asset_ratio = []
        self.equity_to_debt_ratio = []
        self.sale_to_asset_ratio = []
        self.altman_bankrupsy_ratio = []
        
        self.process_assets()

    def process_assets(self):
        for financial_asset in self.financial_assets:
            sold_product_fee = financial_asset.sold_product_fees.first()
            profit_loss_statement = financial_asset.profit_loss_statements.first()
            balance_report = financial_asset.balance_reports.first()
            account_turnover = financial_asset.account_turnovers.first()

            if balance_report:
                self._process_balance_report(financial_asset, balance_report)

            if profit_loss_statement:
                self._process_profit_loss_statement(
                    profit_loss_statement, balance_report)

            if sold_product_fee:
                self._process_sold_product_fee(
                    sold_product_fee, profit_loss_statement)

            if account_turnover:
                self._process_account_turnover(account_turnover)
        self._calculate_ratios()

    def _process_balance_report(self, financial_asset, balance_report):
        self.year.append(int(financial_asset.year))
        self.month.append(int(financial_asset.month)
                          if financial_asset.month else "")
        current_asset_value = int(balance_report.total_current_asset)
        non_current_asset_value = int(balance_report.total_non_current_asset)
        total_asset_value = current_asset_value + non_current_asset_value

        current_debt_value = int(balance_report.total_current_debt)
        non_current_debt_value = int(balance_report.total_non_current_debt)
        total_debt_value = current_debt_value + non_current_debt_value
        ownership_right_total_value = int(balance_report.ownership_right_total)

        self.current_asset.append(current_asset_value)
        self.non_current_asset.append(non_current_asset_value)
        self.total_asset.append(total_asset_value)
        self.total_debt.append(total_debt_value)
        self.current_debt.append(current_debt_value)
        self.non_current_debt.append(non_current_debt_value)
        self.ownership_right_total.append(ownership_right_total_value)
        self.total_sum_equity_debt.append(
            total_debt_value + ownership_right_total_value)

        inventory_value = balance_report.inventory
        net_sale_value = balance_report.net_sale

        if inventory_value is not None:
            self.inventory.append(int(inventory_value))
        if net_sale_value is not None:
            self.net_sale.append(int(net_sale_value))

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

        self.operational_profit.append(int(operational_profit_value))
        self.net_profit.append(net_profit_value)
        self.proceed_profit.append(int(proceed_profit_value))
        self.salary_fee.append(int(salary_fee_value))
        self.gross_profit.append(int(gross_profit_value))

        if operational_income_value and int(operational_income_value) != 0:
            self.gross_profit_margin.append(
                gross_profit_value / int(operational_income_value))
            if balance_report and balance_report.net_profit:
                self.profit_margin_ratio.append(
                    net_profit_value / int(operational_income_value))
        else:
            self.gross_profit_margin.append(0)
            self.profit_margin_ratio.append(0)

    def _process_sold_product_fee(self, sold_product_fee, profit_loss_statement):
        sold_product_total_fee_value = sold_product_fee.sold_product_total_price
        consuming_material_value = sold_product_fee.consuming_material
        production_fee_value = sold_product_fee.direct_wage
        construction_overhead_value = sold_product_fee.construction_overhead
        production_total_price_value = sold_product_fee.production_total_price
        salary_production_fee_value = (int(profit_loss_statement.salary_fee + production_fee_value)
                                       if profit_loss_statement and production_fee_value else 0)

        self.sold_product_total_fee.append(int(sold_product_total_fee_value))
        self.consuming_material.append(int(consuming_material_value))
        self.production_fee.append(int(production_fee_value))
        self.construction_overhead.append(int(construction_overhead_value))
        self.production_total_price.append(int(production_total_price_value))
        self.salary_production_fee.append(salary_production_fee_value)

    def _process_account_turnover(self, account_turnover):
        accumulated_profit_value = account_turnover.end_year_accumulated_profit
        if accumulated_profit_value is not None:
            self.accumulated_profit.append(int(accumulated_profit_value))
        else:
            self.accumulated_profit.append(0)

    def _calculate_ratios(self):
        for i in range(self.length):
            # Ensure no division by zero
            if self.net_sale[i] != 0:
                self.usability.append(self.net_profit[i] / self.net_sale[i])
            else:
                self.usability.append(0)

            if self.total_asset[i] != 0:
                self.efficiency.append(self.net_sale[i] / self.total_asset[i])
            else:
                self.efficiency.append(0)

        # ROA and ROE Calculations
        total_asset_mean = sum(self.total_asset) / \
            len(self.total_asset) if self.total_asset else 0
        for i in range(self.length):
            self.roa.append(
                self.net_profit[i] / total_asset_mean if total_asset_mean != 0 else 0)
            self.roab.append(self.usability[i] * self.efficiency[i])
            self.roe.append(self.net_profit[i] / self.ownership_right_total[i]
                            if self.ownership_right_total[i] != 0 else 0)

            # Debt and Capital Ratios
        for i in range(self.length):
            self.debt_ratio.append(
                self.total_debt[i] / self.total_asset[i] if self.total_asset[i] != 0 else 0)
            self.capital_ratio.append(
                self.net_profit[i] / self.ownership_right_total[i] if self.ownership_right_total[i] != 0 else 0)

        # Proprietary ratio
        for i in range(self.length):
            if len(self.proceed_profit) > 0:
                if self.proceed_profit[i] != 0:
                    self.proprietary_ratio.append(
                        self.total_asset[i]/self.proceed_profit[i])
                else:
                    self.proprietary_ratio.append(0)

        # equity_per (total_debt_ratio , non_current_asset_ratio)
        for i in range(self.length):
            if self.total_debt[i] != 0:
                self.equity_per_total_debt_ratio.append(
                    self.ownership_right_total[i]/self.total_debt[i]
                )
            else:
                self.equity_per_total_debt_ratio.append(0)
            if self.non_current_asset[i] != 0:
                self.equity_per_total_non_current_asset_ratio.append(
                    self.ownership_right_total[i]/self.non_current_asset[i]
                )
            else:
                self.equity_per_total_non_current_asset_ratio.append(0)

        # current ratio, instant ratio

        for i in range(self.length):
            if self.current_debt[i] != 0:
                self.current_ratio.append(
                    self.current_asset[i]/self.current_debt[i])
            else:
                self.current_ratio.append(0)
            if self.current_debt[i] != 0:
                self.instant_ratio.append(
                    (self.current_asset[i] -
                        self.inventory[i])/self.current_debt[i]
                )
            else:
                self.instant_ratio.append(0)

        # missing cash ratio
        # missing ROI

        # stock turnover
        for i in range(self.length):
            if np.mean(self.inventory) != 0:
                self.stock_turnover.append(
                    float(self.sold_product_total_fee[i]/np.mean(self.inventory)))
            else:
                self.stock_turnover.append(0)

        for i in range(self.length):
            a = self.current_asset[i]-self.current_debt[i]
            if self.total_asset[i] != 0:
                self.capital_to_asset_ratio.append(a/self.total_asset[i])

                self.accumulated_profit_to_asset_ratio.append(
                    self.accumulated_profit[i]/self.total_asset[i])

                self.before_tax_profit_to_asset_ratio.append(
                    self.proceed_profit[i]/self.total_asset[i])

                self.equity_to_debt_ratio.append(
                    self.ownership_right_total[i]/self.total_debt[i]) if self.total_debt[i] != 0 else 0

                self.sale_to_asset_ratio.append(
                    self.net_sale[i]/self.total_asset[i])

        for i in range(self.length):
            if self.total_asset[i] != 0:
                self.capital_to_asset_ratio.append(
                    (self.current_asset[i] - self.current_debt[i]) / self.total_asset[i])
                self.accumulated_profit_to_asset_ratio.append(
                    self.accumulated_profit[i] / self.total_asset[i])
                self.before_tax_profit_to_asset_ratio.append(
                    self.proceed_profit[i] / self.total_asset[i])
                self.sale_to_asset_ratio.append(
                    self.net_sale[i] / self.total_asset[i])

                if self.total_debt[i] != 0:
                    self.equity_to_debt_ratio.append(
                        self.ownership_right_total[i] / self.total_debt[i])
                else:
                    self.equity_to_debt_ratio.append(0)
                self.altman_bankrupsy_ratio.append(
                    1.2 * self.capital_to_asset_ratio[i] +
                    1.4 * self.accumulated_profit_to_asset_ratio[i] +
                    3.3 * self.before_tax_profit_to_asset_ratio[i] +
                    0.6 * (self.equity_per_total_debt_ratio[i] if i < len(self.equity_per_total_debt_ratio) else 0) +
                    self.sale_to_asset_ratio[i]
                )
            else:
                self.capital_to_asset_ratio.append(0)
                self.accumulated_profit_to_asset_ratio.append(0)
                self.before_tax_profit_to_asset_ratio.append(0)
                self.sale_to_asset_ratio.append(0)
                self.altman_bankrupsy_ratio.append(0)

    def get_results(self):
        return {
            'status': 'success',
            'data': {
                'year': self.year,
                'month': self.month,
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