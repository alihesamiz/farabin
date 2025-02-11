from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.db import models


class SoldProductFee(models.Model):
    financial_asset = models.ForeignKey(
        'FinancialAsset', on_delete=models.CASCADE, related_name='sold_product_fees', verbose_name=_('Financial Asset'))
    consuming_material = models.DecimalField(default=0,
                                             max_digits=20, decimal_places=0, verbose_name=_('Consuming Material'))
    direct_wage = models.DecimalField(default=0,
                                      max_digits=20, decimal_places=0, verbose_name=_('Direct Wage'))
    construction_overhead = models.DecimalField(default=0,
                                                max_digits=20, decimal_places=0, verbose_name=_('Construction Overhead'))
    production_total_price = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Production Total Price'))
    first_period_constructing_product_inventory = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Current Constructing Product First Period'))
    end_period_constructing_product_inventory = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Current Constructing Product End Period'))
    produced_product_total_price = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Produced Product Total Price'))
    first_period_produced_inventory = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('First Period Produced Inventory'))
    period_bought_product = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Period Bought Product'))
    ready_for_sale_product = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Ready for Sale Product'))
    end_period_inventory = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('End Period Inventory'))
    product_other = models.DecimalField(
        max_digits=20, decimal_places=0, default=0, verbose_name=_('Other Product'))
    sold_product_total_price = models.DecimalField(default=0,
                                                   max_digits=20, decimal_places=0, verbose_name=_('Sold Product Total Price'))

    def __str__(self):
        return f"{self.financial_asset}"

    class Meta:
        unique_together = ('financial_asset',)
        verbose_name = _("Sold Product Fee")
        verbose_name_plural = _("Sold Products Fee")


