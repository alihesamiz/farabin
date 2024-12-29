import numpy as np


def current_asset_function(self, balance_report):
    """
    Current Asset calculation
    """
    if balance_report:

        self.balance_report_values["current_asset"].append(
            balance_report.total_current_asset)
    else:
        self.balance_report_values["current_asset"].append(
            0)  # or some other default value


def non_current_asset_function(self, balance_report):
    """
    Non-Current Asset Mean calculation
    """
    if balance_report:
        self.balance_report_values["non_current_asset"].append(
            balance_report.total_non_current_asset)
    else:
        self.balance_report_values["non_current_asset"].append(0)


def total_asset_function(self, balance_report):
    """
    Total Asset calculation
    """
    if balance_report:
        self.balance_report_values["total_asset"].append(
            balance_report.total_non_current_asset + balance_report.total_current_asset)
    else:
        self.balance_report_values["total_asset"].append(0)

#########################
# Debt Functions        #
#########################


def current_debt_function(self, balance_report):
    """
    Current debt calculation
    """
    if balance_report:
        self.balance_report_values["current_debt"].append(
            balance_report.total_current_debt)
    else:
        self.balance_report_values["current_debt"].append(0)


def non_current_debt_function(self, balance_report):
    """
    Non Current debt calculation
    """
    if balance_report:
        self.balance_report_values["non_current_debt"].append(
            balance_report.total_non_current_debt)
    else:
        self.balance_report_values["non_current_debt"].append(0)


def total_debt_function(self, balance_report):
    """
    Total debt calculation
    """
    if balance_report:
        self.balance_report_values["total_debt"].append(
            balance_report.total_non_current_debt + balance_report.total_current_debt)
    else:
        self.balance_report_values["total_debt"].append(0)


def inventory_function(self, balance_report):
    """
    Inventory calculation
    """
    if balance_report:
        self.balance_report_values["inventory"].append(
            (balance_report.first_period_inventory+balance_report.end_period_inventory)/2)
    else:
        self.balance_report_values["inventory"].append(0)


def net_sale_function(self, balance_report):
    """
    Net Sale calculation
    """
    if balance_report:
        self.balance_report_values["net_sale"].append(
            balance_report.net_sale)
    else:
        self.balance_report_values["net_sale"].append(0)


def net_profit_function(self, balance_report):
    """
    Net Profit calculation
    """
    if balance_report:
        self.balance_report_values["net_profit"].append(
            balance_report.net_profit)
    else:
        self.balance_report_values["net_profit"].append(0)


def accumulated_profit_function(self, balance_report):
    """
    Accumulated Profit/Loss calculation
    """
    if balance_report:
        self.balance_report_values["accumulated_profit"].append(
            balance_report.accumulated_profit_loss)
    else:
        self.balance_report_values["accumulated_profit"].append(0)


def ownership_right_total_function(self, balance_report):
    """
    Total ownership right calculation
    """
    if balance_report:
        self.balance_report_values["ownership_right_total"].append(
            balance_report.ownership_right_total)
    else:
        self.balance_report_values["ownership_right_total"].append(0)


def trade_payable_function(self, balance_report):
    if balance_report:
        self.balance_report_values["trade_payable"].append(
            balance_report.trade_payable)
    else:
        self.balance_report_values["trade_payable"].append(0)


def advance_function(self, balance_report):
    if balance_report:
        self.balance_report_values["advance"].append(
            balance_report.advance)
    else:
        self.balance_report_values["advance"].append(0)


def reserves_function(self, balance_report):
    if balance_report:
        self.balance_report_values["reserves"].append(
            balance_report.reserves)
    else:
        self.balance_report_values["reserves"].append(0)


def long_term_payable_function(self, balance_report):
    if balance_report:
        self.balance_report_values["long_term_payable"].append(
            balance_report.long_term_payable)
    else:
        self.balance_report_values["long_term_payable"].append(0)


