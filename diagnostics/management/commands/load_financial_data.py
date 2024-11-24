import random
from company.models import CompanyProfile
from diagnostics.models import FinancialData, FinancialAsset
from django.core.management.base import BaseCommand
from django.db import transaction
from django_seed import Seed
from typing import Any


class Command(BaseCommand):
    help = "Create some random data for financial charts"

    def add_arguments(self, parser):
        parser.add_argument('--asset', type=int, default=10,
                            help='Number of records to create')

        parser.add_argument('--number', type=int, default=10,
                            help='Number of records to create')

    def handle(self, *args: Any, **options: Any) -> str | None:
        financial_data_seeder = Seed.seeder()
        financial_asset_seeder = Seed.seeder()
        asset = options.get('asset', 1)
        number = options.get('number', 1)
        companies = CompanyProfile.objects.all()
        with transaction.atomic():
            try:
                """consuming_material
production_fee
construction_overhead
production_total_price
current_constructing_product_first_period_inventory
current_constructing_product_end_period_inventory
produced_product_total_price
first_period_produced_inventory
period_bought_product
ready_for_sale_product
end_period_inventory
product_other
sold_product_total_price
operational_income
operational_income_expense
gross_profit
salary_fee
marketing_fee
doubtful_burnt_claims_fee
attendance_fee
accounting_fee
consulting_fee
rental_fee
other_general_expense
total_general_expense
other_operation_income
other_operational_expense
operational_profit
immovable_property_sale_profit
other_assets_sale_profit
material_sale_profit
investment_sale_profit
interpretation_profit
dividend_profit
investment_profit
bank_deposit_profit
rental_income
incidental_income
other_non_operationl_income_expense
net_value_other_non_operationl_income_expense
financial_expense
proceed_profit
current_year_income_tax
prev_year_income_tax
profit_after_tax
advance_payment
inventory
trade_receivable
short_term_investment
cash_balance
held_non_current_asset
current_shareholder_asset
total_current_asset
tangible_fixed_asset
property_investment
intangible_asset
long_term_investment
long_term_receivable
other_asset
total_non_current_asset
capital
capital_increase
share_spend
treasury_share_spend
legal_reserve
other_reserve
revaluation_surplus
accumulated_profit_loss
treasury_share
ownership_right_total
trade_payable
paid_tax
dividend_payable
financial_facility
reserves
advance
held_for_sale_liability
current_shareholder_debt
total_current_debt
long_term_payable
long_term_financial
employee_termination_benefit_reserve
total_non_current_debt
net_sale
net_profit
profit_after_tax
first_year_accumulated_profit
correcting_mistake
accounting_method_change
first_year_accumulated_profit_balanced
transfer_from_reserve
other_account_turnover
allocable_profit
share_profit
legal_reserve
wealth_increase
current_wealt_increase
other_reserves
treasury_share_purchase
treasury_share_sale
treasury_share_sale_profit
board_reward
other_profit
total_allocated_profit
end_year_accumulated_profit"""
                financial_asset_seeder.add_entity(FinancialAsset, asset, {
                    'company': lambda x: random.choice(companies),
                    'year': lambda x: random.randint(1399, 1410),
                    'month': lambda x: random.choice([None, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
                })
                financial_asset_seeder.execute()
                self.stdout.write(self.style.SUCCESS(
                    f"Successfully created {asset} financial asset records."))
                financial_assets = FinancialAsset.objects.all()
            except Exception as e:
                self.stderr.write(self.style.ERROR(
                    f"Error creating financial data records: {str(e)}"))

            try:
                financial_data_seeder.add_entity(FinancialData, number, {
                    'financial_asset': lambda x: random.choice(financial_assets),
                    'current_asset': lambda x: random.randint(1000, 1000000),
                    'non_current_asset': lambda x: random.randint(1000, 1000000),
                    'total_asset': lambda x: random.randint(1000, 2000000),
                    'current_debt': lambda x: random.randint(500, 500000),
                    'non_current_debt': lambda x: random.randint(500, 500000),
                    'total_debt': lambda x: random.randint(500, 1000000),
                    'total_equity': lambda x: random.randint(1000, 1000000),
                    'total_sum_equity_debt': lambda x: random.randint(1000, 2000000),
                    'gross_profit': lambda x: random.randint(500, 500000),
                    'net_sale': lambda x: random.randint(1000, 1000000),
                    "inventory": lambda x: random.randint(1000, 100000),
                    "operational_profit": lambda x: random.randint(1000, 100000),
                    "proceed_profit": lambda x: random.randint(1000, 100000),
                    "net_profit": lambda x: random.randint(1000, 100000),
                    "consuming_material": lambda x: random.randint(1000, 100000),
                    "production_fee": lambda x: random.randint(1000, 100000),
                    "construction_overhead": lambda x: random.randint(1000, 100000),
                    "production_total_price": lambda x: random.randint(1000, 100000),
                    "salary_fee": lambda x: random.randint(1000, 100000),
                    "salary_production_fee": lambda x: random.randint(1000, 100000),
                    "usability": lambda x: random.randint(1000, 100000),
                    "efficiency": lambda x: random.randint(1000, 100000),
                    "roa": lambda x: random.randint(1000, 100000),
                    "roab": lambda x: random.randint(1000, 100000),
                    "roe": lambda x: random.randint(1000, 100000),
                    "gross_profit_margin": lambda x: random.randint(1000, 100000),
                    "profit_margin_ratio": lambda x: random.randint(1000, 100000),
                    "debt_ratio": lambda x: random.randint(1000, 100000),
                    "capital_ratio": lambda x: random.randint(1000, 100000),
                    "proprietary_ratio": lambda x: random.randint(1000, 100000),
                    "equity_per_total_debt_ratio": lambda x: random.randint(1000, 100000),
                    "equity_per_total_non_current_asset_ratio": lambda x: random.randint(1000, 100000),
                    "current_ratio": lambda x: random.randint(1000, 100000),
                    "instant_ratio": lambda x: random.randint(1000, 100000),
                    "stock_turnover": lambda x: random.randint(1000, 100000),
                    "altman_bankrupsy_ratio": lambda x: random.randint(0, 4),
                    # Add more fields as needed, using similar patterns
                })
                financial_data_seeder.execute()
                self.stdout.write(self.style.SUCCESS(
                    f"Successfully created {number} financial data records."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(
                    f"Error creating financial data records: {str(e)}"))
