from.utils.balance_sheet_ecxel_reader import read_balance_sheet_excel
from.utils.balance_sheet_json_insert import insert_balance_sheet_data
from celery import shared_task

import logging
logger = logging.getLogger(__name__)





# @shared_task
def analyze_balance_sheet(file_path, company_id, year):
    balance_sheet_json = read_balance_sheet_excel(file_path)
    logger.info("Parsed balance sheet JSON: %s", balance_sheet_json)

    try:
        bs = insert_balance_sheet_data(balance_sheet_json, company_id=company_id, year=year)
        logger.info("Inserted BalanceSheet ID %s", bs.id)
        return f"Inserted BalanceSheet ID {bs.id}"
    
    except Exception as e:
        logger.error("Error inserting balance sheet: %s", e, exc_info=True)
        return f"Error inserting balance sheet: {e}"