class ProfitLossStatement(models.Model):
    financial_asset = models.ForeignKey(
        'FinancialAsset', on_delete=models.CASCADE, related_name='profit_loss_statements', verbose_name=_('Financial Asset'))
    operational_income = models.DecimalField(default=0,
                                             max_digits=20, decimal_places=0, verbose_name=_('Operational Income'))
    operational_income_expense = models.DecimalField(default=0,
                                                     max_digits=20, decimal_places=0, verbose_name=_('Operational Income Expense'))
    gross_profit = models.DecimalField(default=0,
                                       max_digits=20, decimal_places=0, verbose_name=_('Gross Profit'))
    salary_fee = models.DecimalField(default=0,
                                     max_digits=20, decimal_places=0, verbose_name=_('Salary Fee'))
    marketing_fee = models.DecimalField(default=0,
                                        max_digits=20, decimal_places=0, verbose_name=_('Marketing Fee'))
    doubtful_burnt_claims_fee = models.DecimalField(
        max_digits=20, default=0, decimal_places=0, verbose_name=_('Doubtful Burnt Claims Fee'))
    attendance_fee = models.DecimalField(default=0,
                                         max_digits=20, decimal_places=0, verbose_name=_('Attendance Fee'))
    accounting_fee = models.DecimalField(default=0,
                                         max_digits=20, decimal_places=0, verbose_name=_('Accounting Fee'))
    consulting_fee = models.DecimalField(default=0,
                                         max_digits=20, decimal_places=0, verbose_name=_('Consulting Fee'))
    rental_fee = models.DecimalField(default=0,
                                     max_digits=20, decimal_places=0, verbose_name=_('Rental Fee'))
    other_general_expense = models.DecimalField(default=0,
                                                max_digits=20, decimal_places=0, verbose_name=_('Other General Expense'))
    total_general_expense = models.DecimalField(default=0,
                                                max_digits=20, decimal_places=0, verbose_name=_('Total General Expense'))
    other_operation_income = models.DecimalField(default=0,
                                                 max_digits=20, decimal_places=0, verbose_name=_('Other Operational Income'))
    other_operational_expense = models.DecimalField(default=0,
                                                    max_digits=20, decimal_places=0, verbose_name=_('Other Operational Expense'))
    operational_profit = models.DecimalField(default=0,
                                             max_digits=20, decimal_places=0, verbose_name=_('Operational Profit'))
    immovable_property_sale_profit = models.DecimalField(default=0,
                                                         max_digits=20, decimal_places=0, verbose_name=_('Immovable Property Sale Profit'))
    other_assets_sale_profit = models.DecimalField(default=0,
                                                   max_digits=20, decimal_places=0, verbose_name=_('Other Assets Sale Profit'))
    material_sale_profit = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_('Material Sale Profit'))
    investment_sale_profit = models.DecimalField(default=0,
                                                 max_digits=20, decimal_places=0, verbose_name=_('Investment Sale Profit'))
    interpretation_profit = models.DecimalField(default=0,
                                                max_digits=20, decimal_places=0, verbose_name=_('Interpretation Profit'))
    dividend_profit = models.DecimalField(default=0,
                                          max_digits=20, decimal_places=0, verbose_name=_('Dividend Profit'))
    investment_profit = models.DecimalField(default=0,
                                            max_digits=20, decimal_places=0, verbose_name=_('Investment Profit'))
    bank_deposit_profit = models.DecimalField(default=0,
                                              max_digits=20, decimal_places=0, verbose_name=_('Bank Deposit Profit'))
    rental_income = models.DecimalField(default=0,
                                        max_digits=20, decimal_places=0, verbose_name=_('Rental Income'))
    incidental_income = models.DecimalField(default=0,
                                            max_digits=20, decimal_places=0, verbose_name=_('Incidental Income'))
    other_non_operationl_income_expense = models.DecimalField(default=0,
                                                              max_digits=20, decimal_places=0, verbose_name=_('Other Non-Operational Income/Expense'))
    net_value_other_non_operationl_income_expense = models.DecimalField(default=0,
                                                                        max_digits=20, decimal_places=0, verbose_name=_('Net Value Other Non-Operational Income/Expense'))
    financial_expense = models.DecimalField(default=0,
                                            max_digits=20, decimal_places=0, verbose_name=_('Financial Expense'))
    proceed_profit = models.DecimalField(default=0,
                                         max_digits=20, decimal_places=0, verbose_name=_('Proceed Profit'))
    current_year_income_tax = models.DecimalField(default=0,
                                                  max_digits=20, decimal_places=0, verbose_name=_('Current Year Income Tax'))
    prev_year_income_tax = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_('Previous Year Income Tax'))
    profit_after_tax = models.DecimalField(default=0,
                                           max_digits=20, decimal_places=0, verbose_name=_('Profit After Tax'))

    def __str__(self):
        return f"{self.financial_asset}"

    class Meta:
        unique_together = ('financial_asset',)
        verbose_name = _("Profit And Loss Statement")
        verbose_name_plural = _("Profit And Loss Statements")