def employee_termination_benefit_reserve_function(self, balance_report):
    if balance_report:
        self.balance_report_values["employee_termination_benefit_reserve"].append(
            balance_report.employee_termination_benefit_reserve)
    else:
        self.balance_report_values["employee_termination_benefit_reserve"].append(
            0)


def operational_profit_function(self, profit_loss_statement):
    """
    Operational Profit calculation
    """
    if profit_loss_statement:
        self.profit_loss_statement_values["operational_profit"].append(
            profit_loss_statement.operational_profit)
    else:
        self.profit_loss_statement_values["operational_profit"].append(0)


def gross_profit_function(self, profit_loss_statement):
    """
    Gross Profit Mean calculation
    """
    if profit_loss_statement:
        self.profit_loss_statement_values["gross_profit"].append(
            profit_loss_statement.gross_profit)
    else:
        self.profit_loss_statement_values["gross_profit"].append(0)


def proceed_profit_function(self, profit_loss_statement):
    """
    Proceed Profit calculation
    """
    if profit_loss_statement:
        self.profit_loss_statement_values["proceed_profit"].append(
            profit_loss_statement.proceed_profit)
    else:
        self.profit_loss_statement_values["proceed_profit"].append(0)


def salary_fee_function(self, profit_loss_statement):
    """Salary Fee calculation
    """
    if profit_loss_statement:
        self.profit_loss_statement_values["salary_fee"].append(
            profit_loss_statement.salary_fee)
    else:
        self.profit_loss_statement_values["salary_fee"].append(0)


def operational_income_expense_function(self, profit_loss_statement):
    """Operational Income Expense calculation"""
    if profit_loss_statement:
        self.profit_loss_statement_values["operational_income_expense"].append(
            profit_loss_statement.operational_income_expense)
    else:
        self.profit_loss_statement_values["operational_income_expense"].append(
            0)


def marketing_fee_function(self, profit_loss_statement):
    """Marketing Fee calculation"""
    if profit_loss_statement:
        self.profit_loss_statement_values["marketing_fee"].append(
            profit_loss_statement.marketing_fee)
    else:
        self.profit_loss_statement_values["marketing_fee"].append(0)


def consuming_material_function(self, sold_product_fee):
    """
    Consuming Material calculation
    """
    if sold_product_fee:
        self.sold_product_values["consuming_material"].append(
            sold_product_fee.consuming_material)
    else:
        self.sold_product_values["consuming_material"].append(0)


def construction_overhead_function(self, sold_product_fee):
    """
    Construction Overhead calculation
    """
    if sold_product_fee:
        self.sold_product_values["construction_overhead"].append(
            sold_product_fee.construction_overhead)
    else:
        self.sold_product_values["construction_overhead"].append(0)


def production_total_price_function(self, sold_product_fee):
    """
    Production Total Price calculation
    """
    if sold_product_fee:
        self.sold_product_values["production_total_price"].append(
            sold_product_fee.production_total_price)
    else:
        self.sold_product_values["production_total_price"].append(0)


def direct_wage_function(self, sold_product_fee):
    """
    Direct Wage calculation
    """
    if sold_product_fee:
        self.sold_product_values["direct_wage"].append(
            sold_product_fee.direct_wage)
    else:
        self.sold_product_values["direct_wage"].append(0)


def sold_product_total_fee_function(self, sold_product_fee):
    """Sold Product Total Fee calculation"""
    if sold_product_fee:
        self.sold_product_values["sold_product_total_fee"].append(
            sold_product_fee.sold_product_total_price)
    else:
        self.sold_product_values["sold_product_total_fee"].append(0)


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
            self.balance_report_values["net_profit"][i]/self.balance_report_values["net_sale"][i] if self.balance_report_values["net_sale"][i] != 0 else 0)


def efficiency_function(self):
    """
    Efficiency calculation
    """
    for i in range(self.length):
        self.efficiency.append(self.balance_report_values["net_sale"][i]/self.balance_report_values["total_asset"][i]
                               if self.balance_report_values["total_asset"][i] != 0 else 0)


