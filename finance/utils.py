from pathlib import Path
from typing import List
from math import log2
import pandas as pd
import logging


from django.utils.translation import gettext_lazy as _


from finance.functions import (
    current_asset_function,
    non_current_asset_function,
    total_asset_function,
    current_debt_function,
    non_current_debt_function,
    total_debt_function,
    ownership_right_total_function,
    inventory_function,
    net_sale_function,
    net_profit_function,
    accumulated_profit_function,
    operational_profit_function,
    gross_profit_function,
    proceed_profit_function,
    salary_fee_function,
    operational_income_expense_function,
    marketing_fee_function,
    consuming_material_function,
    construction_overhead_function,
    production_total_price_function,
    sold_product_total_fee_function,
    direct_wage_function,
    usability_function,
    efficiency_function,
    roa_function,
    roab_function,
    roe_function,
    gross_profit_margin_ratio_function,
    net_profit_margin_ratio_function,
    debt_ratio_function,
    capital_ratio_function,
    total_debt_to_proceed_profit_ratio_function,
    current_debt_to_proceed_profit_ratio_function,
    properitary_ratio_function,
    equity_per_total_debt_ratio_function,
    current_ratio_function,
    instant_ratio_function,
    total_asset_turnover_ratio_function,
    salary_production_fee_function,
    capital_to_asset_ratio_function,
    accumulated_profit_to_asset_ratio_function,
    before_tax_profit_to_asset_ratio_function,
    sale_to_asset_ratio_function,
    equity_per_total_non_current_asset_ratio_function,
    altman_bankruptcy_ratio_function,
    equity_to_debt_ratio_function,
    total_sum_equity_debt_function,
    stock_turn_over_ratio_function,
    trade_payable_function,
    advance_function,
    reserves_function,
    long_term_payable_function,
    employee_termination_benefit_reserve_function,
)


logger = logging.getLogger("finance")


def get_life_cycle(company):
    # Initialize x_vals and y_vals for graphical representation
    x_vals = [_("Start"), _("Introduction"), _("Growth"), _("Maturity"),
              _("Recession 1"), _("Recession 2"), _("Recession 3"),
              _("Decline 1"), _("Decline 2")]
    x_vals_numerical = [1, 1.5, 2, 2.5, 4, 4.5, 4, 3, 2]
    y_vals = [log2(x) for x in x_vals_numerical]

    life_cycle = company.capital_providing_method.all()
    life_cycles_data = [str(lc) for lc in life_cycle]

    cycle_mappings = {
        ('Operational', 'Finance'): 7,
        ('Operational', 'Invest'): 6,
        ('Finance', 'Invest'): 2,
        ('Operational',): 8,
        ('Finance',): 1,
        ('Invest',): 3
    }

    sorted_cycles = tuple(sorted(life_cycles_data))
    life_cycle_stage = cycle_mappings.get(
        sorted_cycles, 5) if len(sorted_cycles) <= 2 else 5

    return life_cycle_stage, x_vals, y_vals


