import pandas as pd
import json
import unicodedata
import re



def read_balance_sheet_excel(file_path):

    # Enhanced normalization function
    def normalize_farsi(text):
        if not text:
            return text
        text = text.strip()
        # Replace common variations
        text = text.replace('\u200c', '')  # Zero-width non-joiner
        text = text.replace('\u2019', '')  # Right single quotation mark
        text = text.replace('\u2018', '')  # Left single quotation mark
        text = text.replace('\u200e', '')  # Left-to-right mark
        text = text.replace('\u200f', '')  # Right-to-left mark
        # Normalize slashes and spaces
        text = re.sub(r'\s*/\s*', '/', text)  # Standardize slashes
        text = re.sub(r'\s+', '', text)       # Remove all spaces
        # Normalize parentheses
        text = text.replace('(', '').replace(')', '')
        # Normalize Persian/Arabic characters
        text = text.replace('ي', 'ی')  # Arabic Yeh to Persian Yeh
        text = text.replace('ك', 'ک')  # Arabic Kaf to Persian Kaf
        # Normalize Unicode form
        text = unicodedata.normalize('NFKC', text)
        return text

    # Define the JSON template
    balance_sheet = {
        "BalanceSheet": {
            "CurrentAsset": {
                "Cash": {},
                "ShortTermInvestment": {},
                "TradeReceivable": {},
                "NonTradeReceivable": {},
                "ShareholderReceivable": {},
                "Inventory": {},
                "OrdersAndPrepayments": {},
                "AssetsHeldForSale": {}
            },
            "FixedAsset": {
                "IntangibleAsset": {},
                "TangibleFixedAsset": {},
                "AssetsInProgress": {},
                "LongTermInvestment": {},
                "OtherNonCurrentAsset": {}
            },
            "CurrentLiability": {
                "TradeAccountsPayable": {},
                "NonTradeAccountsPayable": {},
                "ShareholderPayables": {},
                "DividendsPayable": {},
                "ShortTermLoans": {},
                "AdvancesAndDeposits": {},
                "LiabilitiesRelatedToAssetsHeldForSale": {},
                "TaxProvision": {},
                "TaxPayable": {}
            },
            "LongTermLiability": {
                "LongTermAccountsPayable": {},
                "LongTermLoans": {},
                "LongTermProvisions": {}
            },
            "Equity": {
                "InitialCapital": {},
                "CapitalIncreaseDecrease": {},
                "SharePremiumReserve": {},
                "ShareDiscountReserve": {},
                "LegalReserve": {},
                "OtherReserves": {},
                "RevaluationSurplus": {},
                "ForeignCurrencyTranslationDifference": {},
                "RetainedEarnings": {}
            },
            "Revenue": {
                "NetSales": {},
                "ServiceRevenue": {},
                "ForeignCurrencyRevenue": {},
                "OtherOperatingRevenue": {}
            },
            "Expense": {
                "ProductionCosts": {},
                "DistributionAndMarketingCosts": {},
                "GeneralAndAdministrativeCosts": {},
                "FinancialCosts": {},
                "OtherOperatingCosts": {}
            },
            "ContingentAccount": {
                "ContingentAccounts": {},
                "ContingentCounterparties": {}
            }
        }
    }

    # Main section mappings
    main_mappings = {
        'دارایی‌های جاری': 'CurrentAsset',
        'دارایی های غیر جاری': 'FixedAsset',
        'بدهی‌های جاری': 'CurrentLiability',
        'بدهی‌های بلندمدت': 'LongTermLiability',
        'حقوق صاحبان سهام': 'Equity',
        'درآمدها': 'Revenue',
        'هزینه ها': 'Expense',
        'حساب‌های انتظامی': 'ContingentAccount'
    }

    # Sub-section mappings
    sub_mappings = {
        'CurrentAsset': {
            'موجودی نقد': 'Cash',
            'سرمایه‌گذاری‌های کوتاه‌مدت': 'ShortTermInvestment',
            'حساب‌ها و اسناد دریافتنی تجاری': 'TradeReceivable',
            'حسابها و اسناد دریافتنی غیرتجاری': 'NonTradeReceivable',
            'جاری شرکا/سهامداران': 'ShareholderReceivable',
            'موجودی مواد و کالا': 'Inventory',
            'سفارش‌ها و پیش‌پرداخت‌ها': 'OrdersAndPrepayments',
            'دارایی نگهداری شده برای فروش': 'AssetsHeldForSale'
        },
        'FixedAsset': {
            'دارایی‌های نامشهود': 'IntangibleAsset',
            'دارایی‌های ثابت مشهود': 'TangibleFixedAsset',
            'دارایی در جریان تکمیل': 'AssetsInProgress',
            'سرمایه‌گذاری بلندمدت': 'LongTermInvestment',
            'سایر دارایی های غیر جاری': 'OtherNonCurrentAsset'
        },
        'CurrentLiability': {
            'حساب ها و اسناد پرداختنی تجاری': 'TradeAccountsPayable',
            'حساب‌ها و اسناد پرداختنی غیرتجاری': 'NonTradeAccountsPayable',
            'جاری شرکا/سهامداران': 'ShareholderPayables',
            'سود سهام پرداختنی': 'DividendsPayable',
            'تسهیلات مالی دریافتی کوتاه‌مدت': 'ShortTermLoans',
            'پیش‌دریافت‌ها و سپرده‌ها': 'AdvancesAndDeposits',
            'بدهی‌های مرتبط با دارایی‌های نگهداری‌شده برای فروش': 'LiabilitiesRelatedToAssetsHeldForSale',
            'ذخیره مالیات': 'TaxProvision',
            'مالیات پرداختنی': 'TaxPayable'
        },
        'LongTermLiability': {
            'حساب ها و اسناد پرداختنی بلندمدت': 'LongTermAccountsPayable',
            'تسهیلات مالی دریافتی بلندمدت': 'LongTermLoans',
            'ذخایر بلند مدت': 'LongTermProvisions'
        },
        'Equity': {
            'سرمایه اولیه': 'InitialCapital',
            'افزایش /کاهش سرمایه': 'CapitalIncreaseDecrease',
            'اندوخته‌ی صرف سهام': 'SharePremiumReserve',
            'اندوخته کسر سهام': 'ShareDiscountReserve',
            'اندوخته‌ی قانونی': 'LegalReserve',
            'سایر اندوخته‌ها': 'OtherReserves',
            'مازاد تجدید ارزیابی دارایی‌ها': 'RevaluationSurplus',
            'تفاوت تسعیر ارز': 'ForeignCurrencyTranslationDifference',
            'سود (زیان)انباشته': 'RetainedEarnings'
        },
        'Revenue': {
            'خالص فروش': 'NetSales',
            'درامد ارائه خدمات': 'ServiceRevenue',
            'درآمد تسعیر ارز': 'ForeignCurrencyRevenue',
            'سایر درآمدهای عملیاتی': 'OtherOperatingRevenue'
        },
        'Expense': {
            'هزینه های تولید': 'ProductionCosts',
            'هزینه‌های توزیع و فروش و بازاریابی': 'DistributionAndMarketingCosts',
            'هزینه های عمومی و اداری': 'GeneralAndAdministrativeCosts',
            'هزینه‌های مالی': 'FinancialCosts',
            'سایر هزینه های عملیاتی': 'OtherOperatingCosts'
        },
        'ContingentAccount': {
            'حساب‌های انتظامی': 'ContingentAccounts',
            'طرف حساب‌های انتظامی': 'ContingentCounterparties'
        }
    }

    # Extended FIELD_FARSI_MAP
    FIELD_FARSI_MAP = {
        "BalanceSheet": {
            "date": "تاریخ",
            "current_assets": "دارایی جاری",
            "non_current_assets": "دارایی غیر جاری",    
            "current_liabilities": "بدهی جاری",
            "long_term_liabilities": "بدهی بلندمدت",
            "equity": "حقوق صاحبان سهام",
            "revenue": "درآمد",
            "expense": "هزینه",
            "contingent_account": "حساب انتظامی",
        },
        "CurrentAsset": {
            "balance_sheet": "ترازنامه",
            "name": "نام",
            "amount": "مبلغ",
        },
        "Cash": {
            "current_asset": "دارایی جاری",
            "cash_in_hand": "صندوق",
            "bank_balances": "بانک‌ها",
            "petty_cash": "تنخواه‌گردان‌ها",
            "cash_in_transit": "وجوه در راه",
        },
        "ShortTermInvestment": {
            "current_asset": "دارایی جاری",
            "short_term_deposits": "سپرده‌های کوتاه مدت",
            "tradable_stocks": "سهام بورسی قابل معامله",
            "participation_bonds": "اوراق مشارکت",
            "etf_investment_fund": "صندوق سرمایه گذاری قابل معامله (ETF)",
            "other_short_term_investments": "سایر سرمایه گذاری‌های کوتاه‌مدت",
            "short_term_investment_impairment": "ذخیره‌ی کاهش ارزش سرمایه‌گذاری‌های کوتاه‌مدت",
        },
        "TradeReceivable": {
            "current_asset": "دارایی جاری",
            "trade_accounts_receivable": "حساب‌های دریافتنی تجاری",
            "trade_notes_receivable": "اسناد دریافتنی تجاری",
            "receivables_in_litigation": "حساب‌های دریافتنی در دعاوی حقوقی",
            "notes_in_collection": "اسناد درجریان وصول",
            "returned_cheques": "اسناد دریافتنی واخواستی (چک‌های برگشتی مشتری)",
            "doubtful_receivables_provision": "ذخیره‌ی مطالبات مشکوک‌الوصول",
        },
        "NonTradeReceivable": {
            "current_asset": "دارایی جاری",
            "non_trade_accounts_receivable": "حساب‌های دریافتنی غیرتجاری",
            "non_trade_notes_receivable": "اسناد دریافتنی غیرتجاری",
            "employee_receivables": "حساب‌های دریافتنی از کارکنان (وام و مساعده)",
            "director_receivables": "حساب‌های دریافتنی از مدیران و اعضای هیات مدیره",
            "related_companies_receivables": "حساب‌های دریافتنی از شرکت‌ها و اشخاص وابسته",
            "vat_receivable": "مالیات بر ارزش افزوده",
            "deposits_with_others": "سپرده‌های ما نزد دیگران",
            "dividends_receivable": "سود سهام دریافتنی",
        },
        "ShareholderReceivable": {
            "current_asset": "دارایی جاری",
            "amount": "مبلغ",
            "shareholder_receivables": "جاری شرکا/سهامداران",
        },
        "Inventory": {
            "current_asset": "دارایی جاری",
            "raw_materials": "موجودی مواد اولیه",
            "work_in_progress": "موجودی کالای درجریان ساخت",
            "finished_goods": "موجودی کالای ساخته شده و آماده فروش",
            "purchased_goods_for_sale": "موجودی کالای خریداری شده جهت فروش",
            "spare_parts": "موجودی قطعات و لوازم یدکی",
            "packaging_materials": "موجود مواد بسته بندی",
            "consignment_goods_with_others": "کالای امانی نزد دیگران",
            "idle_items": "موجودی اقلام راکد",
            "scrap_raw_materials": "موجودی ضایعات مواد اولیه",
            "inventory_impairment": "ذخیره کاهش ارزش موجودی",
        },
        "OrdersAndPrepayments": {
            "current_asset": "دارایی جاری",
            "prepaid_goods_and_services": "پیش‌پرداخت خرید کالا و خدمات",
            "prepaid_income_tax": "پیش‌پرداخت مالیات عملکرد",
            "prepaid_rent": "پیش‌پرداخت اجاره",
            "prepaid_insurance": "پیش‌پرداخت بیمه",
            "orders_in_transit": "سفارشات در راه",
            "prepaid_loans": "پیش پرداخت تسهیلات",
            "prepaid_interest_on_loans": "پیش پرداخت سود تسهیلات",
            "other_prepayments": "سایر پیش‌پرداخت‌ها",
        },
        "AssetsHeldForSale": {
            "current_asset": "دارایی جاری",
            "assets_held_for_sale": "دارایی نگهداری شده برای فروش",
            "impairment_reserve": "ذخیره کاهش ارزش دارایی",
        },
        "FixedAsset": {
            "balance_sheet": "ترازنامه",
        },
        "IntangibleAsset": {
            "fixed_asset": "دارایی ثابت",
            "software": "نرم‌افزار",
            "royalty": "حق الامتیاز",
            "goodwill": "سرقفلی",
            "patent": "حق اختراع",
            "trademark": "علائم تجاری و برندها",
            "copyright": "حق تالیف/ حق نشر",
            "pre_operating_expenses": "هزینه های قبل از بهره برداری",
        },
        "TangibleFixedAsset": {
            "fixed_asset": "دارایی ثابت",
            "land": "زمین",
            "building": "ساختمان",
            "installations": "تاسیسات",
            "machinery_and_equipment": "ماشین‌آلات و تجهیزات",
            "vehicles": "وسایل نقلیه",
            "office_furniture": "اثاثیه اداری",
            "accumulated_depreciation": "استهلاک انباشته‌ی دارایی غیر جاری",
        },
        "AssetsInProgress": {
            "fixed_asset": "دارایی ثابت",
            "assets_in_progress": "دارایی‌های در جریان تکمیل",
            "amount": "مبلغ",
        },
        "LongTermInvestment": {
            "fixed_asset": "دارایی ثابت",
            "investment_in_affiliates": "سرمایه گذاری در سهام شرکت های وابسته",
            "investment_in_subsidiaries": "سرمایه گذاری در سهام شرکت های فرعی",
            "investment_in_private_companies": "سرمایه گذاری در سهام شرکت های غیربورسی",
            "long_term_bonds": "سرمایه گذاری در اوراق مشارکت بلندمدت",
            "property_investment": "سرمایه گذاری بلند مدت در املاک",
            "long_term_deposits": "سپرده های بلند مدت",
            "long_term_participation_in_projects": "مشارکت بلند مدت در طرح ها و پروژه ها",
            "long_term_treasury_investment": "سرمایه گذاری بلند مدت در اوراق خزانه",
            "long_term_investment_impairment": "ذخیره کاهش ارزش سرمایه گذاری های بلند مدت",
        },
        "OtherNonCurrentAsset": {
            "fixed_asset": "دارایی ثابت",
            "other_non_current_assets": "سایر دارایی های غیرجاری",
            "amount": "مبلغ",
        },
        "CurrentLiability": {
            "balance_sheet": "ترازنامه",
        },
        "TradeAccountsPayable": {
            "current_liability": "بدهی جاری",
            "domestic_suppliers": "حساب ها و اسناد پرداختنی به تامین کننده داخلی",
            "foreign_suppliers": "حساب ها و اسناد پرداختنی به تامین کننده خارجی",
        },
        "NonTradeAccountsPayable": {
            "current_liability": "بدهی جاری",
            "non_trade_accounts_payable": "حسابها و اسناد پرداختنی غیر تجاری",
            "salaries_payable": "حقوق و دستمزد پرداختنی",
            "social_security_payable": "سازمان تامین اجتماعی (حق بیمه‌ی کارکنان)",
            "deposits_from_entities": "سپرده دریافتی از اشخاص حقیقی و حقوقی",
            "deposits_from_individuals": "سپرده دریافتنی از اشخاص حقیقی",
            "accrued_unpaid_expenses_provision": "ذخیره‌ی هزینه‌های تحقق‌یافته‌ی پرداخت‌نشده",
        },
        "ShareholderPayables": {
            "current_liability": "بدهی جاری",
            "shareholder_payables": "جاری شرکا/سهامداران",
            "amount": "مبلغ",
        },
        "DividendsPayable": {
            "current_liability": "بدهی جاری",
            "dividends_payable_to_individuals": "سود سهام پرداختنی به اشخاص",
            "dividends_payable_to_shareholders": "سود سهام پرداختنی به سهامداران",
            "dividends_payable_from_previous_years": "سود سهام پرداختنی سنوات گذشته",
        },
        "ShortTermLoans": {
            "current_liability": "بدهی جاری",
            "loans_from_banks": "تسهیلات مالی دریافتی از بانک‌ها",
            "loans_from_individuals": "تسهیلات مالی دریافتی از اشخاص",
        },
        "AdvancesAndDeposits": {
            "current_liability": "بدهی جاری",
            "advances_for_goods_sales": "پیش‌دریافت فروش کالا",
            "advances_for_services": "پیش‌دریافت ارائه خدمات",
            "advances_for_contracts": "پیش‌دریافت قرارداد پیمانکاری",
            "deposits_from_others": "سپرده های دیگران نزد ما",
        },
        "LiabilitiesRelatedToAssetsHeldForSale": {
            "current_liability": "بدهی جاری",
            "related_loans": "تسهیلات دریافت شده مربوطه",
            "related_major_repairs_liability": "بدهی بابت تعمیرات اساسی مربوطه",
            "related_deferred_tax": "مالیات معوق مربوطه",
            "related_expert_fees_payable": "حق‌الزحمه‌ی پرداختنی کارشناس رسمی",
        },
        "TaxProvision": {
            "current_liability": "بدهی جاری",
            "tax_provision": "ذخیره مالیات",
            "amount": "مبلغ",
        },
        "TaxPayable": {
            "current_liability": "بدهی جاری",
            "payroll_tax": "سازمان امور مالیاتی (مالیات حقوق)",
            "withholding_tax": "سازمان امور مالیاتی (مالیات تکلیفی)",
            "vat_payable": "سازمان امور مالیاتی (مالیات ارزش افزوده)",
            "income_tax_payable": "سازمان امور مالیاتی (مالیات عملکرد)",
        },
        "LongTermLiability": {
            "balance_sheet": "ترازنامه",
        },
        "LongTermAccountsPayable": {
            "long_term_liability": "بدهی بلندمدت",
            "long_term_notes_payable": "اسناد پرداختنی بلند مدت",
            "long_term_accounts_payable": "حساب های پرداختنی بلند مدت",
        },
        "LongTermLoans": {
            "long_term_liability": "بدهی بلندمدت",
            "loans_from_banks": "تسهیلات مالی دریافتی بلندمدت از بانک‌ها",
        },
        "LongTermProvisions": {
            "long_term_liability": "بدهی بلندمدت",
            "employee_end_of_service_benefits": "ذخیره‌ی مزایای پایان خدمت کارکنان",
            "Employee Termination Benefit Reserve": "ذخیره‌ی مزایای پایان خدمت کارکنان",
        },
        "Equity": {
            "balance_sheet": "ترازنامه",
            "initial_capital": "سرمایه اولیه",
            "capital_increase_decrease": "افزایش/کاهش سرمایه",
            "share_premium_reserve": "اندوخته‌ی صرف سهام",
            "share_discount_reserve": "اندوخته کسر سهام",
            "legal_reserve": "اندوخته‌ی قانونی",
            "other_reserves": "سایر اندوخته‌ها",
            "revaluation_surplus": "مازاد تجدید ارزیابی دارایی‌ها",
            "foreign_currency_translation_difference": "تفاوت تسعیر ارز",
            "retained_earnings": "سود (زیان)انباشته",
        },
        "Revenue": {
            "balance_sheet": "ترازنامه",
            "net_sales": "خالص فروش",
            "service_revenue": "درامد ارائه خدمات",
            "foreign_currency_revenue": "درآمد تسعیر ارز",
            "other_operating_revenue": "سایر درآمدهای عملیاتی",
            "incidental_revenue": "درآمد اتفاقی",
            "non_operating_revenue": "درآمدهای غیرعملیاتی",
            "rental_income": "درآمد اجاره",
        },
        "Expense": {
            "balance_sheet": "ترازنامه",
        },
        "ProductionCosts": {
            "expense": "هزینه",
            "direct_materials": "مواد مستقیم مصرفی",
            "direct_labor": "دستمزد مستقیم - تولید",
            "machinery_depreciation": "استهلاک ماشین آلات",
            "production_line_insurance": "بیمه خط تولید",
            "energy_and_fuel": "انرژی و سوخت مصرفی تولید",
            "equipment_maintenance": "تعمیر و نگهداری تجهیزات تولید",
            "production_consumables": "ابزار مصرفی تولید",
            "production_rent": "اجاره فضای تولید",
            "raw_material_transport": "حمل و نقل مواد اولیه",
        },
        "DistributionAndMarketingCosts": {
            "expense": "هزینه",
            "marketing_salaries": "هزینه حقوق و دستمزد - بازاریابی و فروش",
            "advertising_and_promotions": "هزینه‌های تبلیغات، بازاریابی، کاتالوگ و بروشور",
            "advertising_and_exhibitions": "هزینه‌های تبلیغات، بازاریابی، کاتالوگ و بروشور و نمایشگاه ها",
            "warehousing_costs": "هزینه‌ی انبارداری",
            "transportation_to_customers": "حمل و نقل کالا به مشتری",
            "after_sales_services": "هزینه خدمات پس از فروش",
            "sales_commissions": "پورسانت فروش",
            "packaging_and_labeling": "بسته بندی و لیبل زنی",
            "exhibitions_and_events": "نمایشگاه ها و رویدادهای تبلیغاتی",
        },
        "GeneralAndAdministrativeCosts": {
            "expense": "هزینه",
            "administrative_salaries_payable": "حقوق و دستمزد پرداختنی - اداری",
            "head_office_rent": "اجاره دفتر مرکزی",
            "utility_bills": "قبوض",
            "office_supplies": "هزینه ملزومات",
            "administrative_assets_depreciation": "استهلاک دارایی های اداری",
            "general_insurance": "بیمه های عمومی",
            "audit_and_consulting_fees": "هزینه حسابرسی و مشاوره",
            "audit_and_accounting_fees": "هزینه حسابرسی و حسابداری",
            "consulting_fees": "هزینه مشاوره",
            "hospitality_and_transport": "پذیرایی و ایاب و ذهاب",
        },
        "FinancialCosts": {
            "expense": "هزینه",
            "bank_interest_and_fees": "سود و کارمزد تسهیلات بانکی",
            "loan_late_penalties": "جرائم تاخیر در بازپرداخت وام",
            "guarantee_fees": "هزینه های کارمزد ضمانت نامه ها",
            "discounting_expenses_on_receivables": "هزینه های تنزیل اسناد دریافتنی",
            "fund_transfer_and_bank_services": "هزینه انتقال وجه و خدمات بانکی",
        },
        "OtherOperatingCosts": {
            "expense": "هزینه",
            "bad_debts_and_written_off_expense": "هزینه‌ی مطالبات مشکوک‌الوصول و سوخت‌شده",
            "fx_non_operating_gain_loss": "سود و زیان تسعیر دارایی‌ها و بدهی‌های ارزی غیرمرتبط با عملیات",
            "impairment_short_term_investments": "هزینه کاهش ارزش سرمایه گذاری های کوتاه مدت",
            "inventory_write_down": "هزینه کاهش ارزش موجودی",
            "asset_impairment": "هزینه کاهش ارزش دارایی",
            "impairment_long_term_investments": "هزینه کاهش ارزش سرمایه گذاری های بلند مدت",
            "fx_operating_gain_loss": "سود و زیان ناشی از تسعیر دارایی‌ها و بدهی‌های ارزی عملیاتی",
            "non_operating_expenses": "هزینه‌های غیرعملیاتی",
        },
        "ContingentAccount": {
            "balance_sheet": "ترازنامه",
        },
        "ContingentAccounts": {
            "contingent_account": "حساب انتظامی",
            "our_accounts_with_others": "حساب انتظامی ما نزد دیگران",
            "others_accounts_with_us": "حساب انتظامی دیگران نزد ما",
        },
        "ContingentCounterparties": {
            "contingent_account": "حساب انتظامی",
            "our_counterparties_with_others": "طرف حساب انتظامی ما نزد دیگران",
            "others_counterparties_with_us": "طرف حساب انتظامی دیگران نزد ما",
            "amount": "مبلغ",
        },
    }

    # Create normalized reverse mapping for account names
    normalized_account_mappings = {}
    unmapped_names = []  # To track untranslated names with context

    for section, mappings in FIELD_FARSI_MAP.items():
        if section not in ["BalanceSheet", "CurrentAsset"]:  # Skip top-level and generic
            for english_key, farsi_name in mappings.items():
                if english_key not in ["current_asset", "fixed_asset", "current_liability", 
                                    "long_term_liability", "equity", "revenue", "expense", 
                                    "contingent_account", "balance_sheet", "amount"]:
                    normalized_key = normalize_farsi(farsi_name)
                    normalized_account_mappings[normalized_key] = english_key






    # Load the Excel file
    # file_path = 'تراز.xlsx'  # Use the actual file path
    sheet_name = 'تراز آزمایشی'
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

    # Parsing logic
    current_main = None
    current_sub = None

    for _, row in df.iterrows():
        # Set main section if applicable
        if pd.notna(row.get(1, pd.NA)) and str(row[1]).strip() in main_mappings:
            current_main = main_mappings[str(row[1]).strip()]
            current_sub = None  # Reset sub
        
        # Set sub section if applicable
        if current_main and pd.notna(row.get(3, pd.NA)) and str(row[3]).strip() in sub_mappings.get(current_main, {}):
            current_sub = sub_mappings[current_main][str(row[3]).strip()]
        
        # Add account if applicable
        if current_main and current_sub and pd.notna(row.get(4, pd.NA)):
            code = str(row[4]).strip()
            name = str(row[5]).strip() if pd.notna(row.get(5, pd.NA)) else ''
            debit = float(row[6]) if pd.notna(row.get(6, pd.NA)) else 0.0
            credit = float(row[7]) if pd.notna(row.get(7, pd.NA)) else 0.0
            if name:  # Avoid adding empty names
                # Normalize the name from Excel
                normalized_name = normalize_farsi(name)
                # Get translated name
                translated_name = normalized_account_mappings.get(normalized_name, name)
                # Log untranslated names with context
                if translated_name == name:
                    unmapped_names.append({
                        'name': name,
                        'normalized_name': normalized_name,
                        'main_section': current_main,
                        'sub_section': current_sub
                    })
                # New structure: assign type and amount based on debit/credit
                if debit != 0:
                    balance_sheet['BalanceSheet'][current_main][current_sub][translated_name] = {
                        # 'code': code,
                        'type': 'debit',
                        'amount': debit
                    }
                elif credit != 0:
                    balance_sheet['BalanceSheet'][current_main][current_sub][translated_name] = {
                        # 'code': code,
                        'type': 'credit',
                        'amount': credit
                    }
                else:
                    # Default case when both debit and credit are zero
                    balance_sheet['BalanceSheet'][current_main][current_sub][translated_name] = {
                        # 'code': code,
                        'type': 'debit',
                        'amount': 0
                    }

    # Write the populated JSON to a file
    output_file = 'balance_sheet.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(balance_sheet, f, ensure_ascii=False, indent=4)

    # Print unmapped names with context for debugging
    if unmapped_names:
        print("Untranslated account names found in Excel:")
        for item in unmapped_names:
            print(f"- Name: {item['name']}, Normalized: {item['normalized_name']}, "
                f"Main Section: {item['main_section']}, Sub Section: {item['sub_section']}")
    else:
        print("All account names were successfully translated.")


    return balance_sheet