from celery import shared_task
# from pydantic import BaseModel
from typing import List, Union
from diagnostics.models import AnalysisReport, FinancialData
import cohere
from openai import OpenAI


@shared_task
def generate_analysis(company, chart_name, *args, **kwargs):
    COHERE_KEY = "Y95P8wDUR9q4Iw7agGIZQSNl4Ip5zEgpja3Mkwqr"
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
            "prompt": "Using the provided trade payable ,advance payment, reserves, long term payable, employee termination benefit reserve  values, provide a comprehensive analysis of the company's sales performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "trade_payable": [],
            "advance": [],
            "reserves": [],
            "long_term_payable": [],
            # "long_term_financial": [],
            "employee_termination_benefit_reserve": [],
        },
        "asset": {
            "prompt": "Using the provided cash balance ,trade receivable, inventory, property investment, intangible asset, long term investment values, provide a comprehensive analysis of the company's sales performance.Ensure the analysis is detailed, insightful, and highlights key trends and observations then translate the results to persian",
            "cash_balance": [],
            "trade_receivable": [],
            "inventory": [],
            "property_investment": [],
            "intangible_asset": [],
            "long_term_investment": [],
        }
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

    AnalysisReport.objects.update_or_create(
        calculated_data=last_data,
        chart_name=chart_name,
        defaults={
            "period": "y" if last_data.financial_asset.is_tax_record else "m",
            "text": response,
        }
    )