class BalanceReport(models.Model):

    financial_asset = models.ForeignKey(
        'FinancialAsset', on_delete=models.CASCADE, related_name='balance_reports', verbose_name=_('Financial Asset'))

    advance_payment = models.DecimalField(default=0,
                                          max_digits=20, decimal_places=0, verbose_name=_('Advance Payment'))
    first_period_inventory = models.DecimalField(default=0,
                                                 max_digits=20, decimal_places=0, verbose_name=_('First Period Inventory'))
    end_period_inventory = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_('End Period Inventory'))
    trade_receivable = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Recievable Trade Account'))
    short_term_investment = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Short term Investment'))

    cash_balance = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Cash Balance'))

    held_non_current_asset = models.DecimalField(default=0,
                                                 max_digits=20, decimal_places=0, verbose_name=_('Non-current assets held for sale'))
    current_shareholder_asset = models.DecimalField(default=0,
                                                    max_digits=20, decimal_places=0, verbose_name=_('Current Partner/Shareholder'))
    total_current_asset = models.DecimalField(default=0,
                                              max_digits=20, decimal_places=0, verbose_name=_('Total Current Asset'))

    # non-current assets

    tangible_fixed_asset = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_('Tangible Fixed Asset'))
    property_investment = models.DecimalField(default=0,
                                              max_digits=20, decimal_places=0, verbose_name=_('Property Investment'))
    intangible_asset = models.DecimalField(default=0,
                                           max_digits=20, decimal_places=0, verbose_name=_('Intangible Asset'))
    long_term_investment = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_('Long Term Investment'))
    long_term_receivable = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_('Long Term Receivable'))
    other_asset = models.DecimalField(default=0,
                                      max_digits=20, decimal_places=0, verbose_name=_('Other Asset'))
    total_non_current_asset = models.DecimalField(default=0,
                                                  max_digits=20, decimal_places=0, verbose_name=_('Total Non-Current Asset'))

    # ownership right
    capital = models.DecimalField(default=0,
                                  max_digits=20, decimal_places=0, verbose_name=_("Wealth"))
    capital_increase = models.DecimalField(default=0,
                                           max_digits=20, decimal_places=0, verbose_name=_("Wealth Increase"))
    share_spend = models.DecimalField(default=0,
                                      max_digits=20, decimal_places=0, verbose_name=_("Share Spend"))
    treasury_share_spend = models.DecimalField(default=0,
                                               max_digits=20, decimal_places=0, verbose_name=_("Treasury Share Spend"))
    legal_reserve = models.DecimalField(default=0,
                                        max_digits=20, decimal_places=0, verbose_name=_("Legal Reserve"))
    other_reserve = models.DecimalField(default=0,
                                        max_digits=20, decimal_places=0, verbose_name=_("Other Reserve"))
    revaluation_surplus = models.DecimalField(default=0, max_digits=20, decimal_places=0, verbose_name=_(
        "Asset Revaluation Surplus and Other Unrealized Gains"))
    accumulated_profit_loss = models.DecimalField(default=0,
                                                  max_digits=20, decimal_places=0, verbose_name=_("Accumulated Profit and Loss"))
    treasury_share = models.DecimalField(default=0,
                                         max_digits=20, decimal_places=0, verbose_name=_("Treasury Share"))

    ownership_right_total = models.DecimalField(default=0,
                                                max_digits=20, decimal_places=0, verbose_name=_("Ownership right total"))

    # Current Debt
    trade_payable = models.DecimalField(default=0,
                                        max_digits=20, decimal_places=0, verbose_name=_("Trade Payable"))
    paid_tax = models.DecimalField(default=0,
                                   max_digits=20, decimal_places=0, verbose_name=_("Paid Tax"))
    dividend_payable = models.DecimalField(default=0,
                                           max_digits=20, decimal_places=0, verbose_name=_("Dividend Payable"))
    financial_facility = models.DecimalField(default=0,
                                             max_digits=20, decimal_places=0, verbose_name=_("Financial Facility"))
    reserves = models.DecimalField(default=0,
                                   max_digits=20, decimal_places=0, verbose_name=_("Reserves"))
    advance = models.DecimalField(default=0,
                                  max_digits=20, decimal_places=0, verbose_name=_("Advance"))
    held_for_sale_liability = models.DecimalField(default=0, max_digits=20, decimal_places=0, verbose_name=_(
        "Liability related to non-current asset held for sale"))
    current_shareholder_debt = models.DecimalField(default=0,
                                                   max_digits=20, decimal_places=0, verbose_name=_("Current Partner/Shareholder"))
    total_current_debt = models.DecimalField(default=0,
                                             max_digits=20, decimal_places=0, verbose_name=_('Total Current Debt'))

    # Non Current Debt
    long_term_payable = models.DecimalField(default=0,
                                            max_digits=20, decimal_places=0, verbose_name=_("Longterm Payable"))
    long_term_financial = models.DecimalField(default=0,
                                              max_digits=20, decimal_places=0, verbose_name=_("Longterm Financial Facilities"))
    employee_termination_benefit_reserve = models.DecimalField(default=0,
                                                               max_digits=20, decimal_places=0, verbose_name=_("Reserve Employee Termination Benefit"))
    total_non_current_debt = models.DecimalField(default=0,
                                                 max_digits=20, decimal_places=0, verbose_name=_('Total Non-Current Debt'))

    net_sale = models.DecimalField(default=0,
                                   max_digits=20, decimal_places=0, verbose_name=_('Net Sale'))
    net_profit = models.DecimalField(default=0,
                                     max_digits=20, decimal_places=0, verbose_name=_('Net Profit'))

    def __str__(self):
        return f"{self.financial_asset}"

    class Meta:
        unique_together = [['financial_asset',]]
        verbose_name = _("Balance Report")
        verbose_name_plural = _("Balance Reports")