class FinancialCalculations:
    def __init__(self, financial_assets):
        logger.info("Initializing FinancialCalculations with %d financial assets", len(
            financial_assets))

        self.financial_assets = financial_assets
        self.length = len(self.financial_assets)
        self.year = []
        self.month = []

        self.balance_report_values: dict[str, List] = {
            "current_asset": [],
            "non_current_asset": [],
            "total_asset": [],
            "current_debt": [],
            "non_current_debt": [],
            "total_debt": [],
            "inventory": [],
            "net_sale": [],
            "net_profit": [],
            "accumulated_profit": [],
            "ownership_right_total": [],


            "trade_payable": [],
            "advance": [],
            "reserves": [],
            "long_term_payable": [],
            "employee_termination_benefit_reserve": []
        }

        self.profit_loss_statement_values: dict[str, List] = {
            "operational_profit": [],
            "gross_profit": [],
            "proceed_profit": [],
            "salary_fee": [],
            "operational_income_expense": [],
            "marketing_fee": [],
        }

        self.sold_product_values: dict[str, List] = {
            "consuming_material": [],
            "construction_overhead": [],
            "production_total_price": [],
            "direct_wage": [],
            "sold_product_total_fee": [],
        }

        self.gross_profit_margin_ratio = []
        self.net_profit_margin_ratio = []
        self.total_sum_equity_debt = []
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

            logger.info("Starting to process %d financial assets", self.length)

            for i in range(self.length):
                logger.debug("Processing financial asset %d/%d",
                             i + 1, self.length)
                asset = self.financial_assets[i]

                account_turnover = asset.account_turnovers.first()
                balance_report = asset.balance_reports.first()
                sold_product_fee = asset.sold_product_fees.first()
                profit_loss_statement = asset.profit_loss_statements.first()

                if not balance_report or not profit_loss_statement or not sold_product_fee:
                    logger.warning("Missing data for asset %d", i + 1)

                self.process_balance_report(balance_report)

                self.process_profit_loss_statement(profit_loss_statement)

                self.process_sold_product_fee(sold_product_fee)

            self.process_ratios()
            logger.info("Finished processing financial assets successfully")

        except Exception as e:
            logger.error(
                "Error occurred while processing assets: %s", e, exc_info=True)
            return {'status': 'failed',
                    'data': {}}

    def process_balance_report(self, balance_report):
        """
        start balance report processing functions
        """
        logger.debug("Processing balance report data")

        current_asset_function(self, balance_report)
        non_current_asset_function(self, balance_report)
        total_asset_function(self, balance_report)
        current_debt_function(self, balance_report)
        non_current_debt_function(self, balance_report)
        total_debt_function(self, balance_report)
        ownership_right_total_function(self, balance_report)
        inventory_function(self, balance_report)
        net_sale_function(self, balance_report)
        net_profit_function(self, balance_report)
        accumulated_profit_function(self, balance_report)
        trade_payable_function(self, balance_report)
        advance_function(self, balance_report)
        reserves_function(self, balance_report)
        long_term_payable_function(self, balance_report)
        employee_termination_benefit_reserve_function(self, balance_report)

    def process_profit_loss_statement(self, profit_loss_statement):
        """
        start profit loss statement processing functions
        """
        logger.debug("Processing profit and loss statement data")

        operational_profit_function(self, profit_loss_statement)
        gross_profit_function(self, profit_loss_statement)
        proceed_profit_function(self, profit_loss_statement)
        salary_fee_function(self, profit_loss_statement)
        operational_income_expense_function(self, profit_loss_statement)
        marketing_fee_function(self, profit_loss_statement)

    def process_sold_product_fee(self, sold_product_fee):
        """
        start sold product fee processing functions
        """
        logger.debug("Processing sold product fee data")

        consuming_material_function(self, sold_product_fee)
        construction_overhead_function(self, sold_product_fee)
        production_total_price_function(self, sold_product_fee)
        sold_product_total_fee_function(self, sold_product_fee)
        direct_wage_function(self, sold_product_fee)

    def process_ratios(self):

        logger.debug("Processing financial ratios")

        usability_function(self)
        efficiency_function(self)
        roa_function(self)
        roab_function(self)
        roe_function(self)

        gross_profit_margin_ratio_function(self)
        net_profit_margin_ratio_function(self)
        debt_ratio_function(self)
        capital_ratio_function(self)
        total_debt_to_proceed_profit_ratio_function(self)
        current_debt_to_proceed_profit_ratio_function(self)
        properitary_ratio_function(self)
        equity_per_total_debt_ratio_function(self)
        current_ratio_function(self)
        instant_ratio_function(self)
        total_asset_turnover_ratio_function(self)
        salary_production_fee_function(self)
        capital_to_asset_ratio_function(self)
        accumulated_profit_to_asset_ratio_function(self)
        before_tax_profit_to_asset_ratio_function(self)
        sale_to_asset_ratio_function(self)
        equity_per_total_non_current_asset_ratio_function(self)
        altman_bankruptcy_ratio_function(self)
        equity_to_debt_ratio_function(self)
        total_sum_equity_debt_function(self)
        stock_turn_over_ratio_function(self)

        logger.info("Financial ratio calculations completed")

    def get_results(self):
        """ Return the final processed financial data """

        logger.info("Generating results for financial calculations")

        return {

            'status': 'success',
            'data': {
                'current_asset': self.balance_report_values["current_asset"],
                'non_current_asset': self.balance_report_values["non_current_asset"],
                'total_asset': self.balance_report_values["total_asset"],
                'current_debt': self.balance_report_values["current_debt"],
                'non_current_debt': self.balance_report_values["non_current_debt"],
                'total_debt': self.balance_report_values["total_debt"],
                'total_equity': self.balance_report_values["ownership_right_total"],
                'net_sale': self.balance_report_values["net_sale"],
                'inventory': self.balance_report_values["inventory"],
                'net_profit': self.balance_report_values["net_profit"],
                'trade_payable': self.balance_report_values["trade_payable"],
                'advance': self.balance_report_values["advance"],
                'reserves': self.balance_report_values["reserves"],
                'long_term_payable': self.balance_report_values["long_term_payable"],
                'employee_termination_benefit_reserve': self.balance_report_values["employee_termination_benefit_reserve"],

                'total_sum_equity_debt': self.total_sum_equity_debt,
                'gross_profit': self.profit_loss_statement_values["gross_profit"],
                'operational_income_expense': self.profit_loss_statement_values["operational_income_expense"],
                'marketing_fee': self.profit_loss_statement_values["marketing_fee"],
                'operational_profit': self.profit_loss_statement_values["operational_profit"],
                'proceed_profit': self.profit_loss_statement_values["proceed_profit"],
                'consuming_material': self.sold_product_values["consuming_material"],
                'production_fee': self.sold_product_values["direct_wage"],
                'construction_overhead': self.sold_product_values["construction_overhead"],
                'production_total_price': self.sold_product_values["production_total_price"],
                'salary_fee': self.profit_loss_statement_values["salary_fee"],
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


class ReadExcel:
    def __init__(self, file_path):
        self.file_path: Path = file_path
        self.is_tax: bool = False
        self.df: pd.DataFrame = None
        self.years: List[int] = list()
        self.months: List[int] = list()

        self.records: dict = {
            "balance": {"offset": 2, "length": 41},
            "profit_loss": {"offset": None, "length": 32},
            "sold_product": {"offset": None, "length": 13},
            "account_turnover": {"offset": None, "length": 20}
        }

        prev_offset = self.records["balance"]["offset"]
        for key in list(self.records.keys())[1:]:
            self.records[key]["offset"] = prev_offset + \
                self.records[key]["length"]
            prev_offset = self.records[key]["offset"]

        self.load_data()

    def load_data(self):
        """ Lazily loads the DataFrame when first accessed to improve efficiency. """
        if self.df is None:
            self.df = pd.read_excel(
                self.file_path, sheet_name="Sheet1", engine="openpyxl", header=None)
            self.df = self.df.iloc[1:, 1:].reset_index(drop=True)
            self.get_dates()
            if self.df.iloc[1].isnull().all():
                self.is_tax = True
                self.df.loc[1] = self.df.loc[1].fillna(-1)

            self.df.dropna(how="all", inplace=True)
            self.df.reset_index(drop=True, inplace=True)

    def get_dates(self):
        """ Retrieves the dates from the first row of the DataFrame. """
        self.years.extend(self.df.iloc[0].tolist())
        self.months.extend(self.df.iloc[1].tolist(
        ) if self.df.iloc[1] is not None else [])

    def get_record(self, record_name):
        """ Retrieves a record dynamically by name. """
        if record_name in self.records:
            offset = self.records[record_name]["offset"]
            length = self.records[record_name]["length"]
            return self.df.iloc[offset: offset + length]
        raise ValueError(f"Record '{record_name}' not found!")

    def get_balance_record(self):
        return self.get_record("balance")

    def get_profit_loss_record(self):
        return self.get_record("profit_loss")

    def get_sold_product_record(self):
        return self.get_record("sold_product")

    def get_account_turnover_record(self):
        return self.get_record("account_turnover")
