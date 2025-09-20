from django.db import transaction
from apps.company.models import CompanyProfile

from apps.balancesheet.models.balance_sheet import BalanceSheet
from apps.balancesheet.models.contingent_account import (
    ContingentAccount,
    ContingentAccounts,
    ContingentCounterparties,
)
from apps.balancesheet.models.current_liability import (
    CurrentLiability,
    TradeAccountsPayable,
    NonTradeAccountsPayable,
    ShareholderPayables,
    DividendsPayable,
    ShortTermLoans,
    AdvancesAndDeposits,
    LiabilitiesRelatedToAssetsHeldForSale,
    TaxProvision,
    TaxPayable,
)

from apps.balancesheet.models.current_asset import (
    CurrentAsset,
    Cash,
    ShortTermInvestment,
    TradeReceivable,
    NonTradeReceivable,
    ShareholderReceivable,
    Inventory,
    OrdersAndPrepayments,
    AssetsHeldForSale,
)
from apps.balancesheet.models.long_term_liability import (
    LongTermLiability,
    LongTermAccountsPayable,
    LongTermLoans,
    LongTermProvisions,
)

from apps.balancesheet.models.equity import (
    Equity,
    InitialCapital,
    CapitalIncreaseDecrease,
    SharePremiumReserve,
    ShareDiscountReserve,
    LegalReserve,
    OtherReserves,
    RevaluationSurplus,
    ForeignCurrencyTranslationDifference,
    RetainedEarnings,
)

from apps.balancesheet.models.expense import (
    Expense,
    ProductionCosts,
    DistributionAndMarketingCosts,
    GeneralAndAdministrativeCosts,
    FinancialCosts,
    OtherOperatingCosts,
)

from apps.balancesheet.models.fixed_asset import (
    FixedAsset,
    IntangibleAsset,
    TangibleFixedAsset,
    AssetsInProgress,
    LongTermInvestment,
    OtherNonCurrentAsset,
)

from apps.balancesheet.models.revenue import (
    Revenue,
    NetSales,
    ServiceRevenue,
    ForeignCurrencyRevenue,
    OtherOperatingRevenue,
)