class AccountTurnOver(models.Model):
    financial_asset = models.ForeignKey(
        'FinancialAsset', on_delete=models.CASCADE, related_name='account_turnovers', verbose_name=_('Financial Asset'))
    profit_after_tax = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Profit After Tax'))
    first_year_accumulated_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('First Year  Accumulated Profit'))
    correcting_mistake = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Correcting Mistake'))
    accounting_method_change = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Accounting Method Change'))
    first_year_accumulated_profit_balanced = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('First Year`s Accumulated Profit Balanced'))
    transfer_from_reserve = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Transfer From Reserve'))
    other_account_turnover = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Other Account Turnover'))
    allocable_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Allocable Profit'))
    share_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Share Profit'))
    legal_reserve = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Legal Reserve'))
    wealth_increase = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Wealth Increase'))
    current_wealt_increase = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Current Wealt Increase'))
    other_reserves = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Other Reserves'))
    treasury_share_purchase = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Treasury Share Purchase'))
    treasury_share_sale = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Treasury Share Sale'))
    treasury_share_sale_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Treasury Share Sale Profit'))
    board_reward = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Board Reward'))
    other_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Other Profit'))
    total_allocated_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('Total Allocated Profit'))
    end_year_accumulated_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=0, verbose_name=_('End Year`s Accumulated profit'))

    def __str__(self):
        return f"{self.financial_asset}"

    class Meta:
        unique_together = ('financial_asset',)
        verbose_name = _("Account TurnOver")
        verbose_name_plural = _("Accounts Turnovers")


class FinancialAsset(models.Model):

    company = models.ForeignKey(
        'company.CompanyProfile', on_delete=models.CASCADE, related_name='financial_records',
        verbose_name=_('Company'))

    year = models.PositiveIntegerField(verbose_name=_('Year'))

    month = models.PositiveIntegerField(
        verbose_name=_('Month'), null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(13)])

    is_tax_record = models.BooleanField(
        default=False, verbose_name=_('Is Tax Record'))

    class Meta:
        unique_together = [['company', 'year', 'month']]
        verbose_name = _('Financial Asset')
        verbose_name_plural = _('Financial Assets')

    def __str__(self):
        if self.month:
            return f"{self.company.company_title} › {self.year} › {self.month}"
        return f"{self.company.company_title} › {self.year}"