def roa_function(self):
    """
    Return on Assets (ROA) calculation
    """
    for i in range(self.length):
        self.roa.append(
            self.balance_report_values["net_profit"][i]/self.balance_report_values["total_asset"][i] if self.balance_report_values["total_asset"][i] != 0 else 0)


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
            self.balance_report_values["net_profit"][i]/self.balance_report_values["ownership_right_total"][i] if self.balance_report_values["ownership_right_total"][i] != 0 else 0)


def equity_per_total_non_current_asset_ratio_function(self):
    for i in range(self.length):
        self.equity_per_total_non_current_asset_ratio.append(
            self.balance_report_values["ownership_right_total"][i] /
            self.balance_report_values["non_current_asset"][i]
            if self.balance_report_values["non_current_asset"][i] != 0 else 0)


def gross_profit_margin_ratio_function(self):
    """
    Gross Profit Margin Ratio calculation
    """
    for i in range(self.length):
        self.gross_profit_margin_ratio.append(
            self.profit_loss_statement_values["gross_profit"][i]/self.balance_report_values["net_sale"][i] if self.balance_report_values["net_sale"][i] != 0 else 0)


def net_profit_margin_ratio_function(self):
    """
    Net Profit Margin Ratio calculation
    """
    for i in range(self.length):
        self.net_profit_margin_ratio.append(
            self.balance_report_values["net_profit"][i]/self.balance_report_values["net_sale"][i] if self.balance_report_values["net_sale"][i] != 0 else 0)


def operational_profit_margin_function(self):
    """Operational Profit Margin calculation
    """
    pass


def total_sum_equity_debt_function(self):
    """Total Sum of Equity and Debt calculation
    """
    for i in range(self.length):
        self.total_sum_equity_debt.append(
            self.balance_report_values["ownership_right_total"][i] + self.balance_report_values["total_debt"][i])


def debt_ratio_function(self):
    """
    Debt Ratio calculation
    """
    for i in range(self.length):
        self.debt_ratio.append(
            self.balance_report_values["total_debt"][i]/self.balance_report_values["total_asset"][i] if self.balance_report_values["total_asset"][i] != 0 else 0)


def salary_production_fee_function(self):
    for i in range(self.length):
        self.salary_production_fee.append(
            self.sold_product_values["direct_wage"][i] + self.profit_loss_statement_values["salary_fee"][i])


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
            self.balance_report_values["net_profit"][i]/self.balance_report_values["ownership_right_total"][i] if self.balance_report_values["ownership_right_total"][i] != 0 else 0)


def fixed_asset_to_proceed_profit_ratio_function(self):
    """Fixed Asset to Proceed Profit Ratio calculation"""
    pass


def total_debt_to_proceed_profit_ratio_function(self):
    """Total Debt to Proceed Profit Ratio calculation"""
    for i in range(self.length):
        self.total_debt_to_proceed_profit_ratio.append(
            self.balance_report_values["total_debt"][i]/self.profit_loss_statement_values["proceed_profit"][i] if self.profit_loss_statement_values["proceed_profit"][i] != 0 else 0)


def current_debt_to_proceed_profit_ratio_function(self):
    """Current Debt to Proceed Profit Ratio calculation"""
    for i in range(self.length):
        self.current_debt_to_proceed_profit_ratio.append(
            self.balance_report_values["current_debt"][i]/self.profit_loss_statement_values["proceed_profit"][i] if self.profit_loss_statement_values["proceed_profit"][i] != 0 else 0)


def properitary_ratio_function(self):
    """Proprietary Ratio calculation"""
    for i in range(self.length):
        self.proprietary_ratio.append(
            self.profit_loss_statement_values["proceed_profit"][i]/self.balance_report_values["total_asset"][i] if self.balance_report_values["total_asset"][i] != 0 else 0)


def equity_per_total_debt_ratio_function(self):
    """Equity Per Total Debt Ratio calculation"""
    for i in range(self.length):
        self.equity_per_total_debt_ratio.append(
            self.balance_report_values["total_debt"][i]/self.balance_report_values["ownership_right_total"][i] if self.balance_report_values["ownership_right_total"][i] != 0 else 0)


