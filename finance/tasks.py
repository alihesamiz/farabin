from company.models import CompanyProfile
from pathlib import Path
from typing import List, Union
from celery import shared_task
import logging
import cohere

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from finance.models import (
    AnalysisReport,
    FinancialData,
    BalanceReport,
    AccountTurnOver,
    SoldProductFee,
    FinancialAsset,
    ProfitLossStatement,
)
from finance.utils import ReadExcel

logger = logging.getLogger("finance")


@shared_task(rate_limit="5/m")
def generate_analysis(company, chart_name, *args, **kwargs):
    logger.info(f"Starting analysis task for company {company}, chart {chart_name}")

    generator = cohere.ClientV2(settings.FARABIN_COHERE_API_KEY)

    charts: dict[str, dict[Union[str, List[float]]]] = {
        "sale": {
            "prompt": "Using the provided net sales, gross profit,operational income expense and marketing fee values, provide a comprehensive analysis of the company's sales performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "net_sale": [],
            "gross_profit": [],
            "operational_income_expense": [],
            "marketing_fee": [],
        },
        "debt": {
            "prompt": "Using the provided trade payable ,advance payment, reserves, long term payable, employee termination benefit reserve  values, provide a comprehensive analysis of the company's debts performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "trade_payable": [],
            "advance": [],
            "reserves": [],
            "long_term_payable": [],
            # "long_term_financial": [],
            "employee_termination_benefit_reserve": [],
        },
        "asset": {
            # "prompt": "Using the provided cash balance ,trade receivable, inventory, property investment, intangible asset, long term investment values, provide a comprehensive analysis of the company's assets performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "prompt": "Using the provided current asset ,non-current asset, inventory average, total assetvalues, provide a comprehensive analysis of the company's assets performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            # "cash_balance": [],
            # "trade_receivable": [],
            # "property_investment": [],
            # "intangible_asset": [],
            # "long_term_investment": [],
            "inventory_average": [],
            "current_asset": [],
            "non_current_asset": [],
            "total_asset": [],
        },
        "profit": {
            "prompt": "Using the provided gross_profit operational profit, proceed profit, net profit values, provide a comprehensive analysis of the company's profit performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "gross_profit": [],
            "operational_profit": [],
            "proceed_profit": [],
            "net_profit": [],
        },
        "cost": {
            "prompt": "Using the provided consuming_material ,production fee ,construction overhead ,production total price ,salary fee ,salary production fee values, provide a comprehensive analysis of the company's cost performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "consuming_material": [],
            "production_fee": [],
            "construction_overhead": [],
            "production_total_price": [],
            "salary_fee": [],
            "salary_production_fee": [],
        },
        "equity": {
            "prompt": "Using the provided total debt ,total equity ,total sum equity debt values, provide a comprehensive analysis of the company's equity performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "total_debt": [],
            "total_equity": [],
            "total_sum_equity_debt": [],
        },
        "bankrupsy": {
            "prompt": "Using the provided altman bankrupsy ratio values, provide a comprehensive analysis of the company's bankruptcy rate performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "altman_bankrupsy_ratio": [],
        },
        "profitability": {
            "prompt": "Using the provided efficiency ,roa ,roab ,roe ,gross profit margin ,profit margin ratio values, provide a comprehensive analysis of the company's profitability performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "efficiency": [],
            "roa": [],
            "roab": [],
            "roe": [],
            "gross_profit_margin": [],
            "profit_margin_ratio": [],
        },
        "salary": {
            "prompt": "Using the provided construction overhead ,production total price ,salary fee ,salary production fee values, provide a comprehensive analysis of the company's salary performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "construction_overhead": [],
            "production_total_price": [],
            "salary_fee": [],
            "salary_production_fee": [],
        },
        "inventory": {
            "prompt": "Using the provided invenrotry average values, provide a comprehensive analysis of the company's inventory performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "inventory_average": [],
        },
        "agility": {
            "prompt": "Using the provided instant ratio, stock turnover values, provide a comprehensive analysis of the company's agility rate performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "instant_ratio": [],
            "stock_turnover": [],
        },
        "liquidity": {
            "prompt": "Using the provided instant ratio, current ratio values, provide a comprehensive analysis of the company's liquidity rate performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "instant_ratio": [],
            "current_ratio": [],
        },
        "leverage": {
            "prompt": "Using the provided debt_ratio ,capital ratio ,proprietary ratio ,equity per total debt ratio ,equity per total non current asset ratio values, provide a comprehensive analysis of the company's leverage rate performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "debt_ratio": [],
            "capital_ratio": [],
            "proprietary_ratio": [],
            "equity_per_total_debt_ratio": [],
            "equity_per_total_non_current_asset_ratio": [],
        },
    }

    try:
        data = (
            FinancialData.objects.prefetch_related("financial_asset")
            .filter(financial_asset__company__id=company)
            .order_by("financial_asset__year", "financial_asset__month")
        )

        if not data.exists():
            logger.warning(f"No financial data found for company {company}.")
            return "No financial data available for analysis."

        last_data = data.last()
        logger.info(f"Fetched {data.count()} records for company {company}.")

        for field in charts[chart_name]:
            if field != "prompt":
                for values in data:
                    charts[chart_name][field].append(float(getattr(values, field)))
        formatted_prompt = (
            "act as a professional financial management and analyst and"
            + charts[chart_name]["prompt"]
        )
        for field in charts[chart_name]:
            if field != "prompt":
                formatted_prompt += "\n\nData:\n" + (
                    f"{field}: {charts[chart_name][field]}"
                )

        logger.info(
            f"Sending request to Cohere API for company {company}, chart {chart_name}"
        )

        response = (
            generator.chat(
                model="command-r-plus",
                messages=[{"role": "user", "content": f"{formatted_prompt}"}],
            )
            .message.content[0]
            .text
        )

        response = (
            generator.chat(
                model="command-r-plus",
                messages=[
                    {
                        "role": "user",
                        "content": f"fix any issues in the following persian text. also check and fix if there are any grammaricall issues: {response}",
                    }
                ],
            )
            .message.content[0]
            .text
        )

        logger.info(f"Received AI response for company {company}, chart {chart_name}")

        AnalysisReport.objects.update_or_create(
            calculated_data=last_data,
            chart_name=chart_name,
            defaults={
                "period": "y" if last_data.financial_asset.is_tax_record else "m",
                "text": response,
            },
        )
        logger.info(
            f"Successfully saved analysis report for company {company}, chart {chart_name}"
        )

    except ObjectDoesNotExist as e:
        logger.error(
            f"Error: Financial asset data not found for company {company}. Exception: {e}"
        )
        return "Error: Financial asset data not found."

    except Exception as e:
        logger.error(
            f"Unexpected error in analysis task for company {company}, chart {chart_name}: {e}"
        )
        return "Error: An unexpected issue occurred during analysis."