class FinancialData(models.Model):

    is_published = models.BooleanField(default=False, help_text=_(
        "Define whether the reports are published and shown to the user or not."), verbose_name=_("Publish for user"))

    financial_asset = models.ForeignKey(
        FinancialAsset, on_delete=models.CASCADE, related_name='calculated_data', verbose_name=_('Financial Asset'))
    current_asset = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Current Asset'))
    non_current_asset = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Non-Current Asset'))
    total_asset = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Total Asset'))
    current_debt = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Current Debt'))
    non_current_debt = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Non-Current Debt'))
    total_debt = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Total Debt'))
    total_equity = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Total Equity'))
    total_sum_equity_debt = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Total Equity and Debt Sum'))
    gross_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Gross Profit'))
    net_sale = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Net Sale'))

    operational_income_expense = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Operational Income Expense'))

    marketing_fee = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Marketing Fee'))

    inventory_average = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Inventory Average'))
    operational_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Operational Profit'))
    proceed_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Proceed Profit'))
    net_profit = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Net Profit'))
    consuming_material = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Consuming Material'))
    production_fee = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Production Fee'))
    construction_overhead = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Construction Overhead'))
    production_total_price = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Total Production Price'))
    salary_fee = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Salary Fee'))
    salary_production_fee = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Production Salary Fee'))
    usability = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Usability'))
    efficiency = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Efficiency'))
    roa = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Return on Assets (ROA)'))
    roab = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Return on Assets Before Tax (ROAB)'))
    roe = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Return on Equity (ROE)'))
    gross_profit_margin = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Gross Profit Margin'))
    profit_margin_ratio = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Profit Margin Ratio'))
    debt_ratio = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Debt Ratio'))
    capital_ratio = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Capital Ratio'))
    proprietary_ratio = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Proprietary Ratio'))
    equity_per_total_debt_ratio = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Equity to Total Debt Ratio'))
    equity_per_total_non_current_asset_ratio = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Equity to Non-Current Asset Ratio'))
    current_ratio = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Current Ratio'))
    instant_ratio = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Instant Ratio'))
    stock_turnover = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Stock Turnover'))
    altman_bankrupsy_ratio = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Altman Bankruptcy Ratio'))
    trade_payable = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Trade Payable'))
    advance = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Advance'))
    reserves = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Reserves'))
    long_term_payable = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Long Term Payable'))
    employee_termination_benefit_reserve = models.DecimalField(
        default=0, max_digits=20, decimal_places=2, verbose_name=_('Employee Termination Benefit Reserve'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created At'))

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated At'))

    def __str__(self) -> str:
        if self.financial_asset.month:
            return f"{self.financial_asset.company.company_title} › {self.financial_asset.year} › {self.financial_asset.month}"
        return f"{self.financial_asset.company.company_title} › {self.financial_asset.year}"

    class Meta:
        verbose_name = _("Financial Data")
        verbose_name_plural = _("Financial Datas")


class AnalysisReport(models.Model):

    DEBT_CHART = 'debt'
    ASSET_CHART = 'asset'
    SALE_CHART = 'sale'
    EQUITY_CHART = 'equity'
    LIFE_CYCLE_CHART = 'life_cycle'
    BANKRUPSY_CHART = 'bankrupsy'
    PROFITIBILITY_CHART = 'profitability'
    SALARY_CHART = 'salary'
    INVENTORY_CHART = 'inventory'
    AGILITY_CHART = 'agility'
    LIQUIDITY_CHART = 'liquidity'
    LEVERAGE_CHART = 'leverage'
    COST_CHART = 'cost'
    PROFIT_CHART = 'profit'

    CHART_CHOICES = [
        (DEBT_CHART, _("Debt Chart")),
        (ASSET_CHART, _("Asset Chart")),
        (SALE_CHART, _("Sale Chart")),
        (EQUITY_CHART, _("Equity Chart")),
        (LIFE_CYCLE_CHART, _("Life Cycle Chart")),
        (BANKRUPSY_CHART, _("Bankrupsy Chart")),
        (PROFITIBILITY_CHART, _("Profitability Chart")),
        (SALARY_CHART, _("Salary Chart")),
        (INVENTORY_CHART, _("Inventory Chart")),
        (AGILITY_CHART, _("Agility Chart")),
        (LIQUIDITY_CHART, _("Liquidity Chart")),
        (LEVERAGE_CHART, _("Leverage Chart")),
        (COST_CHART, _("Cost Chart")),
        (PROFIT_CHART, _("Profit Chart")),
    ]
    MONTHLY_PERIOD = 'm'
    YEARLY_PERIOD = 'y'
    PERIOD_CHOICES = [
        (MONTHLY_PERIOD, _("Monthly")),

        (YEARLY_PERIOD, _("Yearly")),

    ]

    period = models.CharField(max_length=7, default=YEARLY_PERIOD, verbose_name=_(
        "Period"), choices=PERIOD_CHOICES)

    # monthly = models.BooleanField(default=False, verbose_name=_("Monthly"))

    # yearly = models.BooleanField(default=False, verbose_name=_("Yearly"))

    calculated_data = models.ForeignKey(
        FinancialData, on_delete=models.CASCADE, related_name='analysis_reports', verbose_name=_('Calculated Data'), help_text=_("Select company assosiated with the year for entering the analysis text report. it would be better to only choose the last yaer of each company"))

    chart_name = models.CharField(max_length=15, verbose_name=_(
        'Chart Name'), help_text=_("Enter the name of each chart"), choices=CHART_CHOICES,)

    text = models.TextField(verbose_name=_('Analysis Text'), help_text=_(
        "Enter the analysis text for each chart"))

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))

    is_published = models.BooleanField(default=False, verbose_name=_(
        'Published'), help_text=_("Select to publish the analysis report"))

    class Meta:
        verbose_name = _("Analysis Report")
        verbose_name_plural = _("Analysis Reports")
        unique_together = ['chart_name', 'calculated_data']

    def __str__(self):
        return f"{self.calculated_data.financial_asset.company.company_title} › {self.calculated_data.financial_asset.year} › {self.chart_name}"