def equity_per_total_fixed_asset_ratio_function(self):
    """Equity Per Total Fixed Asset Ratio calculation"""
    pass


def current_ratio_function(self):
    """Current Ratio calculation"""
    for i in range(self.length):
        self.current_ratio.append(
            self.balance_report_values["current_asset"][i]/self.balance_report_values["current_debt"][i] if self.balance_report_values["current_debt"][i] != 0 else 0)


def instant_ratio_function(self):
    """Current Ratio calculation"""
    for i in range(self.length):
        self.instant_ratio.append(
            (self.balance_report_values["current_asset"][i]-self.balance_report_values["inventory"][i])/self.balance_report_values["current_debt"][i] if self.balance_report_values["current_debt"][i] != 0 else 0)


def liquidity_ratio_function(self):
    """Liquidity Ratio calculation"""
    pass


def stock_turn_over_ratio_function(self):
    """Stock Turnover Ratio calculation"""
    avg_inventory = np.mean(
        self.balance_report_values["inventory"])
    for i in range(self.length):
        if avg_inventory != 0:
            self.stock_turnover.append(
                self.sold_product_values["sold_product_total_fee"][i] / avg_inventory)
        else:
            self.stock_turnover.append(0)


def received_turn_over_ratio_function(self):
    """Received Turnover Ratio calculation"""
    pass


def average_collection_period_function(self):
    """Average Collection Period calculation"""
    pass


def total_asset_turnover_ratio_function(self):
    """Total Asset Turnover Ratio calculation"""
    total_asset_mean = np.mean(self.balance_report_values["total_asset"])
    for i in range(self.length):
        self.total_asset_turnover_ratio.append(
            self.balance_report_values["net_sale"][i]/total_asset_mean if total_asset_mean != 0 else 0)


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
            (self.balance_report_values["current_asset"][i] - self.balance_report_values["current_debt"][i]) / self.balance_report_values["total_asset"][i] if self.balance_report_values["total_asset"][i] != 0 else 0)


def accumulated_profit_to_asset_ratio_function(self):
    """
    Accumulated Profit to Asset Ratio calculation
    """

    for i in range(self.length):
        self.accumulated_profit_to_asset_ratio.append(
            self.balance_report_values["accumulated_profit"][i] / self.balance_report_values["total_asset"][i] if self.balance_report_values["total_asset"][i] != 0 else 0)


def before_tax_profit_to_asset_ratio_function(self):
    """
    Before Tax Profit to Asset Ratio calculation
    """
    for i in range(self.length):
        self.before_tax_profit_to_asset_ratio.append(
            self.profit_loss_statement_values["proceed_profit"][i] / self.balance_report_values["total_asset"][i] if self.balance_report_values["total_asset"][i] != 0 else 0)


def sale_to_asset_ratio_function(self):
    """
    Sale to Asset Ratio calculation
    """
    for i in range(self.length):
        self.sale_to_asset_ratio.append(
            self.balance_report_values["net_sale"][i] / self.balance_report_values["total_asset"][i] if self.balance_report_values["total_asset"][i] != 0 else 0)


def equity_to_debt_ratio_function(self):
    """
    Equity to Debt Ratio calculation
    """
    for i in range(self.length):
        self.equity_to_debt_ratio.append(
            self.balance_report_values["ownership_right_total"][i] / self.balance_report_values["total_debt"][i] if self.balance_report_values["total_debt"][i] != 0 else 0)


def altman_bankruptcy_ratio_function(self):
    """Altman Bankruptcy Ratio calculation"""
    from decimal import Decimal
    for i in range(self.length):
        self.altman_bankrupsy_ratio.append(
            (Decimal(1.2) * self.capital_to_asset_ratio[i]) +
            (Decimal(1.4) * self.accumulated_profit_to_asset_ratio[i]) +
            (Decimal(3.3) * self.before_tax_profit_to_asset_ratio[i]) +
            (Decimal(0.6) * self.equity_per_total_debt_ratio[i]) +
            (Decimal(.999)*self.sale_to_asset_ratio[i])
        )