@shared_task
def generate_financial_asset(company_id, file_path):
    reader = ReadExcel(Path(file_path))
    company = CompanyProfile.objects.get(id=company_id)
    years = reader.years
    is_tax = reader.is_tax
    months = reader.months

    for year in years:
        if not all(
            isinstance(x, float) and x != x for x in months
        ):  # NaN is never equal to itself
            print(months)
        financial_asset, created = FinancialAsset.objects.update_or_create(
            company=company, year=year, is_tax_record=is_tax
        )

        profit_loss_df = reader.get_profit_loss_record().T
        populate_financial_model(ProfitLossStatement, financial_asset, profit_loss_df)

        # Populate BalanceReport
        balance_df = reader.get_balance_record().T
        populate_financial_model(BalanceReport, financial_asset, balance_df)

        # Populate AccountTurnOver
        account_turnover_df = reader.get_account_turnover_record().T
        populate_financial_model(AccountTurnOver, financial_asset, account_turnover_df)

        # Populate SoldProductFee
        sold_product_df = reader.get_sold_product_record().T
        populate_financial_model(SoldProductFee, financial_asset, sold_product_df)


def populate_financial_model(model_class, financial_asset, df):
    """
    Dynamically populate financial models based on the DataFrame columns.

    Args:
        model_class: The Django model class to populate.
        financial_asset: The related FinancialAsset object.
        df: The pandas DataFrame containing financial data.

    Returns:
        None
    """
    fields = [
        field.name
        for field in model_class._meta.fields
        if field.name != "id" and field.name != "financial_asset"
    ]

    for index, row in df.iterrows():
        data = {field: value or 0 for field, value in zip(fields, row)}
        model_class.objects.update_or_create(
            financial_asset=financial_asset, defaults=data
        )
