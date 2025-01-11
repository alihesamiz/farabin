from celery import shared_task
# from pydantic import BaseModel
from typing import List, Union
from diagnostics.models import AnalysisReport, FinancialData
import cohere
from openai import OpenAI


@shared_task(rate_limit='9/m') 
def generate_analysis(company, chart_name, *args, **kwargs):
    COHERE_KEY = "BMzAnLb3lWY2Pkj4UqIh3n3tUZt8fiTIw2v5AdVF"
    generator = cohere.ClientV2(COHERE_KEY)  # Synchronous client for tasks

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
            "net_profit": [], },
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

            "altman_bankrupsy_ratio": []
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

    data = FinancialData.objects.prefetch_related("financial_asset").filter(
        financial_asset__company__id=company).order_by("financial_asset__year", "financial_asset__month").all()
    last_data = data.last()
    for field in charts[chart_name]:
        if field != "prompt":
            for values in data:
                charts[chart_name][field].append(float(getattr(values, field)))
    formatted_prompt = "act as a professional financial management and analyst and" + \
        charts[chart_name]["prompt"]
    for field in charts[chart_name]:
        if field != "prompt":
            formatted_prompt += "\n\nData:\n" + (f"{field}: {charts[chart_name][field]}"
                                                 )

    response = generator.chat(
        model="command-r-plus",
        messages=[
            {
                "role": "user",
                "content": f"{formatted_prompt}"}],
    ).message.content[0].text
    print(response)

    AnalysisReport.objects.update_or_create(
        calculated_data=last_data,
        chart_name=chart_name,
        defaults={
            "period": "y" if last_data.financial_asset.is_tax_record else "m",
            "text": response,
        }
    )
