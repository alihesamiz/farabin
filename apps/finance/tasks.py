import logging
from pathlib import Path
from typing import List, Union

import requests
from celery import shared_task
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


from openai import OpenAI

from apps.company.models import CompanyProfile
from apps.finance.models import (
    AccountTurnOver,
    AnalysisReport,
    BalanceReport,
    FinancialAsset,
    FinancialData,
    ProfitLossStatement,
    SoldProductFee,
)
from apps.finance.services.utils import ReadExcel

logger = logging.getLogger("finance")


class CustomGenAIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def chat(self, model, messages):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": messages,
        }
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()


@shared_task(rate_limit="5/m")
def generate_analysis(company, chart_name, *args, **kwargs):
    logger.info(f"Starting analysis task for company {company}, chart {chart_name}")
    client = CustomGenAIClient(
        api_key=settings.FARABIN_GEMINI_API_KEY,
        base_url="https://api.metisai.ir/openai/v1",
    )

    charts: dict[str, dict[Union[str, List[float]]]] = {
        "sale": {
            "prompt": (
                "You are a senior financial analyst. Analyze the company's sales performance using the provided values for net sales, gross profit, operational income/expense, and marketing fee. "
                "Deliver a thorough, insightful, and data-driven assessment, highlighting key trends, strengths, weaknesses, and actionable recommendations. "
                "Present your analysis in clear, structured Persian markdown."
            ),
            "net_sale": [],
            "gross_profit": [],
            "operational_income_expense": [],
            "marketing_fee": [],
        },
        "debt": {
            "prompt": (
                "You are a senior financial analyst. Using the provided data for trade payables, advance payments, reserves, long-term payables, and employee termination benefit reserves, "
                "provide a comprehensive and insightful analysis of the company's debt situation. Discuss trends, risk factors, and offer actionable recommendations. "
                "Present your findings in clear, structured Persian markdown."
            ),
            "trade_payable": [],
            "advance": [],
            "reserves": [],
            "long_term_payable": [],
            # "long_term_financial": [],
            "employee_termination_benefit_reserve": [],
        },
        "asset": {
            "prompt": (
                "You are a senior financial analyst. Analyze the company's asset performance using the provided values for current assets, non-current assets, inventory average, and total assets. "
                "Deliver a detailed, insightful, and data-driven assessment, highlighting key trends, strengths, weaknesses, and actionable recommendations. "
                "Present your analysis in clear, structured Persian markdown."
            ),
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
            "prompt": (
                "You are a senior financial analyst. Using the provided values for gross profit, operational profit, proceed profit, and net profit, "
                "provide a comprehensive, insightful, and data-driven analysis of the company's profitability. Highlight key trends, strengths, weaknesses, and offer actionable recommendations. "
                "Present your findings in clear, structured Persian markdown."
            ),
            "gross_profit": [],
            "operational_profit": [],
            "proceed_profit": [],
            "net_profit": [],
        },
        "cost": {
            "prompt": (
                "You are a senior financial analyst. Analyze the company's cost structure using the provided data for consuming material, production fee, construction overhead, production total price, salary fee, and salary production fee. "
                "Deliver a detailed, insightful, and data-driven assessment, highlighting cost trends, efficiency, and areas for improvement. "
                "Present your analysis in clear, structured Persian markdown."
            ),
            "consuming_material": [],
            "production_fee": [],
            "construction_overhead": [],
            "production_total_price": [],
            "salary_fee": [],
            "salary_production_fee": [],
        },
        "equity": {
            "prompt": (
                "You are a senior financial analyst. Using the provided values for total debt, total equity, and total sum of equity and debt, "
                "provide a comprehensive, insightful, and data-driven analysis of the company's equity position. Discuss trends, capital structure, and offer actionable recommendations. "
                "Present your findings in clear, structured Persian markdown."
            ),
            "total_debt": [],
            "total_equity": [],
            "total_sum_equity_debt": [],
        },
        "bankrupsy": {
            "prompt": (
                "You are a senior financial analyst. Analyze the company's bankruptcy risk using the provided Altman bankruptcy ratio values. "
                "Deliver a thorough, insightful, and data-driven assessment, highlighting risk factors, trends, and recommendations for risk mitigation. "
                "Present your analysis in clear, structured Persian markdown."
            ),
            "altman_bankrupsy_ratio": [],
        },
        "profitability": {
            "prompt": (
                "You are a senior financial analyst. Using the provided values for efficiency, ROA, ROAB, ROE, gross profit margin, and profit margin ratio, "
                "provide a comprehensive, insightful, and data-driven analysis of the company's profitability. Highlight key trends, strengths, weaknesses, and offer actionable recommendations. "
                "Present your findings in clear, structured Persian markdown."
            ),
            "efficiency": [],
            "roa": [],
            "roab": [],
            "roe": [],
            "gross_profit_margin": [],
            "profit_margin_ratio": [],
        },
        "salary": {
            "prompt": (
                "You are a senior financial analyst. Analyze the company's salary and wage performance using the provided data for construction overhead, production total price, salary fee, and salary production fee. "
                "Deliver a detailed, insightful, and data-driven assessment, highlighting trends, efficiency, and areas for improvement. "
                "Present your analysis in clear, structured Persian markdown."
            ),
            "construction_overhead": [],
            "production_total_price": [],
            "salary_fee": [],
            "salary_production_fee": [],
        },
        "inventory": {
            "prompt": (
                "You are a senior financial analyst. Using the provided inventory average values, provide a comprehensive, insightful, and data-driven analysis of the company's inventory management and performance. "
                "Highlight key trends, strengths, weaknesses, and offer actionable recommendations. "
                "Present your findings in clear, structured Persian markdown."
            ),
            "inventory_average": [],
        },
        "agility": {
            "prompt": (
                "You are a senior financial analyst. Analyze the company's agility using the provided instant ratio and stock turnover values. "
                "Deliver a thorough, insightful, and data-driven assessment, highlighting operational flexibility, trends, and recommendations for improvement. "
                "Present your analysis in clear, structured Persian markdown."
            ),
            "instant_ratio": [],
            "stock_turnover": [],
        },
        "liquidity": {
            "prompt": (
                "You are a senior financial analyst. Using the provided instant ratio and current ratio values, provide a comprehensive, insightful, and data-driven analysis of the company's liquidity position. "
                "Highlight key trends, strengths, weaknesses, and offer actionable recommendations. "
                "Present your findings in clear, structured Persian markdown."
            ),
            "instant_ratio": [],
            "current_ratio": [],
        },
        "leverage": {
            "prompt": (
                "You are a senior financial analyst. Analyze the company's leverage using the provided values for debt ratio, capital ratio, proprietary ratio, equity per total debt ratio, and equity per total non-current asset ratio. "
                "Deliver a detailed, insightful, and data-driven assessment, highlighting risk, capital structure, and recommendations for improvement. "
                "Present your analysis in clear, structured Persian markdown."
            ),
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
        formatted_prompt = charts[chart_name]["prompt"]
        for field in charts[chart_name]:
            if field != "prompt":
                formatted_prompt += "\n\nData:\n" + (
                    f"{field}: {charts[chart_name][field]}"
                )

        logger.info(
            f"Sending request to Cohere API for company {company}, chart {chart_name}"
        )
        response = (
            client.chat(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful, expert financial analyst, you only response in persian structured markdown",
                    },
                    {"role": "user", "content": formatted_prompt},
                ],
            )
            .get("choices", [{}])[0]
            .get("message", "")["content"]
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
        return f"Error: An unexpected issue occurred during analysis.{e}"


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