def insert_balance_sheet_data(json_data, company_id, year):
    with transaction.atomic():
        # Get the CompanyProfile instance
        try:
            company = CompanyProfile.objects.get(id=company_id)
        except CompanyProfile.DoesNotExist:
            raise ValueError(f"Company with ID {company_id} does not exist")

        # Create a new BalanceSheet instance
        balance_sheet = BalanceSheet.objects.create(company=company, year=year)

        # Parse the JSON data
        balance_sheet_data = json_data.get('BalanceSheet', {})

        # Helper function to create JSON field
        def create_json_field(account_data):
            return {"type": account_data["type"], "amount": int(account_data["amount"])}

        # CurrentAsset
        current_asset_data = balance_sheet_data.get('CurrentAsset', {})
        current_asset = CurrentAsset.objects.create(balance_sheet=balance_sheet)

        # Cash
        cash_data = current_asset_data.get('Cash', {})
        Cash.objects.create(
            current_asset=current_asset,
            cash_in_hand=create_json_field(cash_data.get('cash_in_hand', {})),
            bank_balances=create_json_field(cash_data.get('bank_balances', {})),
            petty_cash=create_json_field(cash_data.get('petty_cash', {})),
            cash_in_transit=create_json_field(cash_data.get('cash_in_transit', {}))
        )

        # ShortTermInvestment
        sti_data = current_asset_data.get('ShortTermInvestment', {})
        ShortTermInvestment.objects.create(
            current_asset=current_asset,
            short_term_deposits=create_json_field(sti_data.get('short_term_deposits', {})),
            tradable_stocks=create_json_field(sti_data.get('tradable_stocks', {})),
            participation_bonds=create_json_field(sti_data.get('participation_bonds', {})),
            etf_investment_fund=create_json_field(sti_data.get('etf_investment_fund', {})),
            other_short_term_investments=create_json_field(sti_data.get('other_short_term_investments', {})),
            short_term_investment_impairment=create_json_field(sti_data.get('short_term_investment_impairment', {}))
        )

        # TradeReceivable
        tr_data = current_asset_data.get('TradeReceivable', {})
        TradeReceivable.objects.create(
            current_asset=current_asset,
            trade_accounts_receivable=create_json_field(tr_data.get('trade_accounts_receivable', {})),
            trade_notes_receivable=create_json_field(tr_data.get('trade_notes_receivable', {})),
            receivables_in_litigation=create_json_field(tr_data.get('receivables_in_litigation', {})),
            notes_in_collection=create_json_field(tr_data.get('notes_in_collection', {})),
            returned_cheques=create_json_field(tr_data.get('returned_cheques', {})),
            doubtful_receivables_provision=create_json_field(tr_data.get('doubtful_receivables_provision', {}))
        )

        # NonTradeReceivable
        ntr_data = current_asset_data.get('NonTradeReceivable', {})
        NonTradeReceivable.objects.create(
            current_asset=current_asset,
            non_trade_accounts_receivable=create_json_field(ntr_data.get('non_trade_accounts_receivable', {})),
            non_trade_notes_receivable=create_json_field(ntr_data.get('non_trade_notes_receivable', {})),
            employee_receivables=create_json_field(ntr_data.get('employee_receivables', {})),
            director_receivables=create_json_field(ntr_data.get('director_receivables', {})),
            related_companies_receivables=create_json_field(ntr_data.get('related_companies_receivables', {})),
            vat_receivable=create_json_field(ntr_data.get('vat_receivable', {})),
            deposits_with_others=create_json_field(ntr_data.get('deposits_with_others', {})),
            dividends_receivable=create_json_field(ntr_data.get('dividends_receivable', {}))
        )

        # ShareholderReceivable
        sr_data = current_asset_data.get('ShareholderReceivable', {})
        ShareholderReceivable.objects.create(
            current_asset=current_asset,
            amount=create_json_field(sr_data.get('shareholder_payables', {}))
        )

        # Inventory
        inv_data = current_asset_data.get('Inventory', {})
        Inventory.objects.create(
            current_asset=current_asset,
            raw_materials=create_json_field(inv_data.get('raw_materials', {})),
            work_in_progress=create_json_field(inv_data.get('work_in_progress', {})),
            finished_goods=create_json_field(inv_data.get('finished_goods', {})),
            purchased_goods_for_sale=create_json_field(inv_data.get('purchased_goods_for_sale', {})),
            spare_parts=create_json_field(inv_data.get('spare_parts', {})),
            packaging_materials=create_json_field(inv_data.get('packaging_materials', {})),
            consignment_goods_with_others=create_json_field(inv_data.get('consignment_goods_with_others', {})),
            idle_items=create_json_field(inv_data.get('idle_items', {})),
            scrap_raw_materials=create_json_field(inv_data.get('scrap_raw_materials', {})),
            inventory_impairment=create_json_field(inv_data.get('inventory_impairment', {}))
        )

        # OrdersAndPrepayments
        op_data = current_asset_data.get('OrdersAndPrepayments', {})
        OrdersAndPrepayments.objects.create(
            current_asset=current_asset,
            prepaid_goods_and_services=create_json_field(op_data.get('prepaid_goods_and_services', {})),
            prepaid_income_tax=create_json_field(op_data.get('prepaid_income_tax', {})),
            prepaid_rent=create_json_field(op_data.get('prepaid_rent', {})),
            prepaid_insurance=create_json_field(op_data.get('prepaid_insurance', {})),
            orders_in_transit=create_json_field(op_data.get('orders_in_transit', {})),
            prepaid_loans=create_json_field(op_data.get('prepaid_loans', {})),
            prepaid_interest_on_loans=create_json_field(op_data.get('prepaid_interest_on_loans', {})),
            other_prepayments=create_json_field(op_data.get('other_prepayments', {}))
        )

        # AssetsHeldForSale
        ahfs_data = current_asset_data.get('AssetsHeldForSale', {})
        AssetsHeldForSale.objects.create(
            current_asset=current_asset,
            assets_held_for_sale=create_json_field(ahfs_data.get('assets_held_for_sale', {})),
            impairment_reserve=create_json_field(ahfs_data.get('impairment_reserve', {}))
        )

        # FixedAsset
        fixed_asset_data = balance_sheet_data.get('FixedAsset', {})
        fixed_asset = FixedAsset.objects.create(balance_sheet=balance_sheet)

        # IntangibleAsset
        ia_data = fixed_asset_data.get('IntangibleAsset', {})
        IntangibleAsset.objects.create(
            fixed_asset=fixed_asset,
            software=create_json_field(ia_data.get('software', {})),
            royalty=create_json_field(ia_data.get('royalty', {})),
            goodwill=create_json_field(ia_data.get('goodwill', {})),
            patent=create_json_field(ia_data.get('patent', {})),
            trademark=create_json_field(ia_data.get('trademark', {})),
            copyright=create_json_field(ia_data.get('copyright', {})),
            pre_operating_expenses=create_json_field(ia_data.get('pre_operating_expenses', {}))
        )

        # TangibleFixedAsset
        tfa_data = fixed_asset_data.get('TangibleFixedAsset', {})
        TangibleFixedAsset.objects.create(
            fixed_asset=fixed_asset,
            land=create_json_field(tfa_data.get('land', {})),
            building=create_json_field(tfa_data.get('building', {})),
            installations=create_json_field(tfa_data.get('installations', {})),
            machinery_and_equipment=create_json_field(tfa_data.get('machinery_and_equipment', {})),
            vehicles=create_json_field(tfa_data.get('vehicles', {})),
            office_furniture=create_json_field(tfa_data.get('office_furniture', {})),
            accumulated_depreciation=create_json_field(tfa_data.get('accumulated_depreciation', {}))
        )

        # AssetsInProgress
        aip_data = fixed_asset_data.get('AssetsInProgress', {})
        AssetsInProgress.objects.create(
            fixed_asset=fixed_asset,
            amount=create_json_field(aip_data.get('assets_in_progress', {}))
        )

        # LongTermInvestment
        lti_data = fixed_asset_data.get('LongTermInvestment', {})
        LongTermInvestment.objects.create(
            fixed_asset=fixed_asset,
            investment_in_affiliates=create_json_field(lti_data.get('investment_in_affiliates', {})),
            investment_in_subsidiaries=create_json_field(lti_data.get('investment_in_subsidiaries', {})),
            investment_in_private_companies=create_json_field(lti_data.get('investment_in_private_companies', {})),
            long_term_bonds=create_json_field(lti_data.get('long_term_bonds', {})),
            property_investment=create_json_field(lti_data.get('property_investment', {})),
            long_term_deposits=create_json_field(lti_data.get('long_term_deposits', {})),
            long_term_participation_in_projects=create_json_field(lti_data.get('long_term_participation_in_projects', {})),
            long_term_treasury_investment=create_json_field(lti_data.get('long_term_treasury_investment', {})),
            long_term_investment_impairment=create_json_field(lti_data.get('long_term_investment_impairment', {}))
        )

        # OtherNonCurrentAsset
        onca_data = fixed_asset_data.get('OtherNonCurrentAsset', {})
        OtherNonCurrentAsset.objects.create(
            fixed_asset=fixed_asset,
            amount=create_json_field(onca_data.get('other_non_current_assets', {}))
        )

        # CurrentLiability
        current_liability_data = balance_sheet_data.get('CurrentLiability', {})
        current_liability = CurrentLiability.objects.create(balance_sheet=balance_sheet)

        # TradeAccountsPayable
        tap_data = current_liability_data.get('TradeAccountsPayable', {})
        TradeAccountsPayable.objects.create(
            current_liability=current_liability,
            domestic_suppliers=create_json_field(tap_data.get('domestic_suppliers', {})),
            foreign_suppliers=create_json_field(tap_data.get('foreign_suppliers', {}))
        )

        # NonTradeAccountsPayable
        ntap_data = current_liability_data.get('NonTradeAccountsPayable', {})
        NonTradeAccountsPayable.objects.create(
            current_liability=current_liability,
            salaries_payable=create_json_field(ntap_data.get('salaries_payable', {})),
            social_security_payable=create_json_field(ntap_data.get('social_security_payable', {})),
            deposits_from_entities=create_json_field(ntap_data.get('deposits_from_entities', {})),
            deposits_from_individuals=create_json_field(ntap_data.get('deposits_from_individuals', {})),
            accrued_unpaid_expenses_provision=create_json_field(ntap_data.get('accrued_unpaid_expenses_provision', {}))
        )

        # ShareholderPayables
        sp_data = current_liability_data.get('ShareholderPayables', {})
        ShareholderPayables.objects.create(
            current_liability=current_liability,
            amount=create_json_field(sp_data.get('shareholder_payables', {}))
        )

        # DividendsPayable
        dp_data = current_liability_data.get('DividendsPayable', {})
        DividendsPayable.objects.create(
            current_liability=current_liability,
            dividends_payable_to_individuals=create_json_field(dp_data.get('dividends_payable_to_individuals', {})),
            dividends_payable_to_shareholders=create_json_field(dp_data.get('dividends_payable_to_shareholders', {})),
            dividends_payable_from_previous_years=create_json_field(dp_data.get('dividends_payable_from_previous_years', {}))
        )

        # ShortTermLoans
        stl_data = current_liability_data.get('ShortTermLoans', {})
        ShortTermLoans.objects.create(
            current_liability=current_liability,
            loans_from_banks=create_json_field(stl_data.get('loans_from_banks', {})),
            loans_from_individuals=create_json_field(stl_data.get('loans_from_individuals', {}))
        )

        # AdvancesAndDeposits
        ad_data = current_liability_data.get('AdvancesAndDeposits', {})
        AdvancesAndDeposits.objects.create(
            current_liability=current_liability,
            advances_for_goods_sales=create_json_field(ad_data.get('advances_for_goods_sales', {})),
            advances_for_services=create_json_field(ad_data.get('advances_for_services', {})),
            advances_for_contracts=create_json_field(ad_data.get('advances_for_contracts', {})),
            deposits_from_others=create_json_field(ad_data.get('deposits_from_others', {}))
        )

        # LiabilitiesRelatedToAssetsHeldForSale
        lr_data = current_liability_data.get('LiabilitiesRelatedToAssetsHeldForSale', {})
        LiabilitiesRelatedToAssetsHeldForSale.objects.create(
            current_liability=current_liability,
            related_loans=create_json_field(lr_data.get('related_loans', {})),
            related_major_repairs_liability=create_json_field(lr_data.get('related_major_repairs_liability', {})),
            related_deferred_tax=create_json_field(lr_data.get('related_deferred_tax', {})),
            related_expert_fees_payable=create_json_field(lr_data.get('related_expert_fees_payable', {}))
        )

        # TaxProvision
        tp_data = current_liability_data.get('TaxProvision', {})
        TaxProvision.objects.create(
            current_liability=current_liability,
            amount=create_json_field(tp_data.get('tax_provision', {}))
        )

        # TaxPayable
        tpay_data = current_liability_data.get('TaxPayable', {})
        TaxPayable.objects.create(
            current_liability=current_liability,
            payroll_tax=create_json_field(tpay_data.get('payroll_tax', {})),
            withholding_tax=create_json_field(tpay_data.get('withholding_tax', {})),
            vat_payable=create_json_field(tpay_data.get('vat_payable', {})),
            income_tax_payable=create_json_field(tpay_data.get('income_tax_payable', {}))
        )

        # LongTermLiability
        long_term_liability_data = balance_sheet_data.get('LongTermLiability', {})
        long_term_liability = LongTermLiability.objects.create(balance_sheet=balance_sheet)

        # LongTermAccountsPayable
        ltap_data = long_term_liability_data.get('LongTermAccountsPayable', {})
        LongTermAccountsPayable.objects.create(
            long_term_liability=long_term_liability,
            long_term_notes_payable=create_json_field(ltap_data.get('long_term_notes_payable', {})),
            long_term_accounts_payable=create_json_field(ltap_data.get('long_term_accounts_payable', {}))
        )

        # LongTermLoans
        ltl_data = long_term_liability_data.get('LongTermLoans', {})
        LongTermLoans.objects.create(
            long_term_liability=long_term_liability,
            loans_from_banks=create_json_field(ltl_data.get('loans_from_banks', {}))
        )

        # LongTermProvisions
        ltp_data = long_term_liability_data.get('LongTermProvisions', {})
        LongTermProvisions.objects.create(
            long_term_liability=long_term_liability,
            employee_end_of_service_benefits=create_json_field(ltp_data.get('Employee Termination Benefit Reserve', {}))
        )

        # Equity
        equity_data = balance_sheet_data.get('Equity', {})
        equity = Equity.objects.create(balance_sheet=balance_sheet)

        # InitialCapital
        ic_data = equity_data.get('InitialCapital', {})
        InitialCapital.objects.create(
            equity=equity,
            amount=create_json_field(ic_data.get('initial_capital', {}))
        )

        # CapitalIncreaseDecrease
        cid_data = equity_data.get('CapitalIncreaseDecrease', {})
        CapitalIncreaseDecrease.objects.create(
            equity=equity,
            amount=create_json_field(cid_data.get('capital_increase_decrease', {}))
        )

        # SharePremiumReserve
        spr_data = equity_data.get('SharePremiumReserve', {})
        SharePremiumReserve.objects.create(
            equity=equity,
            amount=create_json_field(spr_data.get('share_premium_reserve', {}))
        )

        # ShareDiscountReserve
        sdr_data = equity_data.get('ShareDiscountReserve', {})
        ShareDiscountReserve.objects.create(
            equity=equity,
            amount=create_json_field(sdr_data.get('share_discount_reserve', {}))
        )

        # LegalReserve
        lr_data = equity_data.get('LegalReserve', {})
        LegalReserve.objects.create(
            equity=equity,
            amount=create_json_field(lr_data.get('legal_reserve', {}))
        )

        # OtherReserves
        or_data = equity_data.get('OtherReserves', {})
        OtherReserves.objects.create(
            equity=equity,
            amount=create_json_field(or_data.get('other_reserves', {}))
        )

        # RevaluationSurplus
        rs_data = equity_data.get('RevaluationSurplus', {})
        RevaluationSurplus.objects.create(
            equity=equity,
            amount=create_json_field(rs_data.get('revaluation_surplus', {}))
        )

        # ForeignCurrencyTranslationDifference
        fctd_data = equity_data.get('ForeignCurrencyTranslationDifference', {})
        ForeignCurrencyTranslationDifference.objects.create(
            equity=equity,
            amount=create_json_field(fctd_data.get('foreign_currency_translation_difference', {}))
        )

        # RetainedEarnings
        re_data = equity_data.get('RetainedEarnings', {})
        RetainedEarnings.objects.create(
            equity=equity,
            amount=create_json_field(re_data.get('retained_earnings', {}))
        )

        # Revenue
        revenue_data = balance_sheet_data.get('Revenue', {})
        revenue = Revenue.objects.create(balance_sheet=balance_sheet)

        # NetSales
        ns_data = revenue_data.get('NetSales', {})
        NetSales.objects.create(
            revenue=revenue,
            amount=create_json_field(ns_data.get('net_sales', {}))
        )

        # ServiceRevenue
        sr_data = revenue_data.get('ServiceRevenue', {})
        ServiceRevenue.objects.create(
            revenue=revenue,
            amount=create_json_field(sr_data.get('service_revenue', {}))
        )

        # ForeignCurrencyRevenue
        fcr_data = revenue_data.get('ForeignCurrencyRevenue', {})
        ForeignCurrencyRevenue.objects.create(
            revenue=revenue,
            amount=create_json_field(fcr_data.get('foreign_currency_revenue', {}))
        )

        # OtherOperatingRevenue
        oor_data = revenue_data.get('OtherOperatingRevenue', {})
        OtherOperatingRevenue.objects.create(
            revenue=revenue,
            amount=create_json_field(oor_data.get('other_operating_revenue', {}))
        )

        # Expense
        expense_data = balance_sheet_data.get('Expense', {})
        expense = Expense.objects.create(balance_sheet=balance_sheet)

        # ProductionCosts
        pc_data = expense_data.get('ProductionCosts', {})
        ProductionCosts.objects.create(
            expense=expense,
            direct_materials=create_json_field(pc_data.get('direct_materials', {})),
            direct_labor=create_json_field(pc_data.get('direct_labor', {})),
            machinery_depreciation=create_json_field(pc_data.get('machinery_depreciation', {})),
            production_line_insurance=create_json_field(pc_data.get('production_line_insurance', {})),
            energy_and_fuel=create_json_field(pc_data.get('energy_and_fuel', {})),
            equipment_maintenance=create_json_field(pc_data.get('equipment_maintenance', {})),
            production_consumables=create_json_field(pc_data.get('production_consumables', {})),
            production_rent=create_json_field(pc_data.get('production_rent', {})),
            raw_material_transport=create_json_field(pc_data.get('raw_material_transport', {}))
        )

        # DistributionAndMarketingCosts
        dmc_data = expense_data.get('DistributionAndMarketingCosts', {})
        DistributionAndMarketingCosts.objects.create(
            expense=expense,
            marketing_salaries=create_json_field(dmc_data.get('marketing_salaries', {})),
            advertising_and_promotions=create_json_field(dmc_data.get('advertising_and_exhibitions', {})),
            warehousing_costs=create_json_field(dmc_data.get('warehousing_costs', {})),
            transportation_to_customers=create_json_field(dmc_data.get('transportation_to_customers', {})),
            after_sales_services=create_json_field(dmc_data.get('after_sales_services', {})),
            sales_commissions=create_json_field(dmc_data.get('sales_commissions', {})),
            packaging_and_labeling=create_json_field(dmc_data.get('packaging_and_labeling', {})),
            exhibitions_and_events=create_json_field(dmc_data.get('advertising_and_exhibitions', {}))  # Map to same field as no separate field
        )

        # GeneralAndAdministrativeCosts
        gac_data = expense_data.get('GeneralAndAdministrativeCosts', {})
        GeneralAndAdministrativeCosts.objects.create(
            expense=expense,
            administrative_salaries_payable=create_json_field(gac_data.get('administrative_salaries_payable', {})),
            head_office_rent=create_json_field(gac_data.get('head_office_rent', {})),
            utility_bills=create_json_field(gac_data.get('utility_bills', {})),
            office_supplies=create_json_field(gac_data.get('office_supplies', {})),
            administrative_assets_depreciation=create_json_field(gac_data.get('administrative_assets_depreciation', {})),
            general_insurance=create_json_field(gac_data.get('general_insurance', {})),
            audit_and_consulting_fees=create_json_field(gac_data.get('audit_and_accounting_fees', {})),
            hospitality_and_transport=create_json_field(gac_data.get('hospitality_and_transport', {}))
        )

        # FinancialCosts
        fc_data = expense_data.get('FinancialCosts', {})
        FinancialCosts.objects.create(
            expense=expense,
            bank_interest_and_fees=create_json_field(fc_data.get('bank_interest_and_fees', {})),
            loan_late_penalties=create_json_field(fc_data.get('loan_late_penalties', {})),
            guarantee_fees=create_json_field(fc_data.get('guarantee_fees', {})),
            discounting_expenses_on_receivables=create_json_field(fc_data.get('discounting_expenses_on_receivables', {})),
            fund_transfer_and_bank_services=create_json_field(fc_data.get('fund_transfer_and_bank_services', {}))
        )

        # OtherOperatingCosts
        ooc_data = expense_data.get('OtherOperatingCosts', {})
        OtherOperatingCosts.objects.create(
            expense=expense,
            bad_debts_and_written_off_expense=create_json_field(ooc_data.get('bad_debts_and_written_off_expense', {})),
            fx_non_operating_gain_loss=create_json_field(ooc_data.get('fx_non_operating_gain_loss', {})),
            impairment_short_term_investments=create_json_field(ooc_data.get('impairment_short_term_investments', {})),
            inventory_write_down=create_json_field(ooc_data.get('inventory_write_down', {})),
            asset_impairment=create_json_field(ooc_data.get('asset_impairment', {})),
            impairment_long_term_investments=create_json_field(ooc_data.get('impairment_long_term_investments', {})),
            fx_operating_gain_loss=create_json_field(ooc_data.get('fx_operating_gain_loss', {}))
        )

        # ContingentAccount
        contingent_data = balance_sheet_data.get('ContingentAccount', {})
        contingent_account = ContingentAccount.objects.create(balance_sheet=balance_sheet)

        # ContingentAccounts
        ca_data = contingent_data.get('ContingentAccounts', {})
        ContingentAccounts.objects.create(
            contingent_account=contingent_account,
            our_accounts_with_others=create_json_field(ca_data.get('our_accounts_with_others', {}))['amount'],
            others_accounts_with_us=create_json_field(ca_data.get('others_accounts_with_us', {}))['amount']
        )

        # ContingentCounterparties
        cc_data = contingent_data.get('ContingentCounterparties', {})
        ContingentCounterparties.objects.create(
            contingent_account=contingent_account,
            our_counterparties_with_others="N/A",  # Not provided in JSON, set as needed
            others_counterparties_with_us="N/A",   # Not provided in JSON, set as needed
            amount=create_json_field(cc_data.get('our_counterparties_with_others', {}))['amount']
        )

        return balance_sheet
    
# Example usage:
# import json
# with open('balance_sheet.json', 'r') as file:
#     json_data = json.load(file)
# balance_sheet = insert_balance_sheet_data(json_data, company_id=1, year=2025)