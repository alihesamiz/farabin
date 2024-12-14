from celery import shared_task
import numpy as np
from company.models import CompanyProfile
from diagnostics.models import FinancialData, FinancialAsset
from .utils import get_life_cycle, FinancialCalculations


@shared_task
def perform_calculations(financial_asset_ids, company_id):

    financial_assets = FinancialAsset.objects\
        .filter(id__in=financial_asset_ids)\
        .prefetch_related('account_turnovers',
                          'balance_reports',
                          'profit_loss_statements',
                          'sold_product_fees')\
        .order_by('year', 'month')
    financial_calculator = FinancialCalculations(financial_assets)
    financial_calculator.process_assets()
    results = financial_calculator.get_results()
    
